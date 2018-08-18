<!-------------------------------------------------------------------------------------------*
 *                                      NO ROLE PAGE                                         *
 *------------------------------------------------------------------------------------------->

<!DOCTYPE html>
  <!--[if lt IE 7 ]> <html lang="en" class="no-js ie6"> <![endif]-->
  <!--[if IE 7 ]>    <html lang="en" class="no-js ie7"> <![endif]-->
  <!--[if IE 8 ]>    <html lang="en" class="no-js ie8"> <![endif]-->
  <!--[if IE 9 ]>    <html lang="en" class="no-js ie9"> <![endif]-->
  <!--[if (gt IE 9)|!(IE)]><!-->
<html lang="en" class="no-js">
<!--<![endif]-->

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

    <!-- Disallow robots -->
    <meta name="robots" content="noindex, nofollow">

    <!-- Title -->
    <title><g:message code="views.noRole.title" default="HYOT | User without role"/></title>

    <!-- FAVICON -->
    <link rel="shortcut icon" href="${assetPath(src: 'favicon/favicon.ico')}" type="image/x-icon">
    <link rel="icon" href="${assetPath(src: 'favicon/favicon.ico')}" type="image/x-icon">

    <!-- HUMANS.TXT -->
    <link type="text/plain" rel="author" href="${createLink(uri: '/humans.txt')}"/>

    <!-- GLOBAL MANDATORY STYLES -->
    <link href="https://fonts.googleapis.com/css?family=Open+Sans:400,300,600,700&subset=all" rel="stylesheet" type="text/css"/>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.5.0/css/font-awesome.min.css">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" crossorigin="anonymous">
    <link rel="stylesheet" href="${resource(dir: 'css/custom', file: 'custom.css')}" type="text/css"/>
    <link rel="stylesheet" href="${resource(dir: 'css/error', file: 'error.css')}" type="text/css"/>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/sweetalert2/0.4.3/sweetalert2.css">

    <!-- THEME GLOBAL STYLES -->
    <link rel="stylesheet" href="${resource(dir: 'css', file: 'components-md.css')}" type="text/css" id="style_components"/>

    <!-- LOAD JS -->
    <asset:javascript src="application.js"/>

    <!-- Notification -->
    <script src="https://cdn.jsdelivr.net/sweetalert2/0.4.3/sweetalert2.min.js" crossorigin="anonymous"></script>

    <!-- HTML5 SHIV, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
		<script src="/js/html5shiv.min.js" type="text/javascript"></script>
    <![endif]-->
</head> <!-- /.HEAD -->

<!-- BODY -->
<body class="error-page">

<!-- Logo -->
<div class="logo">
    <g:link uri="/">
        HYOT
    </g:link>
</div>

<!-- Error description of the container -->
<div id="error-container-noRole">
    <div class="row">
        <div class="col-sm-8 col-sm-offset-2 text-center">
            <h1 class="animation-pullDown"><i class="fa fa-exclamation-circle text-danger"></i> <g:message code="views.noRole.error" default="Error!"/> </h1>
            <h3 class="h3 description-error animation-pullDown">
                <g:message code="views.noRole.description" default="User has no role or is invalid. Please, log out."/>
        </div>
    </div>
</div>

<!-- Logout button -->
<div class="content-error">
    <form name="logout" method="POST" action="${createLink(controller:'logout')}">
        <button class="button-logout btn green-dark btn-block">
            <i class="fa fa-sign-out fa-lg icon-back"></i>
            <g:message code="views.noRole.logout" default="Log out"/>
        </button>
    </form>
</div>

<div class="copyright"> 2018 © <a href="http://es.linkedin.com/in/jesusgiglesias" target="_blank"> Jes&uacute;s Iglesias Garc&iacute;a </a></div>
<div class="logoUAM">
    <g:link uri="https://www.uam.es/UAM/Home.htm" target="_blank">
        <asset:image src="logo/logo_uam.gif" alt="UAM"/>
    </g:link>
    <g:link uri="http://www.uam.es/ss/Satellite/EscuelaPolitecnica/es/home.htm" target="_blank">
        <asset:image src="logo/logo_eps.png" alt="EPS"/>
    </g:link>
</div>

<!-- Back to top -->
<g:link href="#" class="back-to-top back-to-top-error"><g:message code="views.general.backtotop" default="Top"/></g:link>

<!-- LOAD JAVASCRIPT -->
<!-- Enable responsive CSS code on browsers that don't support it -->
<!--[if lt IE 9]>
			<script src="js/respond.min.js"></script>
	<![endif]-->

<!-- CORE PLUGINS -->
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js" crossorigin="anonymous"></script>
<asset:javascript src="custom/icon.js"/>
<asset:javascript src="custom/custom.js"/>

</body>
</html>