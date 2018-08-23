package HyperledgerFabric

import grails.gorm.transactions.Transactional
import groovy.json.JsonSlurper

/**
 * Service to make requests to the Blockchain of the Hyperledger Fabric.
 */
@Transactional
class HyperledgerFabricService {

    def grailsApplication
    def namespaceUser = "resource%3Aorg.hyot.network.User%23"

    /**
     * Gets the users.
     *
     * @return List of users.
     */
    def getUsers() {

        return new URL(grailsApplication.config.blockchain.get.users).getText(requestProperties: [Accept: 'application/json'])
    }

    /**
     * Gets the total alerts.
     *
     * @return Total number of the alerts.
     */
    def countAlerts() {

        return count(new URL(grailsApplication.config.blockchain.get.alerts).getText(requestProperties: [Accept: 'application/json']))
    }

    /**
     * Gets the total alerts triggered by DHT11 sensor.
     *
     * @return Total number of the alerts triggered by DHT11 sensor.
     */
    def countAlertsDHT11() {

        return count(new URL(grailsApplication.config.blockchain.get.alertsSensor.dht11).getText(requestProperties: [Accept: 'application/json']))
    }

    /**
     * Gets the total alerts triggered by HCSR04 sensor.
     *
     * @return Total number of the alerts triggered by HCSR04 sensor.
     */
    def countAlertsHCSR04() {

        return count(new URL(grailsApplication.config.blockchain.get.alertsSensor.hcsr04).getText(requestProperties: [Accept: 'application/json']))
    }

    /**
     * Gets the total alerts triggered by temperature event.
     *
     * @return Total number of the alerts triggered by temperature event.
     */
    def countAlertsTemperature() {

        return count(new URL(grailsApplication.config.blockchain.get.alertsEvent.temperature).getText(requestProperties: [Accept: 'application/json']))
    }

    /**
     * Gets the total alerts triggered by humidity event.
     *
     * @return Total number of the alerts triggered by humidity event.
     */
    def countAlertsHumidity() {

        return count(new URL(grailsApplication.config.blockchain.get.alertsEvent.humidity).getText(requestProperties: [Accept: 'application/json']))
    }

    /**
     * Gets the total alerts triggered by distance event.
     *
     * @return Total number of the alerts triggered by distance event.
     */
    def countAlertsDistance() {

        return count(new URL(grailsApplication.config.blockchain.get.alertsEvent.distance).getText(requestProperties: [Accept: 'application/json']))
    }

    /**
     * Gets the total alerts of a specific user.
     *
     * @return Total number of the alerts of an user.
     */
    def countAlertsUser(String username) {

        return count(new URL(grailsApplication.config.blockchain.get.alertsUser + namespaceUser + username).getText(requestProperties: [Accept: 'application/json']))
    }

    /**
     * Gets the total users.
     *
     * @return Total number of users.
     */
    def countUsers() {

        return count(new URL(grailsApplication.config.blockchain.get.users).getText(requestProperties: [Accept: 'application/json']))
    }

    /**
     * Counts the items.
     *
     * @param input Response of the request in JSON format.
     *
     * @return Number of items.
     */
    private count(input) {

        def json = new JsonSlurper().parseText(input)
        return json.size()
    }
}
