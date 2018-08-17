package Security

import groovy.transform.EqualsAndHashCode
import groovy.transform.ToString
import grails.compiler.GrailsCompileStatic

/**
 * It represents the role of an user.
 */
@GrailsCompileStatic
@EqualsAndHashCode(includes='authority')
@ToString(includes='authority', includeNames=true, includePackage=false)
class SecRole implements Serializable {

	private static final long serialVersionUID = 1

	// Attributes
	String authority

	// Restrictions on the attributes of the entity
	static constraints = {
		authority nullable: false, blank: false, unique: true
	}

	static mapping = {
		cache true
	}
}
