package Authentication;

import grails.plugin.springsecurity.SpringSecurityUtils;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.springframework.security.web.authentication.SavedRequestAwareAuthenticationSuccessHandler;

/**
 * It implements the success authentication handler to redirect to the user according to their role.
 */
public class CustomAuthenticationSuccessHandler extends SavedRequestAwareAuthenticationSuccessHandler {

    // Attributes
    private String userUrl;
    private String adminUrl;

    /**
     * It determines the URL redirection depending on the role.
     *
     * @param request HTTP request to authenticate.
     * @param response HTTP response to authenticate.
     * @return url URL to redirect.
     */
    @Override
    protected String determineTargetUrl(HttpServletRequest request, HttpServletResponse response) {

        // Roles
        boolean hasAdmin = SpringSecurityUtils.ifAllGranted("ROLE_ADMIN");
        boolean hasUser = SpringSecurityUtils.ifAllGranted("ROLE_USER");

        if(hasAdmin){ // Admin role
            return adminUrl;
        }else if (hasUser){ // User role
            return userUrl;
        }else{ // Without role
            return super.determineTargetUrl(request, response);
        }
    }

    /**
     * It establishes the URL redirection in the success authentication process for an admin user.
     *
     * @param userUrl URL redirection for user with admin role.
     */
    public void setUserUrl(String userUrl){
        this.userUrl = userUrl;
    }

    /**
     * It establishes the URL redirection in the success authentication process for an normal user.
     *
     * @param adminUrl URL redirection for user with user role.
     */
    public void setAdminUrl(String adminUrl){
        this.adminUrl = adminUrl;
    }
}
