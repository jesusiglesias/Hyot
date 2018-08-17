package CustomUserTasks

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

    def customTasksUserService // TODO

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
        log.debug("CustomTasksUserController:loggedIn()")

        // Redirection to admin url
        if (SpringSecurityUtils.ifAllGranted('ROLE_ADMIN')) {
            log.debug("CustomTasksUserController:loggedIn():adminRole")
            redirect uri: adminUrlRedirection

        } else if (SpringSecurityUtils.ifAllGranted('ROLE_USER')) {  // Redirection to user url
            log.debug("CustomTasksUserController:loggedIn():userRole")
            redirect uri: userUrlRedirection
        }
    }

    /**
     * Callback after a failed login. Redirects to the "/" page with a warning message.
     *
     * @return failMessage Message to show to the user.
     */
    def authFail() {
        log.debug("CustomTasksUserController:authFail()")

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
                log.error("CustomTasksUserController:authFail():accountExpired:UserOrEmailIntroduced:${session['SPRING_SECURITY_LAST_USERNAME']}")

                messageType = "accountExpired"
                failMessage = g.message(code: "customUserTasks.login.expired",
                        default: 'Sorry, your user account has expired.')

            } else if (exception instanceof CredentialsExpiredException) {
                log.error("CustomTasksUserController:authFail():passwordExpired:UserOrEmailIntroduced:${session['SPRING_SECURITY_LAST_USERNAME']}")

                messageType = "passwordExpired"
                failMessage = g.message(code: "customUserTasks.login.passwordExpired",
                        default: 'Sorry, your password has expired.')

            } else if (exception instanceof DisabledException) {
                log.error("CustomTasksUserController:authFail():accountDisabled:UserOrEmailIntroduced:${session['SPRING_SECURITY_LAST_USERNAME']}")

                failDisabledMessage = g.message(code: "customUserTasks.login.disabled",
                        default: 'Sorry, your account is disabled. Contact with an administrator to enable it.')

            } else if (exception instanceof LockedException) {
                log.error("CustomTasksUserController:authFail():accountLocked:UserOrEmailIntroduced:${session['SPRING_SECURITY_LAST_USERNAME']}")

                messageType = "accountLocked"
                failMessage = g.message(code: "customUserTasks.login.locked",
                        default: 'Sorry, your user account has been locked by the administrator.')

            } else if (exception instanceof AuthenticationServiceException) {
                log.error("CustomTasksUserController:authFail():authenticationService")

                failAuthenticationMessage = g.message(code: "customUserTasks.login.authenticationException",
                        default: 'An internal error has occurred during log in.')

            } else if (exception instanceof SessionAuthenticationException){
                log.error("CustomTasksUserController:authFail():sessionAuthentication")

                failSessions = g.message(code: "customUserTasks.login.concurrentSessions",
                        default: 'Maximum sessions for this user exceeded. Limit: 1 session.')

            } else {
                log.debug("CustomTasksUserController:authFail():fail")

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
}