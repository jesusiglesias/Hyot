<!-------------------------------------------------------------------------------------------*
 *                                    LOGIN TASKS PAGES                                      *
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
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/sweetalert2/0.4.3/sweetalert2.css">

    <!-- THEME GLOBAL STYLES -->
    <link rel="stylesheet" href="${resource(dir: 'css', file: 'components-md.css')}" type="text/css" id="style_components"/>
    <link rel="stylesheet" href="${resource(dir: 'css', file: 'plugins-md.css')}" type="text/css"/>

    <!-- PAGE LEVEL STYLES -->
    <link rel="stylesheet" href="${resource(dir: 'css/authentication', file: 'authentication.css')}" type="text/css"/>

    <!-- LOAD JS -->
    <asset:javascript src="application.js"/>

    <!-- Notification -->
    <script src="https://cdn.jsdelivr.net/sweetalert2/0.4.3/sweetalert2.min.js" crossorigin="anonymous"></script>

    <!-- LOAD HEADER OTHER VIEWS -->
    <g:layoutHead/>

</head> <!-- /.HEAD -->

<!-- BODY -->
<body class="login">

<!-- Logo -->
<div class="logo">
    <g:link uri="/">
        HYOT
    </g:link>
</div>

<!-- LOAD BODY OTHER VIEWS -->
<g:layoutBody/>

<!-- Back to top -->
<g:link href="#" class="back-to-top"><g:message code="views.general.backtotop" default="Top"/></g:link>

<!-- CORE PLUGINS -->
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js" crossorigin="anonymous"></script>
<asset:javascript src="slimScroll/jquery.slimscroll.min.js"/>
<asset:javascript src="custom/custom.js"/>

<asset:javascript src="app.js"/>

<!-- PAGE LEVEL SCRIPTS -->
<script src="https://cdn.jsdelivr.net/jquery.validation/1.15.0/jquery.validate.min.js"></script>
<script src="https://cdn.jsdelivr.net/jquery.validation/1.15.0/additional-methods.min.js"></script>

</body>
</html>