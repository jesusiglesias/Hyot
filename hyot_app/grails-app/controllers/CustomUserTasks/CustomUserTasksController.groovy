package CustomUserTasks

import grails.gorm.transactions.Transactional
import org.springframework.beans.factory.annotation.Value
import grails.plugin.springsecurity.SpringSecurityUtils
import org.apache.commons.lang.StringUtils
import org.springframework.security.authentication.AccountExpiredException
import org.springframework.security.authentication.AuthenticationServiceException
import org.springframework.security.authentication.CredentialsExpiredException
import org.springframework.security.authentication.DisabledException
import org.springframework.security.authentication.LockedException
import org.springframework.security.web.authentication.session.SessionAuthenticationException
import org.springframework.security.web.WebAttributes

/**
 * It contains the habitual custom general tasks of the user.
 */
class CustomUserTasksController {

    static allowedMethods = [sendEmail: "POST", updatePass: "POST"]

    def customUserTasksService
    def springSecurityService

    // Obtain the default url of users
    @Value('${springsecurity.urlredirection.admin}')
            redirectionControlPanel
    @Value('${springsecurity.urlredirection.user}')
            redirectionUserPage

    @Value('${springsecurity.urlredirection.noRole}')
            redirectionNoRole

    /**
     * It obtains the default URL redirection based on role from the call successHandler.defaultTargetUrl.
     *
     * @return urlRedirection URL to redirection to the user.
     */
    def loggedIn() {
        log.debug("CustomUserTasksController:loggedIn()")

        // Redirection to control panel
        if (SpringSecurityUtils.ifAllGranted('ROLE_ADMIN')) {
            log.debug("CustomUserTasksController:loggedIn():adminRole")
            redirect uri: redirectionControlPanel

        } else if (SpringSecurityUtils.ifAllGranted('ROLE_USER')) {  // Redirection to user page
            log.debug("CustomUserTasksController:loggedIn():userRole")
            redirect uri: redirectionUserPage

        } else { // Redirection to /noRole
            log.error("CustomUserTasksController:loggedIn():noRole:User:${springSecurityService.authentication.principal.username}:Email:${springSecurityService.authentication.principal.email}") // It obtains the username and email from cache by principal
            redirect uri: redirectionNoRole
        }
    }

    /**
     * Callback after a failed login. Redirects to the "/" page with a warning message.
     *
     * @return failMessage Message to show to the user.
     */
    def authFail() {
        log.debug("CustomUserTasksController:authFail()")

        String failMessage = ''
        String messageType = ''
        String failDisabledMessage = ''
        String failUserMessage = ''
        String failAuthenticationMessage = ''
        String failSessions = ''

        // Fail exceptions
        def exception = session[WebAttributes.AUTHENTICATION_EXCEPTION]
        if (exception) {
            if (exception instanceof AccountExpiredException) {
                log.error("CustomUserTasksController:authFail():accountExpired:UserOrEmailIntroduced:${session['SPRING_SECURITY_LAST_USERNAME']}")

                messageType = "accountExpired"
                failMessage = g.message(code: "customUserTasks.login.expired",
                        default: 'Sorry, your user account has expired.')

            } else if (exception instanceof CredentialsExpiredException) {
                log.error("CustomUserTasksController:authFail():passwordExpired:UserOrEmailIntroduced:${session['SPRING_SECURITY_LAST_USERNAME']}")

                messageType = "passwordExpired"
                failMessage = g.message(code: "customUserTasks.login.passwordExpired",
                        default: 'Sorry, your password has expired.')

            } else if (exception instanceof DisabledException) {
                log.error("CustomUserTasksController:authFail():accountDisabled:UserOrEmailIntroduced:${session['SPRING_SECURITY_LAST_USERNAME']}")

                failDisabledMessage = g.message(code: "customUserTasks.login.disabled",
                        default: 'Sorry, your account is disabled. Contact with an administrator to enable it.')

            } else if (exception instanceof LockedException) {
                log.error("CustomUserTasksController:authFail():accountLocked:UserOrEmailIntroduced:${session['SPRING_SECURITY_LAST_USERNAME']}")

                messageType = "accountLocked"
                failMessage = g.message(code: "customUserTasks.login.locked",
                        default: 'Sorry, your user account has been locked by the administrator.')

            } else if (exception instanceof AuthenticationServiceException) {
                log.error("CustomUserTasksController:authFail():authenticationService")

                failAuthenticationMessage = g.message(code: "customUserTasks.login.authenticationException",
                        default: 'An internal error has occurred during log in.')

            } else if (exception instanceof SessionAuthenticationException){
                log.error("CustomUserTasksController:authFail():sessionAuthentication")

                failSessions = g.message(code: "customUserTasks.login.concurrentSessions",
                        default: 'Maximum sessions for this user exceeded. Limit: 1 session.')

            } else {
                log.debug("CustomUserTasksController:authFail():fail")

                failUserMessage = g.message(code: "customUserTasks.login.fail",
                        default: '<strong>Sorry, we were not able to find a user with these credentials.</strong>')
            }
        }

        flash.errorLogin = failMessage
        flash.errorMessageType = messageType
        flash.errorDisabledLogin = failDisabledMessage
        flash.errorLoginUser = failUserMessage
        flash.errorInvalidSessionAuthenticationException = failAuthenticationMessage
        flash.errorSessions = failSessions
        redirect(controller: 'login', action: 'auth')
    }

    /*-------------------------------------------------------------------------------------------*
     *                                     RESTORE PASSWORD                                      *
     *-------------------------------------------------------------------------------------------*/
    /**
     * It renders the view to restore the password.
     *
     * @return restorePassword View to introduce the email of the user account.
     */
    def restorePassword(){
        render view: '/login/restorePassword'
    }

