/*-------------------------------------------------------------------------------------------*
 *                                         BOOTSTRAP                                         *
 *-------------------------------------------------------------------------------------------*/

package hyot_app

import grails.util.Environment
import Security.*
import User.*

/**
 * Configuration during startup and destruction of the application.
 */
class BootStrap {

    def verificationCertificateService

    /**
     * Initial operations when starting application.
     */
    def init = { servletContext ->


        // Skips the validation of the certificate in the requests to the Blockchain (fail with self-signed certificate)
        verificationCertificateService.skipValidation()

        // Populating the database depending on the environment
        switch (Environment.current) {
            case Environment.DEVELOPMENT:
                createInitialData()
                break
            case Environment.TEST:
                createInitialData()
                break
            case Environment.PRODUCTION:
                createInitialData()
                break
        }
    }

    /**
     * Final operations when finishing application.
     */
    def destroy = {
    }

    /**
     * Populating the database.
     */
    void createInitialData() {
        log.debug("BootStrap:init():createInitialData()")

        // It checks the existence of data
        if (!SecUser.count() && !SecRole.count()) {

            /*-------------------------------------------------------------------------------------------*
             *                                        ADMIN AND ROLE                                     *
             *-------------------------------------------------------------------------------------------*/

            // Role
            def adminRole = SecRole.findByAuthority('ROLE_ADMIN') ?: new SecRole(authority: 'ROLE_ADMIN')
            def userRole = SecRole.findByAuthority('ROLE_USER') ?: new SecRole(authority: 'ROLE_USER')

            // Administrator user
            def adminUser = SecUser.findByUsername('hyot_admin') ?: new SecUser(
                    username: 'hyot_admin',
                    password: 'Qwerty321!',
                    email: 'hyot.project@gmail.com')

            // TODO Eliminar usuario normal para la demo y entrega final
            /*-------------------------------------------------------------------------------------------*
             *                                          USER                                             *
             *-------------------------------------------------------------------------------------------*/

            // Normal user
            def normalUser = User.findByUsername('hyot') ?: new User( // Normal user
                    username: 'hyot',
                    password: 'Qwerty321!',
                    email: 'jesus.iglesiasg@estudiante.uam.es',
                    name: 'Jesús',
                    surname: 'Iglesias'
            )

            /*-------------------------------------------------------------------------------------------*
             *                                        VALIDATION                                         *
             *-------------------------------------------------------------------------------------------*/

            def validation_adminUser = adminUser.validate()
            def validation_normalUser = normalUser.validate()

            if (validation_adminUser & validation_normalUser) {

                // It saves the roles
                adminRole.save(flush: true, failOnError: true)
                userRole.save(flush: true, failOnError: true)

                // It saves the users
                adminUser.save(flush: true, failOnError: true)
                normalUser.save(flush: true, failOnError: true)

                // It assigns the role to the admin user
                if (!adminUser.authorities.contains(adminRole)) {
                    SecUserSecRole.create adminUser, adminRole, true
                }

                // It assigns the role to the normal user
                if (!normalUser.authorities.contains(userRole)) {
                    SecUserSecRole.create normalUser, userRole, true
                }

                log.debug("BootStrap:init():createInitialData():Initial data has been created")
                log.info("Configuration - Admin user: hyot_admin/Qwerty321!; Normal user: hyot/Qwerty321!")
            } else {
                log.error("BootStrap:init():createInitialData():Initial data has not been created. Verify the " +
                        "constraints of the data")
            }
        } else {
            log.warn("BooStrap:init():Initial data already exists")
        }
    }
}
