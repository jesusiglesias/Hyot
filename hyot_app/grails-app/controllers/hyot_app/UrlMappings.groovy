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

        /* Domain URLS
        ======================================================*/
        // Admin group
        group("/administrator") {
            "/"(controller: 'secUser', action: 'index')
            "/create"(controller: 'secUser', action: 'create')
            "/create-error"(controller: 'secUser', action: 'save')
            "/edit/$id?(.$format)?"(controller: 'secUser', action: 'edit')
            "/edit-error/$id?(.$format)?"(controller: 'secUser', action: 'update')
            "/edit/profileImage/$id?(.$format)?"(controller: 'secUser', action: 'editProfileImage')
            "/edit-error/profileImage/$id?(.$format)?"(controller: 'secUser', action: 'updateProfileImage')
        }

        // User - Grouping URLs
        group("/user") {
            "/"(controller: 'user', action: 'index')
            "/create"(controller: 'user', action: 'create')
            "/create-error"(controller: 'user', action: 'save')
            "/edit/$id?(.$format)?"(controller: 'user', action: 'edit')
            "/edit-error/$id?(.$format)?"(controller: 'user', action: 'update')
            "/edit/profileImage/$id?(.$format)?"(controller: 'user', action: 'editProfileImage')
            "/edit-error/profileImage/$id?(.$format)?"(controller: 'user', action: 'updateProfileImage')
        }

        /* General tasks of unregistered user
        ======================================================*/
        // LoggedIn
        "/login/loggedIn"(controller: 'customUserTasks', action: 'loggedIn')
        // Fail authentication
        "/authFail"(controller: 'customUserTasks', action: 'authFail')
        // Restore password
        "/forgotPassword"(controller: 'customUserTasks', action: 'restorePassword')
        // Change password
        "/newPassword"(controller: 'customUserTasks', action: 'changePass')
        // User without role
        "/noRole"(view: '/login/noRole')

        /* General tasks of administrator
        ======================================================*/
        "/dashboard"(controller: 'controlPanel', action: 'dashboard')
        "/alert"(controller: 'alert', action: 'getAllAlerts')
        "/measurement"(controller: 'measurement', action: 'getAllMeasurements')

        /* General tasks of the normal user
        ======================================================*/
        "/home"(controller: 'userPage', action: 'home')
        "/mymeasurements"(controller: 'userPage', action: 'myMeasurements')
        "/myalerts"(controller: 'userPage', action: 'myalerts')
        "/profile"(controller: 'userPage', action: 'profile')
        "/profile-error"(controller: 'userPage', action: 'updatePersonalInfo')
        "/profilePassword"(controller: 'userPage', action: 'profilePassword')
        "/profilePassword-error"(controller: 'userPage', action: 'profilePassword')
        "/profileAvatar"(controller: 'userPage', action: 'profileAvatar')
        "/profileAvatar-error"(controller: 'userPage', action: 'updateAvatar')

        /* Information files
        ======================================================*/
        // Humans.txt
        "/humans.txt"(view: '/extraInformation/humans')
        // Robots.txt
        "/robots.txt"(view: '/extraInformation/robots')

        /* Errors
        ======================================================*/
        "400"(view: '/error/badRequest')
        "401"(view: '/error/unauthorized')
        "403"(view: '/error/denied')
        "404"(view: '/error/notFound')
        "405"(view: '/error/notAllowed')
        "500"(view: '/error/internalError')
        "503"(view: '/error/unavailableService')
    }
}