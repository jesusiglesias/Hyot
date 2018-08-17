/* Spring Security Core settings
 ============================================================================================= */
grails.plugin.springsecurity.userLookup.userDomainClassName = 'Security.SecUser'
grails.plugin.springsecurity.userLookup.authorityJoinClassName = 'Security.SecUserSecRole'
grails.plugin.springsecurity.authority.className = 'Security.SecRole'

grails.plugin.springsecurity.controllerAnnotations.staticRules = [
		[pattern: '/**',                access: ['permitAll']], /** It includes: /humans.txt, /robots.txt TODO **/
		[pattern: '/assets/**',         access: ['permitAll']],
		[pattern: '/**/js/**',          access: ['permitAll']],
		[pattern: '/**/css/**',         access: ['permitAll']],
		[pattern: '/**/images/**',      access: ['permitAll']],
		[pattern: '/**/fonts/**',       access: ['permitAll']],
		[pattern: '/**/favicon.ico',    access: ['permitAll']],

		/* Login controller
        ======================================================*/
        [pattern: '/login/full',        access: ['IS_AUTHENTICATED_REMEMBERED']], // TODO
        [pattern: '/login/**',          access: ['permitAll']],

        /* Domain
        ======================================================*/
        [pattern: '/SecUser/**',        access: ['ROLE_ADMIN']],
        [pattern: '/User/**',           access: ['ROLE_ADMIN']],

		/* General tasks of unregistered user TODO
        ======================================================*/
		// LoggedIn
		[pattern: '/customTasksUser/loggedIn',								access: ['IS_AUTHENTICATED_REMEMBERED']],
		// Concurrent sessions
		[pattern: '/customTasksUser/invalidSession',						access: ['permitAll']],
		// Fail authentication
		[pattern: '/customTasksUser/authFail',								access: ['permitAll']],
		// Register normal user TODO
		[pattern: "/customTasksUser/registerAccount",   					access: ['permitAll']],
		[pattern: "/customTasksUser/saveUserRegistered",   					access: ['permitAll']],
		[pattern: "/customTasksUser/enabledAccount",   						access: ['permitAll']],
		[pattern: "/customTasksUser/checkUsernameRegisteredAvailibility",   access: ['permitAll']],
		[pattern: "/customTasksUser/checkEmailRegisteredAvailibility",   	access: ['permitAll']],
		// Restore password
		[pattern: "/customTasksUser/restorePassword",   					access: ['permitAll']],
		// Password
		[pattern: "/customTasksUser/sendEmail",   							access: ['permitAll']],
		[pattern: "/customTasksUser/changePass",   							access: ['permitAll']],
		[pattern: "/customTasksUser/updatePass",   							access: ['permitAll']],
		[pattern: "/customTasksUser/**",   									access: ['permitAll']],

		/* Custom tasks of administrator TODO
        ======================================================*/
	/*	'/customTasksAdmin/dashboard':              ['ROLE_ADMIN'],
		'/customTasksAdmin/reloadUsers':            ['ROLE_ADMIN'],
		'/customTasksAdmin/reloadAdmin':            ['ROLE_ADMIN'],
		'/customTasksAdmin/reloadEvent':            ['ROLE_ADMIN'],
		'/customTasksAdmin/reloadBooking':          ['ROLE_ADMIN'],
		'/customTasksAdmin/reloadLastUsers':        ['ROLE_ADMIN'],
		'/customTasksAdmin/profileImage':           ['ROLE_ADMIN', 'ROLE_USER'],
		'/customTasksBackend/**':                   ['ROLE_ADMIN'],*/

		/* Custom tasks of normal user TODO
        ======================================================*/
		/*'/customTasksNormalUser/home':                ['ROLE_USER'],
		'/customTasksNormalUser/filterEvent':         ['ROLE_USER'],
		'/customTasksNormalUser/allEvents':           ['ROLE_USER'],
		'/customTasksNormalUser/eventSelected':       ['ROLE_USER'],
		'/customTasksNormalUser/updateAvailableTickets':  ['ROLE_USER'],
		'/customTasksNormalUser/buyTickets':          ['ROLE_USER'],
		'/customTasksNormalUser/bookTickets':         ['ROLE_USER'],
		'/customTasksNormalUser/tickets':             ['ROLE_USER'],
		'/customTasksNormalUser/profile':             ['ROLE_USER'],
		'/customTasksNormalUser/updatePersonalInfo':  ['ROLE_USER'],
		'/customTasksNormalUser/notFound':            ['ROLE_USER'],
		'/customTasksNormalUser/creditCard':          ['ROLE_USER'],
		'/customTasksNormalUser/updateCreditCard':    ['ROLE_USER'],
		'/customTasksNormalUser/profileAvatar':       ['ROLE_USER'],
		'/customTasksNormalUser/updateAvatar':        ['ROLE_USER'],
		'/customTasksNormalUser/notFoundAvatar':      ['ROLE_USER'],
		'/customTasksNormalUser/profilePassword':     ['ROLE_USER'],
		'/customTasksNormalUser/updatePassword':      ['ROLE_USER'],
		'/customTasksNormalUser/notFoundPassword':    ['ROLE_USER'],
		'/customTasksNormalUser/bookings':            ['ROLE_USER'],
		'/customTasksNormalUser/payBooking':          ['ROLE_USER'],
		'/customTasksNormalUser/cancelBooking':       ['ROLE_USER'],
		'/customTasksNormalUser/faq':                 ['ROLE_USER'],
		'/customTasksNormalUser/cookiesPolicy':       ['permitAll'],
		'/customTasksNormalUser/contact':             ['ROLE_USER'],
		'/customTasksNormalUser/contactForm':         ['ROLE_USER'],
		'/customTasksNormalUser/**':                  ['ROLE_USER'],*/

		/* Information tasks of normal user TODO
        ======================================================*/
	/*	'/customTasksUserInformation/cookiesPolicy':       ['permitAll'],
		'/customTasksUserInformation/contact':             ['ROLE_USER'],
		'/customTasksUserInformation/contactForm':         ['ROLE_USER'],
		'/customTasksUserInformation/faq':                 ['ROLE_USER'],
		'/customTasksUserInformation/**':                  ['ROLE_USER'],*/
]

