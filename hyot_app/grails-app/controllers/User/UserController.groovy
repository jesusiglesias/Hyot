package User

import grails.gorm.transactions.Transactional
import org.springframework.beans.factory.annotation.Value
import Security.SecRole
import Security.SecUser
import Security.SecUserSecRole
import grails.converters.JSON
import org.apache.commons.lang.StringUtils
import org.springframework.dao.DataIntegrityViolationException
import static org.springframework.http.HttpStatus.*

/**
 * Class that represents to the User controller (actions for normal user).
 */
@Transactional(readOnly = true)
class UserController {

    static allowedMethods = [save: "POST", update: "PUT", updateProfileImage: 'POST', delete: "DELETE"]

    // Mime-types allowed in image
    private static final contentsType = ['image/png', 'image/jpeg', 'image/gif']

    // Default value of pagination
    @Value('${paginate.defaultValue:10}')
            defaultPag

    // URL to get the User with an ID
    @Value('${blockchain.get.userID}')
            blockchain_getUserID

    /**
     * It lists the main data of all normal users of the database.
     *
     * @param max Maximum number of normal users to list.
     * @return Users List of users with their information and number of normal users in the database.
     */
    def index(Integer max) {
        //params.max = Math.min(max ?: 10, 100)

        defaultPag=10

        // Protecting against attacks when max is a negative number. If is 0, max = defaultPag
        max = max ?: defaultPag.toInteger()
        // If max < 0, return all records (This is dangerous)
        if (max < 0) {
            max = defaultPag.toInteger()
        }
        params.max = Math.min(max, 100)

        respond User.list(params)
    }

    /**
     * It creates a new user instance.
     *
     * @return return If the user instance is null or has errors.
     */
    def create() {
        respond new User(params)
    }

    /**
     * It checks the username availability and if exists an User participant with this username in the Blockchain.
     */
    def checkUsernameAvailibilityAndBlockchain () {

        def responseData

        try {

            new URL(blockchain_getUserID + params.username).getText(requestProperties: [Accept: 'application/json'])

            if (SecUser.countByUsername(params.username)) { // Username found
                responseData = [
                        'status': "ERROR",
                        'message': g.message(code: 'secUser.checkUsernameAvailibility.notAvailable', default:'Username is not available. Please, choose another one.')
                ]
            } else { // Username not found
                responseData = [
                        'status': "OK",
                        'message':g.message(code: 'secUser.checkUsernameAvailibility.available', default:'Username available.')
                ]
            }

        } catch (FileNotFoundException exception) {
            log.error("UserController():checkUsernameAvailibilityAndBlockchain():Exception:NormalUserNotExistBlockchain:${exception}")

            responseData = [
                    'status': "ERROR",
                    'message': g.message(code: 'secUser.checkUsernameAvailibility.notAvailable.user.blockchain',
                            default:'Username does not exist in the Blockchain. Please, create this user before continuing.')
            ]
        } catch (ConnectException exception) {
            log.error("UserController():checkUsernameAvailibilityAndBlockchain():Exception:BlockchainNotAvailable:${exception}")

            responseData = [
                    'status': "ERROR",
                    'message': g.message(code: 'secUser.checkUsernameAvailibility.notAvailable.blockchain',
                            default:'Blockchain of Hyperledger Fabric is not available. Please, run the server before continuing.')
            ]
        }

        render responseData as JSON
    }

