package Security

import grails.plugin.springsecurity.SpringSecurityService
import groovy.transform.EqualsAndHashCode
import groovy.transform.ToString
import grails.compiler.GrailsCompileStatic


/**
 * It represents the basic information of an user (admin user).
 */
@GrailsCompileStatic
@EqualsAndHashCode(includes='username')
@ToString(includes='username', includeNames=true, includePackage=false)
class SecUser implements Serializable {

    private static final long serialVersionUID = 1

    transient SpringSecurityService springSecurityService

    // Atributes
    UUID id
    Date dateCreated
    String username
    String password
    String confirmPassword          // Plain text, not stored
    String email
    boolean enabled = true
    boolean accountExpired
    boolean accountLocked
    boolean passwordExpired
    byte[] avatar
    String avatarType

    // Transient attributes
    static transients = ['springSecurityService', 'confirmPassword']

    /**
     * It obtains the roles of the entity.
     *
     * @return roles Role/s of the user.
     */
    Set<SecRole> getAuthorities() {
        (SecUserSecRole.findAllBySecUser(this) as List<SecUserSecRole>)*.secRole as Set<SecRole>
    }

    /**
     * It encrypts the password before inserting the entity.
     */
    def beforeInsert() {
        encodePassword()
    }

    /**
     * It encrypts the password before updating the entity.
     */
    def beforeUpdate() {
        if (isDirty('password')) {
            encodePassword()
        }
    }

    /**
     * It encrypts the user's password.
     */
    protected void encodePassword() {
        password = springSecurityService?.passwordEncoder ? springSecurityService.encodePassword(password) : password
    }

    // Restrictions on the attributes of the entity
    static constraints = {
        username blank: false, unique: true, maxSize: 30
        password blank: false, matches: "^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=\\S+\$).{8,}\$", password: true // Pattern
        email blank: false, unique: true, email: true, maxSize: 60
        confirmPassword bindable: true
        avatar nullable:true, maxSize: 1048576 /* 1MB */
        avatarType nullable:true, inList: ['image/png', 'image/jpeg', 'image/gif']
    }

    // It modifies the name of the password column in database
    static mapping = {
        id(generator: "uuid2", type: "uuid-binary", length: 16)
        password column: '`password`'
        tablePerHierarchy(false)
    }
}
