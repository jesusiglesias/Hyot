<!-------------------------------------------------------------------------------------------*
 *                                         USER PAGE                                         *
 *------------------------------------------------------------------------------------------->
<!DOCTYPE html>
  <!--[if lt IE 7 ]> <html lang="en" class="no-js ie6"> <![endif]-->
  <!--[if IE 7 ]>    <html lang="en" class="no-js ie7"> <![endif]-->
  <!--[if IE 8 ]>    <html lang="en" class="no-js ie8"> <![endif]-->
  <!--[if IE 9 ]>    <html lang="en" class="no-js ie9"> <![endif]-->
  <!--[if (gt IE 9)|!(IE)]><!--> <html lang="en" class="no-js"><!--<![endif]-->

<!-- HEAD -->
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <meta name="description" content="HYOT is a PoC for monitoring IoT environments through Hyperledger"/>
    <meta name="author" content="Jesús Iglesias García"/>
    <meta name="keywords" content="Hyot, Blockchain, Hyperledger, Hyperledger Fabric, Internet of Things, Ledger,
     Raspberry Pi, Security, Sensor, Smart Contracts, Privacy"/>
    <meta name="dcterms.rightsHolder" content="Jesús Iglesias García">
    <meta name="dcterms.dateCopyrighted" content="2018">

    <!-- LOAD TITLE -->
    <title><g:layoutTitle/></title>

    <!-- FAVICON -->
    <link rel="shortcut icon" href="${assetPath(src: 'favicon/favicon.ico')}" type="image/x-icon">
    <link rel="icon" href="${assetPath(src: 'favicon/favicon.ico')}" type="image/x-icon">

    <!-- HUMANS.TXT -->
    <link type="text/plain" rel="author" href="${createLink(uri: '/humans.txt')}"/>

    <!-- GLOBAL MANDATORY STYLES -->
    <link href="https://fonts.googleapis.com/css?family=Raleway" rel="stylesheet">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.5.0/css/font-awesome.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/simple-line-icons/2.2.3/css/simple-line-icons.css">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" crossorigin="anonymous">
    <link rel="stylesheet" href="${resource(dir: 'css/custom', file: 'custom.css')}" type="text/css"/>
    <link rel="stylesheet" href="${resource(dir: 'css', file: 'icofont.min.css')}" type="text/css"/>

    <!-- THEME GLOBAL STYLES -->
    <link rel="stylesheet" href="${resource(dir: 'css', file: 'components-md.css')}" type="text/css" id="style_components"/>
    <link rel="stylesheet" href="${resource(dir: 'css', file: 'plugins-md.css')}" type="text/css"/>

    <!-- THEME LAYOUT STYLES -->
    <link rel="stylesheet" href="${resource(dir: 'css', file: 'layout.css')}" type="text/css"/>
    <link rel="stylesheet" href="${resource(dir: 'css', file: 'light2.css')}" type="text/css" id="style_color"/>

    <!-- LOAD JS -->
    <asset:javascript src="application.js"/>

    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js" crossorigin="anonymous"></script>

    <!-- LOAD HEADER OTHER VIEWS -->
    <g:layoutHead/>

</head> <!-- /.HEAD -->

<!-- BODY -->
<body class="page-header-fixed page-header-fixed-mobile page-sidebar-closed-hide-logo page-content-white page-full-width page-md">

