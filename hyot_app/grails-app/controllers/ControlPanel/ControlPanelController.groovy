package ControlPanel

import Security.*
import grails.converters.JSON
import groovy.json.JsonSlurper
import org.grails.core.io.ResourceLocator
import org.springframework.core.io.Resource

/**
 * It contains the habitual custom tasks of the admin (control panel).
 */
class ControlPanelController {

    def springSecurityService
    def hyperledgerFabricService
    ResourceLocator grailsResourceLocator

    /**
     * It shows the main page of the admin user.
     */
    def dashboard() {
        log.debug("ControlPanelController:dashboard()")

        // It obtains the number of normal users
        def roleUser = SecRole.findByAuthority("ROLE_USER")
        def normalUsers = SecUserSecRole.findAllBySecRole(roleUser).secUser

        // It obtains the number of admin users
        def roleAdminUser = SecRole.findByAuthority("ROLE_ADMIN")
        def adminUsers = SecUserSecRole.findAllBySecRole(roleAdminUser).secUser

        // Queries to the Blockchain
        def totalAlerts = hyperledgerFabricService.countAlerts()
        def totalUsers = hyperledgerFabricService.countUsers()

        // It obtains the the last 10 registered users
        def lastUsers = SecUser.executeQuery("from SecUser where id in (select secUser.id from SecUserSecRole where secRole.id = :roleId) order by dateCreated desc", [roleId: roleUser.id], [max: 10])

        render view: 'dashboard', model: [normalUsers: normalUsers.size(), adminUsers: adminUsers.size(),
                                          totalAlerts: totalAlerts, totalUsers: totalUsers, lastUsers: lastUsers]
    }

    /**
     * It obtains the number of users from the AJAX call.
     */
    def reloadNormalUser() {
        log.debug("ControlPanelController:reloadUsers()")

        def roleUser = SecRole.findByAuthority("ROLE_USER")
        def normalUsers = SecUserSecRole.findAllBySecRole(roleUser).secUser

        render normalUsers.size()
    }

    /**
     * It obtains the number of admin users from the AJAX call.
     */
    def reloadAdmin() {
        log.debug("ControlPanelController:reloadAdmin()")

        def roleAdminUser = SecRole.findByAuthority("ROLE_ADMIN")
        def adminUsers = SecUserSecRole.findAllBySecRole(roleAdminUser).secUser

        render adminUsers.size()
    }

    /**
     * It obtains the lastest 10 registered users from the AJAX call.
     */
    def reloadLastUsers() {
        log.debug("ControlPanelController:reloadLastUsers()")

        def roleUser = SecRole.findByAuthority("ROLE_USER")

        // Obtaining the last 10 registered users
        def lastUsers = SecUser.executeQuery("from SecUser where id in (select secUser.id from SecUserSecRole where secRole.id = :roleId) order by dateCreated desc", [roleId: roleUser.id], [max: 10])

        render(template:'lastUsers', model: [lastUsers: lastUsers])
    }

    /**
     * It obtains the number of alerts registered in the BC.
     */
    def reloadAlert() {
        log.debug("ControlPanelController:reloadAlert()")

        render hyperledgerFabricService.countAlerts()
    }

    /**
     * It obtains the number of users registered in the BC.
     */
    def reloadUserBC() {
        log.debug("ControlPanelController:reloadUserBC()")

        render hyperledgerFabricService.countUsers()
    }


    /**
     * It obtains the number of alerts triggered by each sensor.
     */
    def alertBySensor() {
        log.debug("ControlPanelController:alertBySensor()")

        def totalAlertsSensorDHT11 = hyperledgerFabricService.countAlertsDHT11()
        def totalAlertsSensorHCSR04 = hyperledgerFabricService.countAlertsHCSR04()

        def data = [
                'dht': totalAlertsSensorDHT11,
                'hcsr': totalAlertsSensorHCSR04,
        ]

        // Avoid undefined function (Google chart)
        sleep(100)

        render data as JSON
    }

    /**
     * It obtains the number of alerts triggered by each event.
     */
    def alertByEvent() {
        log.debug("ControlPanelController:alertByEvent()")

        def totalAlertsEventTEMPERATURE = hyperledgerFabricService.countAlertsTemperature()
        def totalAlertsEventHUMIDITY = hyperledgerFabricService.countAlertsHumidity()
        def totalAlertsEventDISTANCE = hyperledgerFabricService.countAlertsDistance()

        def data = [
                'temperature': totalAlertsEventTEMPERATURE,
                'humidity': totalAlertsEventHUMIDITY,
                'distance': totalAlertsEventDISTANCE,
        ]

        // Avoid undefined function (Google chart)
        sleep(100)

        render data as JSON
    }

    /**
     * It obtains the number of measurements and alerts of an user.
     */
    def measurementAlertByUser() {
        log.debug("ControlPanelController:measurementAlertByUser()")

        def measurementAlertMap = [[g.message(code: 'layouts.main_auth_admin.controller.datatable.user', default:'User'),
                                    g.message(code: 'layouts.main_auth_admin.controller.datatable.measurements', default:'Number of measurements'),
                                    g.message(code: 'layouts.main_auth_admin.controller.datatable.alerts', default:'Number of alerts'),
                                   ]]

        // It obtains all users
        def users = hyperledgerFabricService.getUsers()

        // It parses the users
        def userList = new JsonSlurper().parseText(users)

        // Number of measurements and alerts for each user
        userList.each { // TODO
            measurementAlertMap.push([it.username, 17, hyperledgerFabricService.countAlertsUser(it.username)])
        }

        // Avoid undefined function (Google chart)
        sleep(100)

        render measurementAlertMap as JSON
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
