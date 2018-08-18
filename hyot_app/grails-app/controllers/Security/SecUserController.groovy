package Security

import grails.gorm.transactions.Transactional
import org.springframework.beans.factory.annotation.Value
import grails.converters.JSON
import org.apache.commons.lang.StringUtils
import org.springframework.dao.DataIntegrityViolationException

/**
 * Class that represents to the SecUser controller (actions for admin user).
 */
@Transactional(readOnly = true)
class SecUserController {

    static allowedMethods = [save: "POST", update: "PUT", updateProfileImage: 'POST', delete: "DELETE"]

    // Mime-types allowed in image
    private static final contentsType = ['image/png', 'image/jpeg', 'image/gif']

    // Default value of pagination
    @Value('${paginate.defaultValue:10}')
            defaultPag

    /**
     * It lists the main data of all administrators of the database.
     *
     * @param max Maximum number of administrators to list.
     * @return SecUser List of administrators with their information and number of administrators in the database.
     */
    def index(Integer max) {
        //params.max = Math.min(max ?: 10, 100)

        // Protecting against attacks when max is a negative number. If is 0, max = defaultPag
        max = max ?: defaultPag.toInteger()
        // If max < 0, return all records (This is dangerous)
        if (max < 0) {
            max = defaultPag.toInteger()
        }
        params.max = Math.min(max, 100)

        // Obtain admin role
        def role = SecRole.findByAuthority("ROLE_ADMIN")

        // Obtain users with admin role
        def administrators = SecUserSecRole.findAllBySecRole(role).secUser

        respond administrators
    }

    /**
     * It creates a new secUser instance.
     *
     * @return return If the secUser instance is null or has errors.
     */
    def create() {
        respond new SecUser(params)
    }

    /**
     * It checks the username availability.
     */
    def checkUsernameAvailibility () {

        def responseData

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
        render responseData as JSON
    }

    /**
     * It checks the email availability.
     */
    def checkEmailAvailibility () {

        def responseData

        if (SecUser.countByEmail(params.email)) { // Email found
            responseData = [
                    'status': "ERROR",
                    'message': g.message(code: 'secUser.checkEmailAvailibility.notAvailable', default:'Email is not available. Please, choose another one.')
            ]
        } else { // Email not found
            responseData = [
                    'status': "OK",
                    'message':g.message(code: 'secUser.checkEmailAvailibility.available', default:'Email available.')
            ]
        }
        render responseData as JSON
    }

