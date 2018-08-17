package Security

import grails.gorm.DetachedCriteria
import groovy.transform.ToString
import org.codehaus.groovy.util.HashCodeHelper
import grails.compiler.GrailsCompileStatic

/**
 * It represents the association between SecUser and SecRole.
 */
@GrailsCompileStatic
@ToString(cache=true, includeNames=true, includePackage=false)
class SecUserSecRole implements Serializable {

	private static final long serialVersionUID = 1

    // Attributes
	SecUser secUser
	SecRole secRole

	/**
	 * It checks if the objects are equal (the same SecUserId and SecRoleId).
	 *
	 * @param other It represents another entity.
	 *
	 * @return false False if the supplied object is not a SecUserSecRole instance with the same ID values.
	 */
	@Override
	boolean equals(other) {
		if (other instanceof SecUserSecRole) {
			other.secUserId == secUser?.id && other.secRoleId == secRole?.id
		}
	}

	/**
	 * It establishes the hashCode.
	 *
	 * @return hashCode Hashcode of the SecUserSecRole pair.
	 */
    @Override
	int hashCode() {
	    int hashCode = HashCodeHelper.initHash()
        if (secUser) {
            hashCode = HashCodeHelper.updateHash(hashCode, secUser.id)
		}
		if (secRole) {
		    hashCode = HashCodeHelper.updateHash(hashCode, secRole.id)
		}
		hashCode
	}

	/**
	 * It obtains the pair of IDs (SecUser and SecRole).
	 *
	 * @param secUserId ID that represents to the SecUser.
	 * @param secRoleId ID that represents to the SecRole.
	 *
	 * @return SecUserSecRole Data of the SecUser-SecRole.
	 */
	static SecUserSecRole get(UUID secUserId, long secRoleId) {
		criteriaFor(secUserId, secRoleId).get()
	}

	/**
	 * It checks if a SecUser-SecRole pair exists.
	 *
	 * @param secUserId ID that represents to the SecUser.
	 * @param secRoleId ID that represents to the SecRole.
	 *
	 * @return True If the SecUser-SecRole pair exists.
	 */
	static boolean exists(UUID secUserId, long secRoleId) {
		criteriaFor(secUserId, secRoleId).count()
	}

	/**
	 * It searches the SecUser-SecRole pair in the database.
	 *
	 * @param secUserId ID that represents to the SecUser.
	 * @param secRoleId ID that represents to the SecRole.
	 *
	 * @return DetachedCriteria Query that can be executed outside the scope of a session.
	 */
	private static DetachedCriteria criteriaFor(UUID secUserId, long secRoleId) {
		where {
			secUser == SecUser.load(secUserId) &&
			secRole == SecRole.load(secRoleId)
		}
	}

	/**
	 * It creates the new SecUserSecRole.
	 *
	 * @param secUser It represents to the SecUser.
	 * @param secRole It represents to the SecRole.
	 * @param flush It permits to indicate if the storage should be immediate.
	 *
	 * @return instance SecUserSecRole instance.
	 */
	static SecUserSecRole create(SecUser secUser, SecRole secRole, boolean flush = false) {
		def instance = new SecUserSecRole(secUser: secUser, secRole: secRole)
		instance.save(flush: flush)
		instance
	}

	/**
	 * It removes a SecUserSecRole entity.
	 *
	 * @param u It represents to the SecUser.
	 * @param r It represents to the SecRole.
	 * @param flush It permits to indicate if the storage should be immediate.
	 *
	 * @return rowCount Number of row that was removed.
	 */
	static boolean remove(SecUser u, SecRole r) {
		if (u != null && r != null) {
			where { secUser == u && secRole == r }.deleteAll()
		}
	}

	/**
	 * It removes all entries of a SecUser entity.
	 *
	 * @param u It represents to the SecUser.
	 * @param flush It permits to indicate if the storage should be immediate.
	 */
	static int removeAll(SecUser u) {
		u == null ? 0 : where { secUser == u }.deleteAll() as int
	}

	/**
	 * It removes all entries of a SecRole entity.
	 *
	 * @param r It represents to the SecRole.
	 * @param flush It permits to indicate if the storage should be immediate.
	 */
	static int removeAll(SecRole r) {
		r == null ? 0 : where { secRole == r }.deleteAll() as int
	}
    // Restrictions on the attributes of the entity

    static constraints = {
	    secUser nullable: false
		secRole nullable: false, validator: { SecRole r, SecUserSecRole ur ->
			if (ur.secUser?.id) {
				if (exists(ur.secUser.id, r.id)) {
				    return ['userRole.exists']
				}
			}
		}
	}

    // It activates a composite ID
    static mapping = {
		id composite: ['secUser', 'secRole']
		version false
	}
}
