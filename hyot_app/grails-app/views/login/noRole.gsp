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

    <meta name="description" content="Smart Testing Tool is a HP CDS solution for online evaluation of different subjects through testing that
    it intended as a tool for internal qualification of personnel."/>
    <meta name="author" content="Jesús Iglesias García"/>
    <meta name="keywords" content="HP CDS, Smart Testing Tool, online test, evaluation test, english testing tool, test online, evaluacion online, Jesus Iglesias, TFG, Universidad de Valladolid, UVa"/>
    <meta name="dcterms.rightsHolder" content="Jesús Iglesias García">
    <meta name="dcterms.dateCopyrighted" content="2016">

    <!-- Disallow robots -->
    <meta name="robots" content="noindex, nofollow">

    <!-- Title -->
    <title><g:message code="views.noRole.title" default="STT | User without role"/></title>

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

    <!-- Google Analytics -->
    <g:render template="/template/googleAnalytics"/>

    <!-- Email notification by means of AJAX -->
    <script type="text/javascript">

        $(document).ready(function () {

            // Variables to use in javascript
            var methodUrl = '${g.createLink(controller: "customTasksUser", action: 'statusNotification')}';
            var _stateErrorAccount = '${g.message(code:'customTasksUser.login.stateAccount', default:'Error!')}';
            var _okButton = '${g.message(code:'customTasksUser.login.stateAccount.ok', default:'OK')}';
            var _successEmail = '${g.message(code:'customTasksUser.login.stateAccount.successful', default:'Email sent successfully!')}';
            var _descriptionSuccessEmail = '${g.message(code:'customTasksUser.login.stateAccount.successful.description', default:'Soon you will receive a response from the administrator.')}';
            var _errorEmail = '${g.message(code:'customTasksUser.login.stateAccount.failure.description', default:'Email with incorrect format, non-existent in the system or a problem has occurred during sending email.')}';
            var _internalError = '${g.message(code:'customTasksUser.login.stateAccount.failure.internalError', default:'It has not been able to connect to the internal server. Try again later.')}';

            $('#noRoleEmail-button').click(function (event) {

                var noRoleSendButton = $('#noRoleEmail-button');
                var refreshIcon = $('.refreshIcon');

                event.preventDefault();

                $.ajax({
                    url: methodUrl,
                    data: {email: $('#noRoleEmail').val(), type: 'noRole'},
                    beforeSend: function(){
                        noRoleSendButton.attr('disabled', true);
                        noRoleSendButton.find('span').text('${message(code: "customTasksUser.login.stateAccount.sending", default: "Sending...")}');
                        refreshIcon.removeClass('refresh-icon-stop');
                        refreshIcon.addClass('refresh-icon');
                        $('.i-delete-noRole').css('right', '155px');
                    },
                    success: function (data) {
                        if (data == "sent") {
                            swal({
                                title: _successEmail,
                                text: _descriptionSuccessEmail,
                                type: 'success',
                                confirmButtonText: _okButton,
                                closeOnConfirm: true,
                                customClass: 'successSweetAlert'
                            })
                        } else {
                            swal({
                                title: _stateErrorAccount,
                                text: _errorEmail,
                                type: 'error',
                                confirmButtonText: _okButton,
                                closeOnConfirm: true,
                                customClass: 'errorSweetAlert'
                            })
                        }
                    },
                    error: function () {
                        swal({
                            title: _stateErrorAccount,
                            text: _internalError,
                            type: 'error',
                            confirmButtonText: _okButton,
                            closeOnConfirm: true,
                            customClass: 'errorSweetAlert'
                        })
                    },
                    complete: function(){
                        noRoleSendButton.removeAttr('disabled');
                        noRoleSendButton.find('span').text('${message(code: "customTasksUser.login.stateAccount.send", default: "Send")}');
                        refreshIcon.removeClass('refresh-icon');
                        refreshIcon.addClass('refresh-icon-stop');
                        $('.i-delete-noRole').css('right', '100px');
                    }
                });
            });
        });
    </script>

</head> <!-- /.HEAD -->

<!-- BODY -->
<body class="error-page">

<!-- Logo -->
<div class="logo-error">
    <g:link uri="/">
        <asset:image src="logo/logo_error_pages.png" alt="SMART TESTING TOOL" class="hvr-wobble-vertical"/>
    </g:link>
</div>

<!-- Error description of the container -->
<div id="error-container-noRole">
    <div class="row">
        <div class="col-sm-8 col-sm-offset-2 text-center">
            <h1 class="animation-pullDown"><i class="fa fa-exclamation-circle text-danger"></i> <g:message code="views.noRole.error" default="Error!"/> </h1>
            <h3 class="h3 description-error animation-pullDown">
                <g:message code="views.noRole.description" default="{0} user has no role or is invalid. Please enter your email below to send an email to the administrator and log out." args="${sec.username()}"/>
        </div>
    </div>
</div>

<div class="row">
    <div class="col-xs-10 col-xs-offset-1 col-sm-8 col-sm-offset-2 col-md-6 col-md-offset-3 col-lg-4 col-lg-offset-4">
        <div class="input-group noRoleEmail-group">
            <g:field type="text" class="form-control user-input emptySpaces" name="noRoleEmail"/>
            <i class="fa fa-times i-delete i-delete-noRole"></i> <!-- Delete text icon -->
            <span class="input-group-btn">
                <button name="noRoleEmail-button" id="noRoleEmail-button" class="btn grey-mint noRoleSend-btn">
                    <i class="fa fa-refresh refresh-icon-stop refreshIcon"></i>
                    <span><g:message code="customTasksUser.login.stateAccount.send" default="Send"/></span>
                </button>
            </span>
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

<div class="copyright"> 2016 © <g:link uri="http://es.linkedin.com/in/jesusgiglesias"> Jesús Iglesias García </g:link></div>
<div class="logoHP-error-page">
    <g:link uri="https://www.hpcds.com/">
        <asset:image src="logo/logo_hp.png" alt="HP CDS" class="hvr-wobble-vertical"/>
    </g:link>
    <g:link uri="https://www.inf.uva.es/" class="logoEscuela">
        <asset:image src="logo/logo_escuela.png" alt="UVa" class="hvr-wobble-vertical"/>
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
<g:javascript src="custom/icon.js"/>
<g:javascript src="custom/custom.js"/>

</body>
</html>