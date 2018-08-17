/*-------------------------------------------------------------------------------------------*
 *                                         RESOURCES                                         *
 *-------------------------------------------------------------------------------------------*/

package spring

import Security.SecUserPasswordEncoderListener
import Security.CustomGrailsUserDetailsService
import Sessions.CustomConcurrentSessionControlAuthenticationStrategy
import org.springframework.security.core.session.SessionRegistryImpl
import org.springframework.security.web.authentication.session.SessionFixationProtectionStrategy
import org.springframework.security.web.authentication.session.RegisterSessionAuthenticationStrategy
import org.springframework.security.web.authentication.session.CompositeSessionAuthenticationStrategy
import Logout.CustomSessionLogoutHandler


// Place your Spring DSL code here
beans = {
    secUserPasswordEncoderListener(SecUserPasswordEncoderListener)

    // Bean registration - Login by email or username
    userDetailsService(CustomGrailsUserDetailsService)

    // Bean registration - Invalidate concurrent sessions depending on the role

    // Mechanism with a thread-safe map to register new sessions. It stores both by session ID and by principal.
    // And it uses the SessionInformation class which contains some information, such as the last time anything happened
    // on this session, and if it is expired
    sessionRegistry(SessionRegistryImpl)

    customSessionLogoutHandler(CustomSessionLogoutHandler, ref('sessionRegistry'))

    customConcurrentSessionControlAuthenticationStrategy(CustomConcurrentSessionControlAuthenticationStrategy,ref('sessionRegistry')){
        // If it is true, an exception is thrown if the concurrent sessions exceed the maximumSession. If not,
        // old sessions of an user are invalidated
        exceptionIfMaximumExceeded = true
        maximumSessions = 1
    }

    sessionFixationProtectionStrategy(SessionFixationProtectionStrategy){
        migrateSessionAttributes = true
        alwaysCreateSession = true
    }
    registerSessionAuthenticationStrategy(RegisterSessionAuthenticationStrategy,ref('sessionRegistry'))

    sessionAuthenticationStrategy(CompositeSessionAuthenticationStrategy,[ref('customConcurrentSessionControlAuthenticationStrategy'),ref('sessionFixationProtectionStrategy'),ref('registerSessionAuthenticationStrategy')])
}
