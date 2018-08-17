package CustomUserTasks

import Security.Token
import grails.gorm.transactions.Transactional
import Security.SecUser
import org.apache.commons.validator.routines.EmailValidator
import org.springframework.context.MessageSource
import org.springframework.context.i18n.LocaleContextHolder

/**
 * Service that contains some utilities for the tasks of a unregistered used.
 */
@Transactional
class CustomUserTasksService {

    // It gets access to message source by convention
    MessageSource messageSource
    def mailService
    def tokenService

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
     * It encrypts the email address.
     *
     * @params email Email address to encrypt.
     */
    private encrypt_email(String email) {
        log.debug("CustomUserTasksService:encrypt_email()")

        return tokenService.encrypt(email)
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
}