    /**
     * It saves an administrator in the database.
     *
     * @param secUserInstance It represents the administrator to save.
     * @return return If the secUser instance is null or has errors.
     */
    @Transactional
    save(SecUser secUserInstance) {

        if (secUserInstance == null) {

            // Roll back in database
            transactionStatus.setRollbackOnly()

            notFound()
            return
        }

        // Get the avatar file from the multi-part request
        def filename = request.getFile('avatar')

        if (secUserInstance.hasErrors()) {
            respond secUserInstance.errors, view:'create'
            return
        }

        // Back-end validation - Password with maxlength
        if (secUserInstance.password.length() > 32) {

            flash.secUserErrorMessage = g.message(code: 'default.password.maxlength', default: '<strong>Password</strong> field does not match with the required pattern.')
            render view: "create", model: [secUserInstance: secUserInstance]
            return
        }

        // Check if password and username are same
        if (secUserInstance.password.toLowerCase() == secUserInstance.username.toLowerCase()) {

            flash.secUserErrorMessage = g.message(code: 'default.password.username', default: '<strong>Password</strong> field must not be equal to username.')
            render view: "create", model: [secUserInstance: secUserInstance]
            return
        }

        // Back-end validation - Confirm password
        if (!StringUtils.isNotBlank(secUserInstance.confirmPassword)) {

            flash.secUserErrorMessage = g.message(code: 'default.password.confirm', default: '<strong>Confirm password</strong> field cannot be null.')
            render view: "create", model: [secUserInstance: secUserInstance]
            return
        }

        // Check if password and confirm password fields are same
        if (secUserInstance.password != secUserInstance.confirmPassword) {

            flash.secUserErrorMessage = g.message(code: 'default.password.notsame', default: '<strong>Password</strong> and <strong>Confirm password</strong> fields must match.')
            render view: "create", model: [secUserInstance: secUserInstance]
            return
        }

        // It checks that mime-types is correct: ['image/png', 'image/jpeg', 'image/gif']
        if (!filename.empty && !contentsType.contains(filename.getContentType())) {

            flash.secUserErrorMessage = g.message(code: 'default.validation.mimeType.image', default: 'The profile image must be of type: <strong>.png</strong>, <strong>.jpeg</strong> or <strong>.gif</strong>.')
            render  view: "create", model: [secUserInstance: secUserInstance]
            return
        }

        try {

            // Save the image and mime type
            if (!filename.empty) {
                log.debug("SecUserController():save():ImageProfileUploaded:${filename.name}")

                secUserInstance.avatar = filename.bytes
                secUserInstance.avatarType = filename.contentType
            } else {
                secUserInstance.avatar = null
                secUserInstance.avatarType = null
            }

            // Save admin data
            secUserInstance.save(flush:true, failOnError: true)

            // Save relation with admin role - Asynchronous/Multi-thread
            def adminRole = SecRole.findByAuthority('ROLE_ADMIN')

            // Save relation with admin role
            SecUserSecRole.create secUserInstance, adminRole, true

            request.withFormat {
                form multipartForm {
                    flash.secUserMessage = g.message(code: 'default.created.message', default: '{0} <strong>{1}</strong> created successful.', args: [message(code: 'admin.label', default: 'Administrator'), secUserInstance.username])
                    redirect view: 'index'
                }
                '*' { respond secUserInstance, [status: CREATED] }
            }
        } catch (Exception exception) {
            log.error("SecUserController():save():Exception:Administrator:${secUserInstance.username}:${exception}")

            // Roll back in database
            transactionStatus.setRollbackOnly()

            request.withFormat {
                form multipartForm {
                    flash.secUserErrorMessage = g.message(code: 'default.not.created.message', default: 'ERROR! {0} <strong>{1}</strong> was not created.', args: [message(code: 'admin.label', default: 'Administrator'), secUserInstance.username])
                    render view: "create", model: [secUserInstance: secUserInstance]
                }
            }
        }
    }

    /**
     * It edits an existing administrator with the new values of each field.
     *
     * @param secUserInstance It represents the administrator to edit.
     * @return secUserInstance It represents the secUser instance.
     */
    def edit(SecUser secUserInstance) {
        respond secUserInstance
    }


