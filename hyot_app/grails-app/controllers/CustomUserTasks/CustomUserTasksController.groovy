package CustomUserTasks

import grails.gorm.transactions.Transactional
import org.springframework.beans.factory.annotation.Value
import grails.plugin.springsecurity.SpringSecurityUtils
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

    static allowedMethods = [sendEmail: "POST", updatePass: "POST"] // TODO

    def customUserTasksService

    // Obtain the default url of users
    @Value('${springsecurity.urlredirection.admin}')
            adminUrlRedirection
    @Value('${springsecurity.urlredirection.user}')
            userUrlRedirection

    /**
     * It obtains the default URL redirection based on role from the call successHandler.defaultTargetUrl.
     *
     * @return urlRedirection URL to redirection to the user.
     */
    def loggedIn() {
        log.debug("CustomUserTasksController:loggedIn()")

        // Redirection to admin url
        if (SpringSecurityUtils.ifAllGranted('ROLE_ADMIN')) {
            log.debug("CustomUserTasksController:loggedIn():adminRole")
            redirect uri: adminUrlRedirection

        } else if (SpringSecurityUtils.ifAllGranted('ROLE_USER')) {  // Redirection to user url
            log.debug("CustomUserTasksController:loggedIn():userRole")
            redirect uri: userUrlRedirection
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
}