<!-------------------------------------------------------------------------------------------*
 *                                       ERROR PAGES                                         *
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

    <!-- LOAD TITLE -->
    <title><g:layoutTitle/></title>

    <!-- FAVICON -->
    <link rel="shortcut icon" href="${assetPath(src: 'favicon/favicon.ico')}" type="image/x-icon">
    <link rel="icon" href="${assetPath(src: 'favicon/favicon.ico')}" type="image/x-icon">

    <!-- HUMANS.TXT TODO -->
    <link type="text/plain" rel="author" href="${createLink(uri: '/humans.txt')}"/>

    <!-- GLOBAL MANDATORY STYLES -->
    <link href="https://fonts.googleapis.com/css?family=Raleway" rel="stylesheet">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.5.0/css/font-awesome.min.css">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" crossorigin="anonymous">
    <link rel="stylesheet" href="${resource(dir: 'css/custom', file: 'custom.css')}" type="text/css"/>
    <link rel="stylesheet" href="${resource(dir: 'css/error', file: 'error.css')}" type="text/css"/>

    <!-- THEME GLOBAL STYLES -->
    <link rel="stylesheet" href="${resource(dir: 'css', file: 'components-md.css')}" type="text/css" id="style_components"/>

    <!-- LOAD JS -->
    <asset:javascript src="application.js"/>

    <!-- LOAD HEADER OTHER VIEWS -->
    <g:layoutHead/>

</head> <!-- /.HEAD -->

<!-- BODY -->
<body class="error-page">

<!-- Logo -->
<div class="logo">
    <g:link uri="/">
        HYOT
    </g:link>
</div>

<!-- LOAD BODY OTHER VIEWS -->
<g:layoutBody/>

<!-- Back button -->
<div class="content-error">
    <g:link uri="/" class="btn green-dark btn-block">
        <i class="fa fa-chevron-circle-left fa-lg icon-back"></i>
        <g:message code="layouts.error_pages.back" default="Go back to homepage"/>
    </g:link>
</div>

<div class="copyright"> 2018 © Jesús Iglesias García </div>
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

<!-- CORE PLUGINS -->
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js" crossorigin="anonymous"></script>
<asset:javascript src="custom/icon.js"/>
<asset:javascript src="custom/custom.js"/>

</body>
</html>