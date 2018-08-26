package UserPage

import grails.plugin.springsecurity.SpringSecurityService

/**
 * It contains tasks of the normal user.
 */
class UserPageController {

    SpringSecurityService springSecurityService
    def cloudantDBService

    /**
     * It shows the home page of the user.
     */
    def home() {
        log.debug("UserPageController():home()")

        // Query to Cloudant NoSQL DB
        def totalMeasurements = cloudantDBService.getAllDocsUser(springSecurityService.principal.username).size()

        render view: 'home', model: [totalMeasurements: totalMeasurements]
    }
}
