package UserPage

import grails.converters.JSON
import grails.plugin.springsecurity.SpringSecurityService

/**
 * It contains tasks of the normal user.
 */
class UserPageController {

    SpringSecurityService springSecurityService
    def cloudantDBService
    def hyperledgerFabricService

    /**
     * It shows the home page of the user.
     */
    def home() {
        log.debug("UserPageController():home()")

        // Query to Cloudant NoSQL DB
        def totalMeasurements = cloudantDBService.getAllDocsUser(springSecurityService.principal.username).size()

        // Query to the Blockchain
        def totalAlerts = hyperledgerFabricService.countAlertsUser(springSecurityService.principal.username)

        render view: 'home', model: [totalMeasurements: totalMeasurements, totalAlerts: totalAlerts]
    }


    /**
     * It obtains the number of measurements registered in Cloudant NoSQL DB for the user.
     */
    def reloadMymeasurement() {
        log.debug("UserPageController:reloadMymeasurement()")

        render cloudantDBService.getAllDocsUser(springSecurityService.principal.username).size()

    }

    /**
     * It obtains the number of alerts registered in the BC for the user.
     */
    def reloadMyalert() {
        log.debug("UserPageController:reloadMyalert()")

        render hyperledgerFabricService.countAlertsUser(springSecurityService.principal.username)
    }

    /**
     * It obtains the number of alerts of an user triggered by each sensor.
     */
    def myalertBySensor() {
        log.debug("UserPageController:myalertBySensor()")

        def totalMyalertsSensorDHT11 = hyperledgerFabricService.countAlertsSensorUser(springSecurityService.principal.username, 'DHT11')
        def totalMyalertsSensorHCSR04 = hyperledgerFabricService.countAlertsSensorUser(springSecurityService.principal.username, 'HCSR04')

        def data = [
                'dht': totalMyalertsSensorDHT11,
                'hcsr': totalMyalertsSensorHCSR04,
        ]

        // Avoid undefined function (Google chart)
        sleep(100)

        render data as JSON
    }

    /**
     * It obtains the number of alerts of an user triggered by each event.
     */
    def myalertByEvent() {
        log.debug("UserPageController:myalertByEvent()")

        def totalAlertsEventTEMPERATURE = hyperledgerFabricService.countAlertsEventUser(springSecurityService.principal.username, 'TEMPERATURE')
        def totalAlertsEventHUMIDITY = hyperledgerFabricService.countAlertsEventUser(springSecurityService.principal.username, 'HUMIDITY')
        def totalAlertsEventDISTANCE = hyperledgerFabricService.countAlertsEventUser(springSecurityService.principal.username, 'DISTANCE')

        def data = [
                'temperature': totalAlertsEventTEMPERATURE,
                'humidity': totalAlertsEventHUMIDITY,
                'distance': totalAlertsEventDISTANCE,
        ]

        // Avoid undefined function (Google chart)
        sleep(100)

        render data as JSON
    }
}
