/*-------------------------------------------------------------------------------------------*
 *                                      URL MAPPINGS                                         *
 *-------------------------------------------------------------------------------------------*/

package hyot_app

/**
 * Configuration of the URL mapping.
 */
class UrlMappings {

    static mappings = {
        "/$controller/$action?/$id?(.$format)?" {
            constraints {
            }
        }

        // Homepage
        "/"(controller: 'login', action: 'auth')

        /* General tasks of unregistered user
        ======================================================*/
        // LoggedIn
        "/login/loggedIn"(controller: 'customUserTasks', action: 'loggedIn')
        // Fail authentication
        "/authFail"(controller: 'customUserTasks', action: 'authFail')
        /* Errors
        ======================================================*/
        "400"(view: '/error/badRequest')
        "401"(view: '/error/unauthorized')
        "403"(view: '/login/denied')
        "404"(view: '/error/notFound')
        "405"(view: '/error/notAllowed')
        "500"(view: '/error/internalError')
        "503"(view: '/error/unavailableService')
    }
}