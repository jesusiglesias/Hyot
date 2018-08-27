/* Spring Security Core settings
 ============================================================================================= */
grails.plugin.springsecurity.userLookup.userDomainClassName = 'Security.SecUser'
grails.plugin.springsecurity.userLookup.authorityJoinClassName = 'Security.SecUserSecRole'
grails.plugin.springsecurity.authority.className = 'Security.SecRole'

grails.plugin.springsecurity.controllerAnnotations.staticRules = [
		[pattern: '/**',                access: ['permitAll']], /** It includes: /humans.txt, /robots.txt **/
		[pattern: '/assets/**',         access: ['permitAll']],
		[pattern: '/**/js/**',          access: ['permitAll']],
		[pattern: '/**/css/**',         access: ['permitAll']],
		[pattern: '/**/images/**',      access: ['permitAll']],
		[pattern: '/**/fonts/**',       access: ['permitAll']],
		[pattern: '/**/favicon.ico',    access: ['permitAll']],

		/* Login controller
        ======================================================*/
        [pattern: '/login/**',          access: ['permitAll']],

        /* Domain
        ======================================================*/
        [pattern: '/SecUser/checkEmailAvailibility',   				access: ['ROLE_ADMIN', 'ROLE_USER']],
        [pattern: '/SecUser/**',       	 							access: ['ROLE_ADMIN']],
        [pattern: '/User/**',           							access: ['ROLE_ADMIN']],

		/* General tasks of unregistered user
        ======================================================*/
		// LoggedIn
		// User must be authenticated by explicit login or remember me cookie
		[pattern: '/customUserTasks/loggedIn',						access: ['IS_AUTHENTICATED_REMEMBERED']],
		// Fail authentication
		[pattern: '/customUserTasks/authFail',						access: ['permitAll']],
		// Restore password
		[pattern: "/customUserTasks/restorePassword",   			access: ['permitAll']],
		// Password
		[pattern: "/customUserTasks/sendEmail",   					access: ['permitAll']],
		[pattern: "/customUserTasks/changePass",   					access: ['permitAll']],
		[pattern: "/customUserTasks/updatePass",   					access: ['permitAll']],
		[pattern: "/customUserTasks/**",   							access: ['permitAll']],
		// No role
		[pattern: '/noRole', 										access: ['IS_AUTHENTICATED_REMEMBERED']],

		/* Custom tasks of administrator
        ======================================================*/
		[pattern: '/controlPanel/dashboard',        				access: ['ROLE_ADMIN']],
        [pattern: '/controlPanel/profileImage',     				access: ['ROLE_ADMIN', 'ROLE_USER']],
	    [pattern: '/controlPanel/reloadAdmin',      				access: ['ROLE_ADMIN']],
	    [pattern: '/controlPanel/reloadNormalUser', 				access: ['ROLE_ADMIN']],
	    [pattern: '/controlPanel/reloadLastUsers',  				access: ['ROLE_ADMIN']],
	    [pattern: '/controlPanel/reloadMeasurement',  				access: ['ROLE_ADMIN']],
	    [pattern: '/controlPanel/reloadAlert',  					access: ['ROLE_ADMIN']],
	    [pattern: '/controlPanel/reloadUserBC',  					access: ['ROLE_ADMIN']],
	    [pattern: '/controlPanel/alertBySensor',  					access: ['ROLE_ADMIN']],
	    [pattern: '/controlPanel/alertByEvent',  					access: ['ROLE_ADMIN']],
	    [pattern: '/controlPanel/measurementAlertByUser',  			access: ['ROLE_ADMIN']],
        [pattern: '/controlPanel/**',               				access: ['ROLE_ADMIN']],
		[pattern: '/alert/getAllAlerts',        					access: ['ROLE_ADMIN']],
		[pattern: '/measurement/getAllMeasurements',   				access: ['ROLE_ADMIN']],

		/* Tasks of the normal user
        ======================================================*/
		[pattern: '/userPage/home',               					access: ['ROLE_USER']],
		[pattern: '/userPage/reloadMymeasurement',          		access: ['ROLE_USER']],
		[pattern: '/userPage/reloadMyalert',               			access: ['ROLE_USER']],
		[pattern: '/userPage/myalertBySensor',               		access: ['ROLE_USER']],
		[pattern: '/userPage/myalertByEvent',               		access: ['ROLE_USER']],
		[pattern: '/userPage/mymeasurements',               		access: ['ROLE_USER']],
		[pattern: '/userPage/myalerts',			               		access: ['ROLE_USER']],
		[pattern: '/userPage/profile',			               		access: ['ROLE_USER']],
		[pattern: '/userPage/updatePersonalInfo',			        access: ['ROLE_USER']],
		[pattern: '/userPage/notFound',			               		access: ['ROLE_USER']],
		[pattern: '/userPage/profilePassword',			            access: ['ROLE_USER']],
		[pattern: '/userPage/updatePassword',			      		access: ['ROLE_USER']],
		[pattern: '/userPage/notFoundPassword',	            		access: ['ROLE_USER']],
		[pattern: '/userPage/profileAvatar',	            		access: ['ROLE_USER']],
		[pattern: '/userPage/updateAvatar',		            		access: ['ROLE_USER']],
		[pattern: '/userPage/notFoundAvatar',	            		access: ['ROLE_USER']],
		[pattern: '/userPage/**',               					access: ['ROLE_USER']],
]

// URL redirection based on role
springsecurity.urlredirection.admin = '/dashboard'
springsecurity.urlredirection.user = '/home'
springsecurity.urlredirection.noRole = '/noRole'

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

/* Logout handlers
============================================================================================= */
grails.plugin.springsecurity.logout.handlerNames = ['customSessionLogoutHandler',
													'rememberMeServices',
													'securityContextLogoutHandler']