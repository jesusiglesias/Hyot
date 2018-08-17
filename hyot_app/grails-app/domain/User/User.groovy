package User

import Security.SecUser

/**
 * It represents the general information of a normal user.
 */
class User extends SecUser {

    // Attributes
    String name
    String surname

    // Restrictions on the attributes of the entity
    static constraints = {
        name blank: false, maxSize: 25
        surname blank: false, maxSize: 40
    }

    static mapping = {
    }
}
