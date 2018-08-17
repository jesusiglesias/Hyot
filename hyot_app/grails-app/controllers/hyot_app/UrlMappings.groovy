package hyot_app

/*-------------------------------------------------------------------------------------------*
 *                                      URL MAPPINGS                                         *
 *-------------------------------------------------------------------------------------------*/

/**
 * Configuration of the URL mapping.
 */
class UrlMappings {

    static mappings = {
        "/$controller/$action?/$id?(.$format)?" {
            constraints {
                // apply constraints here
            }
        }

        // Homepage
        "/"(controller: 'login', action: 'auth')
    }
}