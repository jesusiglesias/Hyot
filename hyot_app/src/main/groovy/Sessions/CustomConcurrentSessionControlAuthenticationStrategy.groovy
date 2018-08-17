package Sessions

import org.springframework.security.core.Authentication
import org.springframework.security.core.session.SessionRegistry
import org.springframework.security.web.authentication.session.ConcurrentSessionControlAuthenticationStrategy

/**
 * Custom control strategy of concurrent sessions for a user depending on the role.
 */
class CustomConcurrentSessionControlAuthenticationStrategy extends ConcurrentSessionControlAuthenticationStrategy {

    /**
     * It updates the session registry.
     *
     * @param sessionRegistry {@link SessionRegistry} and principal of an user.
     */
    CustomConcurrentSessionControlAuthenticationStrategy(SessionRegistry sessionRegistry) {
        super(sessionRegistry)
    }

    /**
     * It sets the maximum number of concurrent sessions for each user depending on the role.
     *
     * @param authentication Information related to {@link Authentication} of an user.
     *
     * @return maximumSession Maximum concurrent sessions allowed for an user.
     */
    protected int getMaximumSessionsForThisUser(Authentication authentication) {

        // User role - 1 session
        Long maximumSession = 1

        // Admin role - Unlimited sessions
        if ('ROLE_ADMIN' in authentication.authorities*.authority) {
            maximumSession = -1
        }
        return maximumSession
    }
}

