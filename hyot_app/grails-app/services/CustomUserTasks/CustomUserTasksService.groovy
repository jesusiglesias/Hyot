package CustomUserTasks

import grails.gorm.transactions.Transactional
import groovy.time.TimeCategory
import org.apache.commons.validator.routines.EmailValidator
import org.springframework.context.MessageSource
import org.springframework.context.i18n.LocaleContextHolder
import Security.SecUser
import Security.Token

import User.*
import grails.transaction.Transactional
import org.apache.commons.validator.routines.EmailValidator
import org.springframework.context.MessageSource
import org.springframework.context.i18n.LocaleContextHolder
import groovy.time.TimeCategory


/**
 * Service that contains some utilities for the tasks of a unregistered used.
 */
@Transactional
class CustomUserTasksService {

    // It gets access to message source by convention
    MessageSource messageSource
    def mailService
    def tokenService
    def passwordEncoder
    def grailsApplication

    /*-------------------------------------------------------------------------------------------*
     *                                     RESTORE PASSWORD                                      *
     *-------------------------------------------------------------------------------------------*/

    /**
     * Email is validated (existence and validity).
     *
     * @param email User's email.
     * @return true If it is valid and exists in database.
     */
    def validate_email(String email) {
        log.debug("CustomUserTasksService:validate_email()")

        def valid_email = EmailValidator.getInstance().isValid(email)   // Email is valid
        def exist_email = SecUser.findByEmail(email)                    // Email exists in the DB

       return [valid: valid_email, exist: exist_email]
    }

    /**
     * It creates an encrypt token with the email, saves the token in database and sends the email.
     *
     * @param email User's email.
     * @return true If the action is success.
     */
    def send_email(String email) {
        log.debug("CustomUserTasksService:send_email()")

        // Encrypt
        def token = encrypt_email(email)

        // It saves the token
        create_token(token, 'restorePassword')

        // Send email
        try {
            mailService.sendMail {
                async true
                to email
                subject messageSource.getMessage("resetPassword.email.subject", null,
                        "HYOT - Reset password", LocaleContextHolder.locale)
                html(view: '/email/resetPasswordTemplate',
                        model: [token: token])
            }
            return true
        } catch (Exception exception) {
            log.error("CustomUserTasksService:send_email()" + exception)
            return false
        }
    }

    /**
     * It checks if token is correct (existence, right type and it has not been not used).
     *
     * @params token User's token.
     */
    def check_token(String token, String type) {
        log.debug("CustomUserTasksService:check_token()")

        // It obtains the expiration time
        def timeExpiration = grailsApplication.config.token.expiration ?: 30

        // It checks the validity of the token
        def currentToken = tokenService.check_token(token, type)

        if (currentToken != null) { // Valid token but it must check if token is expired or not - numeric value

            // Parsing to second
            timeExpiration = timeExpiration.toInteger()

            use(TimeCategory) {

                if(new Date() <= (currentToken.dateCreated + timeExpiration.minutes)) { // Time is valid
                    return currentToken

                } else { // Time expired
                    return null
                }
            }

        } else { // Token is invalid - Null value
            return currentToken
        }
    }

    /**
     * It updates the password of the user.
     *
     * @param params Passwords introduced by user.
     * @return true If the action is successful.
     */
    def update_pass(params) {
        log.debug("CustomUserTasksService:update_pass()")

        def valid = password_confirm(params.password, params.passwordConfirm)

        if (valid.valid && valid.match) { // Valid and equal passwords

            def email = decrypt_email(params.token) // It decrypts email

            def passwordSame = password_same(email, params.password) // It checks if password is equal to the current

            def passwordSameUsername = password_notUsername(email, params.password) // It checks if password is equal to username

            if (!passwordSame.same && !passwordSameUsername.sameUsername) { // New password is different

                log.debug("CustomUserTasksService:update_pass():passwordDifferent")

                use_token(params.token)// Token status to true

                def user = SecUser.get(SecUser.findByEmail(email).id) // It obtains the user through its email
                user.password = params.password // It changes the password

                return valid << [response: user.save(flush: true, failOnError: true)]

            } else {

                if (passwordSame.same) {
                    // Same password
                    return passwordSame << [response: false, valid: true, match: true, passwordSame: false]

                } else if (passwordSameUsername.sameUsername) {
                    // Password equal to the username
                    return passwordSameUsername << [response: false, valid: true, match: true, passwordSame: true]
                }
            }
        } else {
            return valid << [response: false] // Error found
        }
    }

    /**
     * It encrypts the email address.
     *
     * @params email Email address to encrypt.
     */
    private encrypt_email(String email) {
        log.debug("CustomUserTasksService:encrypt_email()")

        return tokenService.encrypt(email)
    }

    /**
     * It decrypts email.
     */
    private decrypt_email(String token) {
        log.debug("CustomUserTasksService:decrypt_email()")

        return tokenService.decrypt(token)
    }

    /**
     * It creates a new token.
     *
     * @params token User's token.
     */
    private create_token(String token, String type) {
        log.debug("CustomUserTasksService:create_token()")

        def dateCreated = new Date()

        return tokenService.save(new Token(token: token, tokenType: type, tokenStatus: false, dateCreated:dateCreated))
    }

    /**
     * It checks that new password is correct and is equals to passwordConfirm field.
     *
     * @param password Password introduced by user.
     * @param passwordConfirmation Password to confirm.
     * @return true If the new password is valid.
     */
    private password_confirm(String password, String passwordConfirmation) {
        log.debug("CustomUserTasksService:password_confirm()")

        String pattern = "^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=\\S+\$).{8,}\$"

        return [valid: password.matches(pattern), match: password.equals(passwordConfirmation)]
    }

    /**
     * It checks if the password introduced is equal to the current, searching to the user.
     *
     * @param email User's email.
     * @param password Password introduced.
     * @return true If the password introduced is the same.
     */
    private password_same(String email, String newPassword) {
        log.debug("CustomUserTasksService:password_same()")

        def userOldPassword = SecUser.findByEmail(email).getPassword()

        return [same: passwordEncoder.isPasswordValid(userOldPassword, newPassword, null)]
    }

    /**
     * It checks if the password introduced is equal to the username.
     *
     * @param email User's email.
     * @param password Password introduced.
     * @return true If the password introduced is equal to the username.
     */
    private password_notUsername(String email, String newPassword) {
        log.debug("CustomUserTasksService:password_notUsername()")

        def username = SecUser.findByEmail(email).getUsername()

        return [sameUsername: newPassword.toLowerCase().equals(username.toLowerCase())]
    }

    /**
     * It changes the status of token to true.
     *
     * @param token Token.
     * @return true If the action is successful.
     */
    private use_token(String token) {
        log.debug("CustomUserTasksService:use_token()")

        return tokenService.use_token(token)
    }
}