    /**
     * It checks the user's email and sends an email to restore the password.
     *
     * @return restorePassword View to inform the user of the success or failure of the action.
     */
    @Transactional(readOnly = false)
    sendEmail(){
        log.debug("CustomUserTasksController:sendEmail():email:${params.email as String}")

        // Email validation
        def valid_email = customUserTasksService.validate_email(params.email as String)

        // Email is valid and exists
        if(valid_email.valid && valid_email.exist){

            if (!customUserTasksService.send_email(params.email as String)) {
                log.error("CustomUserTasksController:sendEmail():NOTMailSent:to:${params.email}")

                // Roll back in database
                transactionStatus.setRollbackOnly()

                flash.errorRestorePassword = g.message(code: 'customUserTasks.sendEmail.error',
                        default: 'An internal error has occurred during the sending email. You try it again later.')

            } else {
                log.debug("CustomTasksUserController:sendEmail():mailSent:${params.email}")
                flash.successRestorePassword = g.message(code: 'customUserTasks.sendEmail.success',
                        default: 'Notification processed. You will receive an email valid for 30 minutes with the instructions to follow to reset your password.')

                redirect uri: '/forgotPassword'
                return
            }
        } else{ // Email is not valid
            log.debug("CustomUserTasksController:sendEmail():invalidSyntax/notExists")

            if (!valid_email.valid) { // Invalid (syntax)
                log.error("ForgotPassword():email:invalidSyntax:${params.email}")

                flash.errorRestorePassword = g.message(code: 'customUserTasks.sendEmail.invalid',
                        default: '{0} email entered is invalid.', args: [params.email])

            } else { // Not exist
                log.error("ForgotPassword():email:doesNotExist:${params.email}")

                // A success email is displayed to avoid the user enumeration attack
                flash.successRestorePassword = g.message(code: 'customUserTasks.sendEmail.success',
                        default: 'Notification processed. You will receive an email valid for 30 minutes with the instructions to follow to reset your password.')
            }
        }
        redirect uri: '/forgotPassword'
    }

    /**
     * It checks the token. If this is correct, the view to change the password is displayed.
     *
     * @param token Token.
     * @return View If token is correct. If not error page is displayed.
     */
    def changePass(String token, Boolean newPasswordAgain) {
        log.debug("CustomUserTasksController:changePass()")

        if (newPasswordAgain) {
            render view: '/login/newPassword'

        } else {
            if (customUserTasksService.check_token(token, 'restorePassword')) {
                render view: '/login/newPassword'
            } else {
                response.sendError(404)
            }
        }
    }

    /**
     * It checks that token is correct and updates the password if it satisfies the rules.
     *
     * @return View Displaying the success or failure of the password update.
     */
    @Transactional(readOnly = false)
    updatePass(){
        log.debug("CustomUserTasksController:updatePass()")

        if(customUserTasksService.check_token(params.token, 'restorePassword')){ // It checks again the integrity of the token

            // Back-end validation - Password with maxlength
            if (params.password.length() > 32) {

                flash.errorNewPassword = g.message(code: 'default.myProfile.password.new.match',
                        default: '<strong>New password</strong> field does not match with the required pattern.')
                redirect uri: '/newPassword', params: [token: params.token, newPasswordAgain: true]
                return
            }

            // Back-end validation - Confirm password
            if (!StringUtils.isNotBlank(params.passwordConfirm)) {

                flash.errorNewPassword = g.message(code: 'default.password.confirm',
                        default: '<strong>Confirm password</strong> field cannot be null.')
                redirect uri: '/newPassword', params: [token: params.token, newPasswordAgain: true]
                return
            }

            def update_user = customUserTasksService.update_pass(params) // Password validation

            if(update_user.response){ // Response is true
                log.debug("CustomTasksUserController:updatePass():successful")

                flash.newPasswordSuccessful = g.message(code: 'views.login.auth.newPassword.successful',
                        default: 'New password set correctly.')

                redirect uri: '/'
                return
            }

            if (!update_user.valid) { // Invalid password
                log.debug("CustomTasksUserController:updatePass():invalidPassword")

                flash.errorNewPassword = g.message(code: 'default.myProfile.password.new.match',
                        default: '<strong>New password</strong> field does not match with the required pattern.')

            } else if (!update_user.match) { // Password not equal that passwordConfirm field
                log.debug("CustomTasksUserController:updatePass():passwordIsDifferent")

                flash.errorNewPassword = g.message(code: 'customUserTasks.updatePassword.differentPassword',
                        default: 'The passwords you entered do not match.')

            } else if (!update_user.passwordSame) { // Password is not different than the previous
                log.debug("CustomTasksUserController:updatePass():passwordIsEqualPrevious")

                flash.errorNewPassword = g.message(code: 'customUserTasks.updatePassword.equalPassword',
                        default: 'The password you entered can not be the same as the current.')

            } else { // Password is equal to username
                log.debug("CustomTasksUserController:updatePass():passwordIsEqualToUsername")

                flash.errorNewPassword = g.message(code: 'default.password.username',
                        default: '<strong>Password</strong> field must not be equal to username.')
            }

        }else{ // Token altered
            log.debug("CustomTasksUserController:updatePass():tokenAltered")

            flash.errorNewPassword = g.message(code: 'customUserTasks.updatePassword.invalidToken',
                    default: 'Invalid security token. Please, you enter again your email to send a new email.')
        }
        redirect uri: '/newPassword', params: [token: params.token, newPasswordAgain: true]
    }
}