// URL redirection based on role
springsecurity.urlredirection.admin = '/dashboard'
springsecurity.urlredirection.user = '/home'

// URL of login page (default: "/login/auth")
grails.plugin.springsecurity.auth.loginFormUrl = '/'
grails.plugin.springsecurity.failureHandler.defaultFailureUrl = '/authFail'

// Default URL - If true, it always redirects to the value of successHandler.defaultTargetUrl (default: "/") after
// successful authentication; otherwise redirects to originally-requested page.
grails.plugin.springsecurity.successHandler.alwaysUseDefault = false
// Default post-login URL if there is no saved request that triggered the login
grails.plugin.springsecurity.successHandler.defaultTargetUrl = '/login/loggedIn'

// It stores the last username in a HTTP session
grails.plugin.springsecurity.apf.storeLastUsername = true

// Login form parameters
grails.plugin.springsecurity.apf.usernameParameter = 'hyot_username'
grails.plugin.springsecurity.apf.passwordParameter = 'hyot_password'

/*  Remember me cookie configuration
======================================================*/
// Remember-me cookie name; should be unique per application
grails.plugin.springsecurity.rememberMe.cookieName = 'hyot_remember_me'
// Max age of the cookie in seconds
grails.plugin.springsecurity.rememberMe.tokenValiditySeconds = 604800
// Value used to encode cookies; should be unique per application
grails.plugin.springsecurity.rememberMe.key = 'hyot_remember_me'
// Login form cookie parameter
grails.plugin.springsecurity.rememberMe.parameter = '_hyot_remember_me'

// TODO

//grails.plugin.springsecurity.filterChain.chainMap = [
  //      [pattern: '/assets/**',      filters: 'none'],
    //    [pattern: '/**/js/**',       filters: 'none'],
  //      [pattern: '/**/css/**',      filters: 'none'],
  //      [pattern: '/**/images/**',   filters: 'none'],
  //      [pattern: '/**/favicon.ico', filters: 'none'],
  //      [pattern: '/**',             filters: 'JOINED_FILTERS']
//]*/

grails.plugin.springsecurity.logout.handlerNames = ['customSessionLogoutHandler','securityContextLogoutHandler']