    /**
     * It saves a normal user in database.
     *
     * @param userInstance It represents the normal user to save.
     * @return return If the user instance is null or has errors.
     */
    @Transactional
    save(User userInstance) {

        if (userInstance == null) {

            // Roll back in database
            transactionStatus.setRollbackOnly()

            notFound()
            return
        }

        // Get the avatar file from the multi-part request
        def filename = request.getFile('avatar')

        // Back-end validation - Username in Blockchain
        def blockchainValidation = usernameBlockchainAndDBValidation(userInstance.username)

        // If value is 1 - Username found in BC and not found in DB (OK)
        // Username found in BC and DB
        if (blockchainValidation == 0) {
            flash.userErrorMessage = g.message(code: 'secUser.checkUsernameAvailibility.notAvailable',
                    default:'Username is not available. Please, choose another one.')
            render view: "create", model: [userInstance: userInstance]
            return

        } else if (blockchainValidation == 2) { // Username not found in BC
            flash.userErrorMessage = g.message(code: 'secUser.checkUsernameAvailibility.notAvailable.user.blockchain',
                    default:'Username does not exist in the Blockchain. Please, create this user before continuing.')
            render view: "create", model: [userInstance: userInstance]
            return

        } else if (blockchainValidation == 3) { // BC is not available
            flash.userErrorMessage = g.message(code: 'secUser.checkUsernameAvailibility.notAvailable.blockchain',
                    default:'Blockchain of Hyperledger Fabric is not available. Please, run the server before continuing.')
            render view: "create", model: [userInstance: userInstance]
            return
        }

        if (userInstance.hasErrors()) {
            respond userInstance.errors, view: 'create'
            return
        }

        // Back-end validation - Password with maxlength
        if (userInstance.password.length() > 32) {

            flash.userErrorMessage = g.message(code: 'default.password.maxlength', default: '<strong>Password</strong> field does not match with the required pattern.')
            render view: "create", model: [userInstance: userInstance]
            return
        }

        // Check if password and username are same
        if (userInstance.password.toLowerCase() == userInstance.username.toLowerCase()) {

            flash.userErrorMessage = g.message(code: 'default.password.username', default: '<strong>Password</strong> field must not be equal to username.')
            render view: "create", model: [userInstance: userInstance]
            return
        }

        // Back-end validation - Confirm password
        if (!StringUtils.isNotBlank(userInstance.confirmPassword)) {

            flash.userErrorMessage = g.message(code: 'default.password.confirm', default: '<strong>Confirm password</strong> field cannot be null.')
            render view: "create", model: [userInstance: userInstance]
            return
        }

        // Check if password and confirm password fields are same
        if (userInstance.password != userInstance.confirmPassword) {

            flash.userErrorMessage = g.message(code: 'default.password.notsame', default: '<strong>Password</strong> and <strong>Confirm password</strong> fields must match.')
            render view: "create", model: [userInstance: userInstance]
            return
        }

        // It checks that mime-types is correct: ['image/png', 'image/jpeg', 'image/gif']
        if (!filename.empty && !contentsType.contains(filename.getContentType())) {

            flash.userErrorMessage = g.message(code: 'default.validation.mimeType.image', default: 'The profile image must be of type: <strong>.png</strong>, <strong>.jpeg</strong> or <strong>.gif</strong>.')
            render  view: "create", model: [userInstance: userInstance]
            return
        }

        try {

            // Save the image and mime type
            if (!filename.empty) {
                log.debug("SecUserController():save():ImageProfileUploaded:${filename.name}")

                userInstance.avatar = filename.bytes
                userInstance.avatarType = filename.contentType
            } else {
                userInstance.avatar = null
                userInstance.avatarType = null
            }

            // Save user data
            userInstance.save(flush: true, failOnError: true)

            // Obtain user role - Asynchronous/Multi-thread
            def normalRole = SecRole.findByAuthority("ROLE_USER")

            // Save relation with normal user role
            SecUserSecRole.create userInstance, normalRole, true

            request.withFormat {
                form multipartForm {
                    flash.userMessage = g.message(code: 'default.created.message', default: '{0} <strong>{1}</strong> created successful.', args: [message(code: 'user.label', default: 'User'), userInstance.username])
                    redirect view: 'index'
                }
                '*' { respond userInstance, [status: CREATED] }
            }
        } catch (Exception exception) {
            log.error("UserController():save():Exception:NormalUser:${userInstance.username}:${exception}")

            // Roll back in database
            transactionStatus.setRollbackOnly()

            request.withFormat {
                form multipartForm {
                    flash.userErrorMessage = g.message(code: 'default.not.created.message', default: 'ERROR! {0} <strong>{1}</strong> was not created.', args: [message(code: 'user.label', default: 'User'), userInstance.username])
                    render view: "create", model: [userInstance: userInstance]
                }
            }
        }
    }

    /**
     * It edits an existing normal user with the new values of each field.
     *
     * @param userInstance It represents the normal user to edit.
     * @return userInstance It represents the user instance.
     */
    def edit(User userInstance) {
        respond userInstance
    }

