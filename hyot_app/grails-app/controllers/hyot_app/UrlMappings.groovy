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
    }
}