<!-- HEADER -->
<div class="page-header navbar navbar-fixed-top" role="navigation">
    <div class="page-header-inner">
        <!-- Logo -->
        <div class="page-logo page-logo-normaluser">
            <div class="logoAdmin">
                <g:link uri="/">
                    HYOT
                </g:link>
            </div>
        </div> <!-- /.Logo -->

        <sec:ifLoggedIn>

            <!-- Responsive hamburguer -->
            <a href="javascript:;" class="menu-toggler responsive-toggler" data-toggle="collapse" data-target=".navbar-collapse">
                <i class="icofont  icofont-navigation-menu"></i>
            </a>

            <!-- Top navigation menu -->
            <div class="top-menu">
                <ul class="nav navbar-nav pull-right">
                    <sec:ifAllGranted roles="ROLE_USER">
                        <!-- User dropdown -->
                        <li class="dropdown dropdown-user">
                            <a href="javascript:;" class="dropdown-toggle" data-toggle="dropdown" data-hover="dropdown" data-close-others="true">
                                <!-- Profile image -->
                                <img class="img-circle" alt="Profile image" src="${createLink(controller:'controlPanel', action:'profileImage')}"/>
                                <span class="username username-hide-on-mobile">
                                    <sec:username/>
                                </span>
                                <i class="fa fa-angle-down"></i>
                            </a>
                            <ul class="dropdown-menu">
                                <!-- Profile TODO -->
                                <li class="li-iconId-user">
                                    <g:link uri="/profile" id="${sec.loggedInUserInfo(field:"id")}">
                                        <i class="icofont icofont-id iconId-user"></i> <g:message code="layouts.main_auth_admin.head.profile" default="My profile"/>
                                    </g:link>
                                </li>

                                <li class="divider"> </li>

                                <!-- Logout -->
                                <li class="li-logout-user">
                                    <form name="logout" method="POST" action="${createLink(controller:'logout')}">
                                        <button class="exit-switch-button">
                                            <i class="fa fa-sign-out iconLogout-user"></i> <g:message code="layouts.main_auth_admin.head.logout" default="Logout"/>
                                        </button>
                                    </form>
                                </li>
                            </ul>
                        </li> <!-- /. User dropdown -->
                    </sec:ifAllGranted>

                    <!-- Exit button -->
                    <li class="dropdown">
                        <!-- Logout -->
                        <form name="logout" method="POST" action="${createLink(controller:'logout')}">
                            <button class="exit-button dropdown-toggle">
                                <i class="icon-logout"></i>
                            </button>
                        </form>
                    </li>
                </ul>
            </div> <!-- /.Top navigation menu -->

                <!-- Load horizontal menu -->
            <g:pageProperty name="page.horizontalMenu"/>

        </sec:ifLoggedIn>
    </div> <!-- /.Header inner -->
</div><!-- /.HEADER -->

<div class="page-container">
    <sec:ifLoggedIn>
        <div class="page-sidebar-wrapper">
            <div class="page-sidebar page-sidebar-responsive navbar-collapse collapse">
                <div class="page-sidebar-wrapper">
                    <!-- Responsive horizontal menu -->
                    <ul class="page-sidebar-menu visible-sm visible-xs page-header-fixed">
                        <!-- Load responsive horizontal menu -->
                        <g:pageProperty name="page.responsiveHorizontalMenu"/>
                    </ul>
                </div>
            </div>
        </div>
    </sec:ifLoggedIn>

    <!-- LOAD BODY OTHER VIEWS -->
    <g:layoutBody/>

</div> <!-- /. Container -->

<!-- BEGIN FOOTER -->
<div class="page-footer">
    <div class="copyright"> 2018 © <a href="http://es.linkedin.com/in/jesusgiglesias" target="_blank"> Jes&uacute;s Iglesias Garc&iacute;a </a></div>
    <div class="logoUAM">
        <g:link uri="https://www.uam.es/UAM/Home.htm" target="_blank">
            <asset:image src="logo/logo_uam.gif" alt="UAM"/>
        </g:link>
        <g:link uri="http://www.uam.es/ss/Satellite/EscuelaPolitecnica/es/home.htm" target="_blank">
            <asset:image src="logo/logo_eps.png" alt="EPS"/>
        </g:link>
    </div>
</div>

<!-- Back to top -->
<g:link href="#" class="back-to-top back-to-top-error"><g:message code="views.general.backtotop" default="Top"/></g:link>

<!-- LOAD JAVASCRIPT -->
<!-- CORE PLUGINS -->
<asset:javascript src="dropdown/bootstrap-hover-dropdown.min.js"/>
<asset:javascript src="slimScroll/jquery.slimscroll.min.js"/>
<asset:javascript src="custom/custom.js"/>
<asset:javascript src="custom/icon.js"/>

<!-- THEME GLOBAL SCRIPTS -->
<asset:javascript src="app.js"/>

<!-- THEME LAYOUT SCRIPTS -->
<asset:javascript src="layout.js"/>

</body>
</html>