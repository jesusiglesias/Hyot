package UserPage

import grails.gorm.transactions.Transactional
import User.User
import grails.converters.JSON
import grails.plugin.springsecurity.SpringSecurityService
import groovy.json.JsonSlurper
import org.apache.commons.lang.StringUtils

/**
 * It contains tasks of the normal user.
 */
class UserPageController {

    SpringSecurityService springSecurityService
    def passwordEncoder
    def cloudantDBService
    def hyperledgerFabricService

    // Mime-types allowed in image
    private static final contentsType = ['image/png', 'image/jpeg', 'image/gif']

    static allowedMethods = [updatePersonalInfo: "PUT", updateAvatar: "POST", updatePassword: "PUT"]

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
     * Gets the own measurements.
     */
    def myMeasurements () {

        def mymeasurements = cloudantDBService.getAllDocsUser(springSecurityService.principal.username)

        render view: 'mymeasurements', model: [mymeasurements: mymeasurements]
    }

    /**
     * Gets the own alerts.
     */
    def myalerts () {

        def myalerts = hyperledgerFabricService.getAlertsUser(springSecurityService.principal.username)

        render view: 'myalerts', model: [myalerts: new JsonSlurper().parseText(myalerts)]
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

    /**
     * It shows the profile of the current user.
     */
    def profile() {
        log.debug("UserPageController():profile()")

        // ID of current user
        def currentUser = User.get(springSecurityService.currentUser?.id)

        render view: 'profile', model: [infoCurrentUser: currentUser, currentUser: currentUser]
    }

    /**
     * It updates the profile of the current normal user.
     *
     * @return return If the current user instance is null or has errors.
     */
    @Transactional
    updatePersonalInfo() {
        log.debug("UserPageController():updatePersonalInfo()")

        def infoCurrentUser

        // User with params received
        def user = new User(params)

        // It obtains the current user
        User currentUserInstance = User.get(springSecurityService.currentUser?.id)
        bindData(currentUserInstance, this.params, [exclude:['version', 'username']])

        // Not found
        if (user == null) {

            // Roll back in database
            transactionStatus.setRollbackOnly()

            notFound()
            return
        }

        // It checks concurrent updates
        if (params.version) {
            def version = params.version.toLong()

            if (currentUserInstance.version > version) {

                // Roll back in database
                transactionStatus.setRollbackOnly()

                // Clear the list of errors
                currentUserInstance.clearErrors()
                flash.userProfileErrorMessage = g.message(code:"default.optimistic.locking.failure.userProfile",
                        default:"While you were editing, this user has been update from another device or browser. You try it again later.")

                redirect uri: "/profile"
                return
            }
        }

        // Validate the instance
        if (!currentUserInstance.validate()) {

            // Roll back in database
            transactionStatus.setRollbackOnly()

            // It obtains the original data of the user
            User.withNewSession {
                infoCurrentUser = User.get(springSecurityService.currentUser?.id)
            }

            respond currentUserInstance.errors, view:'profile', model: [infoCurrentUser: infoCurrentUser, currentUser: currentUserInstance]
            return
        }

        try {

            // Save user data
            currentUserInstance.save(flush:true, failOnError: true)

            request.withFormat {
                form multipartForm {
                    flash.userProfileMessage = g.message(code: 'default.myProfile.personalInfo.success', default: 'Your personal information has been successfully updated.')
                    redirect uri: '/profile'
                }
            }
        } catch (Exception exception) {
            log.error("UserPageController():update():Exception:NormalUser:${currentUserInstance.username}:${exception}")

            // Roll back in database
            transactionStatus.setRollbackOnly()

            request.withFormat {
                form multipartForm {
                    flash.userProfileErrorMessage = g.message(code: 'default.myProfile.personalInfo.error', default: 'ERROR! While updating your personal information.')
                    redirect uri: '/profile'
                }
            }
        }
    }

    /**
     * It renders the not found message if the user instance was not found.
     */
    protected void notFound() {
        log.debug("UserPageController():updateProfile:notFound():CurrentUser:${springSecurityService.currentUser?.username}")

        request.withFormat {
            form multipartForm {
                flash.userProfileErrorMessage = g.message(code: 'default.not.found.userProfile.message',
                        default:'It has not been able to locate the user.')
                redirect action: "profile", method: "GET"
            }
            '*'{ render status: NOT_FOUND }
        }
    }

    /**
     * It shows the password page of the current user.
     */
    def profilePassword() {
        log.debug("UserPageController():profilePassword()")

        // ID of current user
        def currentUser = User.get(springSecurityService.currentUser?.id)

        render view: 'profilePassword', model: [currentUser: currentUser]
    }

    /**
     * It updates the password of the current normal user.
     *
     * @return return If the current user instance is null or has errors.
     */
    @Transactional
    updatePassword() {
        log.debug("UserPageController():updatePassword()")

        def pattern = "^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=\\S+\$).{8,}\$"

        // User with params received
        def user = new User(params)

        // Not found
        if (user == null) {

            // Roll back in database
            transactionStatus.setRollbackOnly()

            notFoundPassword()
            return
        }

        // Back-end validation - Current password
        if (!StringUtils.isNotBlank(params.currentPassword)) {

            flash.userProfilePasswordErrorMessage = g.message(code: 'default.myProfile.password.current',
                    default: '<strong>Current password</strong> field is required.')
            redirect uri: "/profilePassword"
            return
        }

        // It obtains the current user
        User currentUserInstance = User.get(springSecurityService.currentUser?.id)

        // Back-end validation - Current password and password in database
        if (!passwordEncoder.isPasswordValid(currentUserInstance.password, params.currentPassword, null)) {

            flash.userProfilePasswordErrorMessage = g.message(code: 'default.myProfile.password.current.match',
                    default: '<strong>Current password</strong> field does not match with your password in force.')
            redirect uri: "/profilePassword"
            return
        }

        // Back-end validation - New password
        if (!StringUtils.isNotBlank(params.password)) {

            flash.userProfilePasswordErrorMessage = g.message(code: 'default.myProfile.password.new',
                    default: '<strong>New password</strong> field is required.')
            redirect uri: "/profilePassword"
            return
        }

        // Back-end validation - New password matches with pattern and maxlength
        if (!params.password.matches(pattern) || params.password.length() > 32) {

            flash.userProfilePasswordErrorMessage = g.message(code: 'default.myProfile.password.new.match',
                    default: '<strong>New password</strong> field does not match with the required pattern.')
            redirect uri: "/profilePassword"
            return
        }

        // Back-end validation - New password different to username
        if (params.password.toLowerCase().equals(currentUserInstance.username.toLowerCase())) {

            flash.userProfilePasswordErrorMessage = g.message(code: 'default.myProfile.password.notUsername',
                    default: '<strong>New password</strong> field must not be equal to username.')
            redirect uri: "/profilePassword"
            return
        }

        // Back-end validation - Confirm password
        if (!StringUtils.isNotBlank(params.confirmPassword)) {

            flash.userProfilePasswordErrorMessage = g.message(code: 'default.myProfile.password.confirm',
                    default: '<strong>Confirm password</strong> field is required.')
            redirect uri: "/profilePassword"
            return
        }

        // Back-end validation - New password and confirm password equals
        if (!params.password.equals(params.confirmPassword)) {

            flash.userProfilePasswordErrorMessage = g.message(code: 'default.myProfile.password.confirm.match.newPassword',
                    default: '<strong>New password</strong> and <strong>Confirm password</strong> fields must match.')
            redirect uri: "/profilePassword"
            return
        }

        // Bind data
        bindData(currentUserInstance, this.params, [include: ['password', 'confirmPassword']])

        // It checks concurrent updates
        if (params.version) {
            def version = params.version.toLong()

            if (currentUserInstance.version > version) {

                // Roll back in database
                transactionStatus.setRollbackOnly()

                // Clear the list of errors
                currentUserInstance.clearErrors()
                flash.userProfilePasswordErrorMessage = g.message(code: 'default.optimistic.locking.failure.userProfile',
                        default: 'While you were editing, this user has been update from another device or browser. You try it again later.')

                redirect uri: "/profilePassword"
                return
            }
        }

        try {

            // Update profile image
            currentUserInstance.save(flush: true, failOnError: true)

            request.withFormat {
                form multipartForm {
                    flash.userProfilePasswordMessage = g.message(code: 'default.myProfile.password.success',
                            default: 'Your password has been successfully updated.')
                    redirect uri: '/profilePassword'
                }
            }

        } catch (Exception exception) {
            log.error("UserPageController():updatePassword():Exception:NormalUser:${currentUserInstance.username}:${exception}")

            // Roll back in database
            transactionStatus.setRollbackOnly()

            request.withFormat {
                form multipartForm {
                    flash.userProfilePasswordErrorMessage = g.message(code: 'default.myProfile.password.error',
                            default: 'ERROR! While updating your password.')
                    redirect uri: "/profilePassword"
                }
            }
        }
    }

    /**
     * It renders the not found message if the user instance was not found.
     */
    protected void notFoundPassword() {
        log.debug("UserPageController():updateProfile:notFoundPassword():CurrentUser:${springSecurityService.currentUser?.username}")

        request.withFormat {
            form multipartForm {
                flash.userProfilePasswordErrorMessage = g.message(code: 'default.not.found.userProfile.message',
                        default:'It has not been able to locate the user.')
                redirect action: "profilePassword", method: "GET"
            }
            '*'{ render status: NOT_FOUND }
        }
    }

    /**
     * It shows the image of profile page of the current user.
     */
    def profileAvatar() {
        log.debug("UserPageController():profileAvatar()")

        // ID of current user
        def currentUser = User.get(springSecurityService.currentUser?.id)

        render view: 'profileAvatar', model: [currentUser: currentUser]
    }

    /**
     * It updates the profile image of the current normal user.
     *
     * @return return If the current user instance is null or has errors.
     */
    @Transactional
    updateAvatar() {
        log.debug("UserPageController():updateAvatar()")

        // User with params received
        def user = new User(params)

        // Not found
        if (user == null) {

            // Roll back in database
            transactionStatus.setRollbackOnly()

            notFoundAvatar()
            return
        }

        // Get the avatar file from the multi-part request
        def filename = request.getFile('avatarUser')

        // It checks that mime-types is correct: ['image/png', 'image/jpeg', 'image/gif']
        if (!filename.empty && !contentsType.contains(filename.getContentType())) {

            flash.userProfileAvatarErrorMessage = g.message(code: 'default.validation.mimeType.image',
                    default: 'The profile image must be of type: <strong>.png</strong>, <strong>.jpeg</strong> or <strong>.gif</strong>.')
            redirect uri: "/profileAvatar"
            return
        }

        // It obtains the current user
        User currentUserInstance = User.get(springSecurityService.currentUser?.id)

        // Update the image and mime type
        currentUserInstance.avatar = filename.bytes
        currentUserInstance.avatarType = filename.contentType

        // It checks concurrent updates
        if (params.version) {
            def version = params.version.toLong()

            if (currentUserInstance.version > version) {

                // Roll back in database
                transactionStatus.setRollbackOnly()

                // Clear the list of errors
                currentUserInstance.clearErrors()
                flash.userProfileAvatarErrorMessage = g.message(code: 'default.optimistic.locking.failure.userProfile',
                        default: 'While you were editing, this user has been update from another device or browser. You try it again later.')

                redirect uri: "/profileAvatar"
                return
            }
        }

        // Validate the instance
        if (!currentUserInstance.validate()) {

            respond currentUserInstance.errors, view:'profileAvatar', model: [currentUser: currentUserInstance]
            return
        }

        try {

            // Update profile image
            currentUserInstance.save(flush:true, failOnError: true)

            request.withFormat {
                form multipartForm {
                    flash.userProfileAvatarMessage = g.message(code: 'default.myProfile.avatar.success', default: 'Your profile image has been updated successfully.')
                    redirect uri: '/profileAvatar'
                }
            }

        } catch (Exception exception) {
            log.error("UserPageController():updateAvatar():Exception:NormalUser:${currentUserInstance.username}:${exception}")

            // Roll back in database
            transactionStatus.setRollbackOnly()

            request.withFormat {
                form multipartForm {
                    flash.userProfileAvatarErrorMessage = g.message(code: 'default.myProfile.avatar.error', default: 'ERROR! While updating your profile image.')
                    redirect uri: "/profileAvatar"
                }
            }
        }
    }

    /**
     * It renders the not found message if the user instance was not found.
     */
    protected void notFoundAvatar() {
        log.debug("UserPageController():updateProfile:notFoundAvatar():CurrentUser:${springSecurityService.currentUser?.username}")

        request.withFormat {
            form multipartForm {
                flash.userProfileAvatarErrorMessage = g.message(code: 'default.not.found.userProfile.message', default:'It has not been able to locate the user.')
                redirect action: "profileAvatar", method: "GET"
            }
            '*'{ render status: NOT_FOUND }
        }
    }
}