    /**
     * It updates an existing normal user in database.
     *
     * @param userInstance It represents the normal user information to update.
     * @return return If the user instance is null or has errors.
     */
    @Transactional
    update(User userInstance) {

        if (userInstance == null) {

            // Roll back in database
            transactionStatus.setRollbackOnly()

            notFound()
            return
        }

        // It checks concurrent updates
        if (params.version) {
            def version = params.version.toLong()

            if (userInstance.version > version) {

                // Roll back in database
                transactionStatus.setRollbackOnly()

                // Clear the list of errors
                userInstance.clearErrors()
                userInstance.errors.rejectValue("version", "default.optimistic.locking.failure", [userInstance.username] as Object[], "Another user has updated the <strong>{0}</strong> instance while you were editing.")

                respond userInstance.errors, view:'edit'
                return
            }
        }

        // Back-end validation - Username in Blockchain
        def blockchainValidation = usernameBlockchainAndDBValidation(userInstance.username)

        // If value is 1 - Username found in BC and not found in DB (OK)
        // Username found in BC and DB
        if (blockchainValidation == 0) {
            flash.userErrorMessage = g.message(code: 'secUser.checkUsernameAvailibility.notAvailable',
                    default:'Username is not available. Please, choose another one.')
            respond userInstance, view: 'edit'
            return
        } else if (blockchainValidation == 2) { // Username not found in BC
            flash.userErrorMessage = g.message(code: 'secUser.checkUsernameAvailibility.notAvailable.user.blockchain',
                    default:'Username does not exist in the Blockchain. Please, create this user before continuing.')
            respond userInstance, view: 'edit'
            return

        } else if (blockchainValidation == 3) { // BC is not available
            flash.userErrorMessage = g.message(code: 'secUser.checkUsernameAvailibility.notAvailable.blockchain',
                    default:'Blockchain of Hyperledger Fabric is not available. Please, run the server before continuing.')
            respond userInstance, view: 'edit'
            return
        }

        // Validate the instance
        if (!userInstance.validate()) {
            respond userInstance.errors, view:''
            return
        }

        try {

            // Save user data
            userInstance.save(flush:true, failOnError: true)

            request.withFormat {
                form multipartForm {
                    flash.userMessage = g.message(code: 'default.updated.message', default: '{0} <strong>{1}</strong> updated successful.', args: [message(code: 'user.label', default: 'User'), userInstance.username])
                    redirect view: 'index'
                }
                '*' { respond userInstance, [status: OK] }
            }
        } catch (Exception exception) {
            log.error("UserController():update():Exception:NormalUser:${userInstance.username}:${exception}")

            // Roll back in database
            transactionStatus.setRollbackOnly()

            request.withFormat {
                form multipartForm {
                    flash.userErrorMessage = g.message(code: 'default.not.updated.message', default: 'ERROR! {0} <strong>{1}</strong> was not updated.', args: [message(code: 'user.label', default: 'User'), userInstance.username])
                    render view: "edit", model: [userInstance: userInstance]
                }
            }
        }
    }

    /**
     * It edits the profile image of an existing normal user.
     *
     * @param userInstance It represents the normal user to edit.
     * @return userInstance It represents the user instance.
     */
    def editProfileImage(User userInstance) {
        respond userInstance
    }

