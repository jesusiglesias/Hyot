package Security

import grails.gorm.transactions.Transactional
import grails.plugin.springsecurity.SpringSecurityUtils
import grails.plugin.springsecurity.userdetails.GrailsUserDetailsService
import org.springframework.security.core.authority.SimpleGrantedAuthority
import org.springframework.security.core.userdetails.UserDetails
import org.springframework.security.core.userdetails.UsernameNotFoundException
import User.CustomUserDetails

/**
 * It enables the authentication process by email or username.
 */
@Transactional
class CustomGrailsUserDetailsService implements GrailsUserDetailsService {

    // Some Spring Security classes (e.g. RoleHierarchyVoter) expect at least * one role, so we give an user with
    // no granted roles, this one which gets * past that restriction but doesn't grant anything.
    static final List NO_ROLES = [new SimpleGrantedAuthority(SpringSecurityUtils.NO_ROLE)]

    /**
     * It locates the user based on the username.
     *
     * @param username The username identifying the user whose data is required.
     * @param loadRoles Whether to load roles at the same time as loading the user.
     *
     * @return A fully populated user record (never <code>null</code>).
     *
     * @throws UsernameNotFoundException If the user could not be found.
     */
    UserDetails loadUserByUsername(String username, boolean loadRoles) throws UsernameNotFoundException {
        return loadUserByUsername(username)
    }

    /**
     * It locates the user based on the email or username.
     *
     * @param username The username identifying the user whose data is required.
     *
     * @return A fully populated user record (never <code>null</code>).
     *
     * @throws UsernameNotFoundException If the user could not be found.
     */
    @Transactional(readOnly=true, noRollbackFor=[IllegalArgumentException, UsernameNotFoundException])
    UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {

        // It is transactional, but read-only, to avoid lazy loading exceptions when accessing
        // the authorities collection

        SecUser.withTransaction { status ->

            // It searches the user by email or username
            SecUser user = SecUser.findByUsernameOrEmail(username, username)

            // User doesn't exist
            if (!user) throw new UsernameNotFoundException('User not found')

            def authorities = user.authorities.collect {new SimpleGrantedAuthority(it.authority)}

            // Email field added to constructor
            return new CustomUserDetails(user.username, user.password, user.enabled, !user.accountExpired,
                    !user.passwordExpired, !user.accountLocked,
                    authorities ?: NO_ROLES, user.id, user.email)
        }
    }
}