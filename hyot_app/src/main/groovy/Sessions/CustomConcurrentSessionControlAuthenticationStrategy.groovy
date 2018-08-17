package Sessions

import org.springframework.security.core.session.SessionRegistry
import org.springframework.security.web.authentication.session.ConcurrentSessionControlAuthenticationStrategy
import org.springframework.security.core.Authentication

/**
 * It permits to set the control strategy of concurrent sessions for a user.
 */
class CustomConcurrentSessionControlAuthenticationStrategy extends ConcurrentSessionControlAuthenticationStrategy {

    /**
     * It updates the session registry.
     *
     * @param sessionRegistry Session and principal of an user.
     */
    CustomConcurrentSessionControlAuthenticationStrategy(SessionRegistry sessionRegistry) {
        super(sessionRegistry)
    }

    /**
     * It sets the maximum number of concurrent sessions. TODO Check if role is "ROLE_SUPER_ADMIN" then set allowed session to 1
     * else unlimited (i.e. -1)
     *
     * @param authentication Information related to authentication of an user.
     * @return maximumSession Maximum concurrent sessions allowed for an user.
     */
    protected int getMaximumSessionsForThisUser(Authentication authentication) {

        // User role: 1
        Long maximumSession = 1

        // Admin role: endless sessions
        if ('ROLE_ADMIN' in authentication.authorities*.authority) {
            maximumSession = -1
        }
        return maximumSession
    }
}

