package User

import grails.transaction.Transactional
import grails.plugin.springsecurity.userdetails.GrailsUser
import org.springframework.security.core.GrantedAuthority

/**
 * It extends the GrailsUser class to add a new field in the session (email).
 */
@Transactional
class CustomUserDetails extends GrailsUser {

    // Attribute
    final String email

    CustomUserDetails(String username, String password, boolean enabled,
                      boolean accountNonExpired, boolean credentialsNonExpired,
                      boolean accountNonLocked,
                      Collection<GrantedAuthority> authorities,
                      UUID id, String email) {

        // Call to the constructor
        super(username, password, enabled, accountNonExpired,
                credentialsNonExpired, accountNonLocked, authorities, id)

        this.email = email
    }
}