    /**
     * It updates an existing administrator in database.
     *
     * @param secUserInstance It represents the administrator information to update.
     * @return return If the secUser instance is null or has errors.
     */
    @Transactional
    update(SecUser secUserInstance) {

        if (secUserInstance == null) {

            // Roll back in database
            transactionStatus.setRollbackOnly()

            notFound()
            return
        }

        // It checks concurrent updates
        if (params.version) {
            def version = params.version.toLong()

            if (secUserInstance.version > version) {

                // Roll back in database
                transactionStatus.setRollbackOnly()

                // Clear the list of errors
                secUserInstance.clearErrors()
                secUserInstance.errors.rejectValue("version", "default.optimistic.locking.failure", [secUserInstance.username] as Object[], "Another user has updated the <strong>{0}</strong> instance while you were editing.")

                respond secUserInstance.errors, view:'edit'
                return
            }
        }

        // Validate the instance
        if (!secUserInstance.validate()) {
            respond secUserInstance.errors, view:'edit'
            return
        }

        // Back-end validation - Password with maxlength
        if (secUserInstance.password.length() > 32) {

            // Roll back in database
            transactionStatus.setRollbackOnly()

            flash.secUserErrorMessage = g.message(code: 'default.password.maxlength', default: '<strong>Password</strong> field does not match with the required pattern.')
            render view: "edit", model: [secUserInstance: secUserInstance]
            return
        }

        // Check if password and username are same
        if (secUserInstance.password.toLowerCase() == secUserInstance.username.toLowerCase()) {

            // Roll back in database
            transactionStatus.setRollbackOnly()

            flash.secUserErrorMessage = g.message(code: 'default.password.username', default: '<strong>Password</strong> field must not be equal to username.')
            render view: "edit", model: [secUserInstance: secUserInstance]
            return
        }

        // Back-end validation - Confirm password
        if (!StringUtils.isNotBlank(secUserInstance.confirmPassword)) {

            // Roll back in database
            transactionStatus.setRollbackOnly()

            flash.secUserErrorMessage = g.message(code: 'default.password.confirm', default: '<strong>Confirm password</strong> field cannot be null.')
            render view: "edit", model: [secUserInstance: secUserInstance]
            return
        }

        // Check if password and confirm password fields are same
        if (secUserInstance.password != secUserInstance.confirmPassword) {

            // Roll back in database
            transactionStatus.setRollbackOnly()

            flash.secUserErrorMessage = g.message(code: 'default.password.notsame', default: '<strong>Password</strong> and <strong>Confirm password</strong> fields must match.')
            render view: "edit", model: [secUserInstance: secUserInstance]
            return
        }

        try {

            // Update admin data
            secUserInstance.save(flush:true, failOnError: true)

            request.withFormat {
                form multipartForm {
                    flash.secUserMessage = g.message(code: 'default.updated.message', default: '{0} <strong>{1}</strong> updated successful.', args: [message(code: 'admin.label', default: 'Administrator'), secUserInstance.username])
                    redirect view: 'index'
                }
                '*' { respond secUserInstance, [status: OK] }
            }

        } catch (Exception exception) {
            log.error("SecUserController():update():Exception:Administrator:${secUserInstance.username}:${exception}")

            // Roll back in database
            transactionStatus.setRollbackOnly()

            request.withFormat {
                form multipartForm {
                    flash.secUserErrorMessage = g.message(code: 'default.not.updated.message', default: 'ERROR! {0} <strong>{1}</strong> was not updated.', args: [message(code: 'admin.label', default: 'Administrator'), secUserInstance.username])
                    render view: "edit", model: [secUserInstance: secUserInstance]
                }
            }
        }
    }

    /**
     * It deletes an existing administrator in database.
     *
     * @param secUserInstance It represents the administrator information to delete.
     * @return return If the secUser instance is null, the notFound function is called.
     */
    @Transactional
    delete(SecUser secUserInstance) {

        if (secUserInstance == null) {

            // Roll back in database
            transactionStatus.setRollbackOnly()

            notFound()
            return
        }

        try {
            // Delete SecUserSecRole relations
            SecUserSecRole.findAllBySecUser(secUserInstance)*.delete(flush: true, failOnError: true)

            // Delete administrator
            secUserInstance.delete(flush:true, failOnError: true)

            request.withFormat {
                form multipartForm {
                    flash.secUserMessage = g.message(code: 'default.deleted.message', default: '{0} <strong>{1}</strong> deleted successful.', args: [message(code: 'admin.label', default: 'Administrator'), secUserInstance.username])
                    redirect action: "index", method: "GET"
                }
                '*' { render status: NO_CONTENT }
            }
        } catch (DataIntegrityViolationException exception) {
            log.error("SecUserController():delete():DataIntegrityViolationException:Administrator:${secUserInstance.username}:${exception}")

            // Roll back in database
            transactionStatus.setRollbackOnly()

            request.withFormat {
                form multipartForm {
                    flash.secUserErrorMessage = g.message(code: 'default.not.deleted.message', default: 'ERROR! {0} <strong>{1}</strong> was not deleted.', args: [message(code: 'admin.label', default: 'Administrator'), secUserInstance.username])
                    redirect action: "index", method: "GET"
                }
                '*' { render status: NO_CONTENT }
            }
        }
    }

    /**
     * It renders the not found message if the secUser instance was not found.
     */
    protected void notFound() {
        log.error("SecUserController():notFound():AdministratorID:${params.id}")

        request.withFormat {
            form multipartForm {
                flash.secUserErrorMessage = g.message(code: 'default.not.found.admin.message', default:'It has not been able to locate the administrator with id: <strong>{0}</strong>.', args: [params.id])
                redirect action: "index", method: "GET"
            }
            '*'{ render status: NOT_FOUND }
        }
    }
}
