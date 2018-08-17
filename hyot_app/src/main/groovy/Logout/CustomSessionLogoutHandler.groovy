package Logout

import javax.servlet.http.HttpServletRequest
import javax.servlet.http.HttpServletResponse
import org.springframework.security.core.Authentication
import org.springframework.security.core.session.SessionRegistry
import org.springframework.security.web.authentication.logout.LogoutHandler
import org.springframework.util.Assert

/**
 * {@link CustomSessionLogoutHandler} is in charge of removing the {@link SessionRegistry} upon logout. A
 * new {@link SessionRegistry} will then be generated by the framework upon the next request.
 */
final class CustomSessionLogoutHandler implements LogoutHandler {

    // Attribute
    private final SessionRegistry sessionRegistry

    /**
     * Creates a new instance.
     *
     * @param sessionRegistry {@link SessionRegistry} and principal of an user.
     */
    CustomSessionLogoutHandler(SessionRegistry sessionRegistry) {

        Assert.notNull(sessionRegistry, "sessionRegistry cannot be null")
        this.sessionRegistry = sessionRegistry
    }

    /**
     * Clears the {@link SessionRegistry}.
     *
     * @see org.springframework.security.web.authentication.logout.LogoutHandler#logout(
     * javax.servlet.http.HttpServletRequest,
     * javax.servlet.http.HttpServletResponse,
     * org.springframework.security.core.Authentication
     * )
     */
    void logout(HttpServletRequest request, HttpServletResponse response, Authentication authentication) {
        this.sessionRegistry.removeSessionInformation(request.getSession().getId())
    }
}