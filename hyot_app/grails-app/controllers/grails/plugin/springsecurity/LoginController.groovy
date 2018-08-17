package grails.plugin.springsecurity

import grails.converters.JSON
import javax.servlet.http.HttpServletResponse
import org.springframework.security.core.context.SecurityContextHolder as SCH

/**
 * Actions of login of the users.
 */
class LoginController {

    /**
     * Dependency injection for the authenticationTrustResolver.
     */
    def authenticationTrustResolver

    /**
     * Dependency injection for the springSecurityService.
     */
    def springSecurityService

    /**
     * Default action; redirects to 'defaultTargetUrl' if logged in, /login/auth otherwise.
     */
    def index() {
        // It checks if the user is logged
        if (springSecurityService.isLoggedIn()) {
            redirect uri: SpringSecurityUtils.securityConfig.successHandler.defaultTargetUrl
        }
        else {
            redirect action: 'auth', params: params
        }
    }

    /**
     * Show the login page.
     */
    def auth() {

        def config = SpringSecurityUtils.securityConfig

        // Check if the user is logged
        if (springSecurityService.isLoggedIn()) {
            redirect uri: config.successHandler.defaultTargetUrl
            return
        }

        String view = 'auth'
        String postUrl = "${request.contextPath}${config.apf.filterProcessesUrl}"
        render view: view, model: [postUrl: postUrl,
                                   rememberMeParameter: config.rememberMe.parameter]
    }

    /**
     * The redirect action for Ajax requests.
     */
    def authAjax() {
        response.setHeader 'Location', SpringSecurityUtils.securityConfig.auth.ajaxLoginFormUrl
        response.sendError HttpServletResponse.SC_UNAUTHORIZED
    }

    /**
     * Show denied page.
     */
    def denied() {
        log.debug("LoginController:denied()")

        if (springSecurityService.isLoggedIn() &&
                authenticationTrustResolver.isRememberMe(SCH.context?.authentication)) {

            // Have cookie but the page is guarded with IS_AUTHENTICATED_FULLY
            redirect uri: '/reauthenticate'
        }
    }

    /**
     * Login page for users with a remember-me cookie but accessing an IS_AUTHENTICATED_FULLY page.
     */
    def full() {
        log.debug("LoginController:full()")

        def config = SpringSecurityUtils.securityConfig

        // TODO
        flash.reauthenticate = g.message(code: "views.login.auth.warning.reauthentication", default: 'For security reasons, it is necessary to authenticate again to do this action.')

        render view: 'auth',
                model: [hasCookie: authenticationTrustResolver.isRememberMe(SCH.context?.authentication),
                        postUrl: "${request.contextPath}${config.apf.filterProcessesUrl}"]
    }

    /**
     * The Ajax success redirect url.
     */
    def ajaxSuccess() {
        render([success: true, username: springSecurityService.authentication.name] as JSON)
    }

    /**
     * The Ajax denied redirect url.
     */
    def ajaxDenied() {
        render([error: 'access denied'] as JSON)
    }
}
