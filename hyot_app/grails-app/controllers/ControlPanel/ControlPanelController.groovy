package ControlPanel

import Security.*
import org.grails.core.io.ResourceLocator
import org.springframework.core.io.Resource

/**
 * It contains the habitual custom tasks of the admin (control panel).
 */
class ControlPanelController {

    def springSecurityService
    ResourceLocator grailsResourceLocator

    /**
     * It shows the main page of the admin user.
     */
    def dashboard() {
        log.debug("ControlPanelController:dashboard()")

        // Obtaining number of normal users
        def roleUser = SecRole.findByAuthority("ROLE_USER")
        def normalUsers = SecUserSecRole.findAllBySecRole(roleUser).secUser

        // Obtaining number of admin users
        def roleAdminUser = SecRole.findByAuthority("ROLE_ADMIN")
        def adminUsers = SecUserSecRole.findAllBySecRole(roleAdminUser).secUser

        // Obtaining the lastest 10 registered users
        def lastUsers = SecUser.executeQuery("from SecUser where id in (select secUser.id from SecUserSecRole where secRole.id = :roleId) order by dateCreated desc", [roleId: roleUser.id], [max: 10])

        render view: 'dashboard', model: [normalUsers: normalUsers.size(), adminUsers: adminUsers.size(), lastUsers: lastUsers]
    }

    /**
     * It obtains the profile image.
     *
     * @return out Profile image of the user.
     */
    def profileImage() {
        log.debug("ControlPanelController:profileImage()")

        def currentUser

        if (params.id) { // Index view
            currentUser = SecUser.get(params.id)

        } else { // Menu
            currentUser = SecUser.get(springSecurityService.currentUser?.id)
        }

        if (!currentUser || !currentUser.avatar || !currentUser.avatarType) {

            final Resource image = grailsResourceLocator.findResourceForURI('/img/profile/user_profile.png')

            def file = new File(image.getURL().getFile())
            def img = file.bytes
            response.contentType = 'image/png'
            response.contentLength = file.size()
            response.outputStream << img
            response.outputStream.flush()

        } else {

            response.contentType = currentUser.avatarType
            response.contentLength = currentUser.avatar.size()
            OutputStream out = response.outputStream
            out.write(currentUser.avatar)
            out.close()
        }
    }
}
