package ControlPanel

import groovy.json.JsonSlurper

/**
 * It contains actions about alerts for the administrator user.
 */
class AlertController {

    def hyperledgerFabricService

    /**
     * It gets all alerts and shows them to the administrator user.
     */
    def getAllAlerts() {
        log.debug("AlertController:getAllAlerts()")

        def allAlerts = hyperledgerFabricService.getAlerts()

        render view: '/controlPanel/alerts', model: [alerts: new JsonSlurper().parseText(allAlerts)]
    }
}
