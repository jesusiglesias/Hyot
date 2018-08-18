package Security

import grails.gorm.transactions.Transactional
import org.springframework.beans.factory.annotation.Value

/**
 * Class that represents to the SecUser controller (actions for admin user).
 */
@Transactional(readOnly = true)
class SecUserController {

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
}