    /**
     * It updates the profile image of an existing normal user in database.
     *
     * @param userInstance It represents the normal user information to update.
     * @return return If the user instance is null or has errors.
     */
    @Transactional
    updateProfileImage(User userInstance) {

        if (userInstance == null) {

            // Roll back in database
            transactionStatus.setRollbackOnly()

            notFound()
            return
        }

        // It checks concurrent updates
        if (params.version) {
            def version = params.version.toLong()

            if (userInstance.version > version) {

                // Roll back in database
                transactionStatus.setRollbackOnly()

                // Clear the list of errors
                userInstance.clearErrors()
                userInstance.errors.rejectValue("version", "default.optimistic.locking.failure", [userInstance.username] as Object[], "Another user has updated the <strong>{0}</strong> instance while you were editing.")

                respond userInstance.errors, view:'editProfileImage'
                return
            }
        }

        // Get the avatar file from the multi-part request
        def filename = request.getFile('avatar')

        // Validate the instance
        if (!userInstance.validate()) {
            respond userInstance.errors, view:'editProfileImage'
            return
        }

        // It checks that mime-types is correct: ['image/png', 'image/jpeg', 'image/gif']
        if (!filename.empty && !contentsType.contains(filename.getContentType())) {

            flash.userErrorMessage = g.message(code: 'default.validation.mimeType.image', default: 'The profile image must be of type: <strong>.png</strong>, <strong>.jpeg</strong> or <strong>.gif</strong>.')
            render  view: "editProfileImage", model: [userInstance: userInstance]
            return
        }

        try {

            // Update the image and mime type
            userInstance.avatar = filename.bytes
            userInstance.avatarType = filename.contentType

            // Update data
            userInstance.save(flush:true, failOnError: true)

            request.withFormat {
                form multipartForm {
                    flash.userMessage = g.message(code: 'default.updated.message', default: '{0} <strong>{1}</strong> updated successful.', args: [message(code: 'user.label', default: 'User'), userInstance.username])
                    redirect view: 'index'
                }
                '*' { respond userInstance, [status: OK] }
            }

        } catch (Exception exception) {
            log.error("UserController():update():Exception:NormalUser:${userInstance.username}:${exception}")

            // Roll back in database
            transactionStatus.setRollbackOnly()

            request.withFormat {
                form multipartForm {
                    flash.userErrorMessage = g.message(code: 'default.not.updated.message', default: 'ERROR! {0} <strong>{1}</strong> was not updated.', args: [message(code: 'user.label', default: 'User'), userInstance.username])
                    render view: "editProfileImage", model: [userInstance: userInstance]
                }
            }
        }
    }

    /**
     * It deletes an existing normal user in database.
     *
     * @param userInstance It represents the normal user information to delete.
     * @return return If the user instance is null, the notFound function is called.
     */
    @Transactional
    delete(User userInstance) {

        if (userInstance == null) {

            // Roll back in database
            transactionStatus.setRollbackOnly()

            notFound()
            return
        }

        try {

            // Delete SecUserSecRole relations
            SecUserSecRole.findAllBySecUser(userInstance)*.delete(flush: true, failOnError: true)

            // Delete user
            userInstance.delete(flush: true, failOnError: true)

            request.withFormat {
                form multipartForm {
                    flash.userMessage = g.message(code: 'default.deleted.message', default: '{0} <strong>{1}</strong> deleted successful.', args: [message(code: 'user.label', default: 'User'), userInstance.username])
                    redirect action: "index", method: "GET"
                }
                '*' { render status: NO_CONTENT }
            }
        } catch (DataIntegrityViolationException exception) {
            log.error("UserController():delete():DataIntegrityViolationException:NormalUser:${userInstance.username}:${exception}")

            // Roll back in database
            transactionStatus.setRollbackOnly()

            request.withFormat {
                form multipartForm {
                    flash.userErrorMessage = g.message(code: 'default.not.deleted.message', default: 'ERROR! {0} <strong>{1}</strong> was not deleted.', args: [message(code: 'user.label', default: 'User'), userInstance.username])
                    redirect action: "index", method: "GET"
                }
                '*' { render status: NO_CONTENT }
            }
        }
    }

    /**
     * It renders the not found message if the user instance was not found.
     */
    protected void notFound() {
        log.error("UserController():notFound():NormalUserID:${params.id}")

        request.withFormat {
            form multipartForm {
                flash.userErrorMessage = g.message(code: 'default.not.found.user.message', default:'It has not been able to locate the normal user with id: <strong>{0}</strong>.', args: [params.id])
                redirect action: "index", method: "GET"
            }
            '*'{ render status: NOT_FOUND }
        }
    }

    /**
     * Back-end validation about the existence of the username in the Blockchain and DB.
     *
     * @param username Name of the user.
     *
     * @return Number to indicate the success or error.
     */
    private usernameBlockchainAndDBValidation (username) {

        def number
        try {
            new URL(blockchain_getUserID + username).getText(requestProperties: [Accept: 'application/json'])

            if (SecUser.countByUsername(username)) { // // Username found in BC and DB
                number = 0
            } else { // Username found in BC and not found in DB
                number = 1
            }

        } catch (FileNotFoundException ignored) { // Username not found in BC
            number = 2

        } catch (ConnectException ignored) { // BC is not available
            number = 3
        }

        return number
    }
}