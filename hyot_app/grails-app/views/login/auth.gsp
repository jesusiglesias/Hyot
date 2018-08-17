<!-------------------------------------------------------------------------------------------*
 *                                    AUTHENTICATION PAGE                                    *
 *------------------------------------------------------------------------------------------->

<html>
<!-- HEAD -->
<head>
    <meta name="layout" content="main_login"/>
    <title><g:message code="views.login.auth.head.title" default="HYOT"/></title>

    <script type="text/javascript">

        // Variables to use in script
        var _stateErrorAccount = '${g.message(code:'customTasksUser.login.stateAccount', default:'Error!')}';
        var _okButton = '${g.message(code:'customTasksUser.login.stateAccount.ok', default:'OK')}';

        // Auto close alert
        function createAutoClosingAlert(selector) {

            var alert = $(selector);

            window.setTimeout(function () {
                alert.hide(1000, function () {
                    $(this).remove();
                });
            }, 5000);
        }
    </script>

</head> <!-- /.HEAD -->

<!-- BODY -->
<body>

<!-- Authentication -->
<div class="content">

    <div class="form-title">
        <span class="form-title"><g:message code="views.login.auth.form.title" default="Welcome."/></span>
        <span class="form-subtitle"><g:message code="views.login.auth.form.subtitle" default="Please login."/></span>
    </div>

    <!-- Account states notification -->
    <g:if test='${flash.errorLogin}'>
        <script type="text/javascript">
            swal({
                title: _stateErrorAccount,
                html: '<p>${flash.errorLogin}</p>',
                type: 'error',
                confirmButtonText: _okButton,
                closeOnConfirm: false,
                customClass: 'errorSweetAlert'
            });
        </script>
    </g:if>

    <!-- Enabled account notification -->
    <g:if test='${flash.errorDisabledLogin}'>
        <script type="text/javascript">
            swal({
                title: _stateErrorAccount,
                text: '${flash.errorDisabledLogin}',
                type: 'error',
                confirmButtonText: _okButton,
                closeOnConfirm: true,
                customClass: 'errorSweetAlert'
            });
        </script>
    </g:if>

    <!-- Wrong credentials -->
    <g:if test='${flash.errorLoginUser}'>
        <div class="alert alert-danger alert-danger-custom alert-dismissable alert-notuser-reauth-invalidsession fade in">
            <button type="button" class="close" data-dismiss="alert" aria-hidden="true"></button>
            <span> ${raw(flash.errorLoginUser)} </span>
        </div>
        <g:javascript>
            createAutoClosingAlert('.alert-notuser-reauth-invalidsession');
        </g:javascript>
    </g:if>

    <!-- Concurrent sessions -->
    <g:if test='${flash.errorSessions}'>
        <div class="alert alert-danger alert-danger-custom alert-dismissable alert-notuser-reauth-invalidsession fade in">
            <button type="button" class="close" data-dismiss="alert" aria-hidden="true"></button>
            <span> ${raw(flash.errorSessions)} </span>
        </div>
        <g:javascript>
            createAutoClosingAlert('.alert-notuser-reauth-invalidsession');
        </g:javascript>
    </g:if>

    <!-- Reauthenticate notification TODO -->
    <g:if test='${flash.reauthenticate}'>
        <div class="alert alert-block alert-warning alert-warning-custom alert-dismissable alert-notuser-reauth-invalidsession fade in">
            <button type="button" class="close" data-dismiss="alert" aria-hidden='true'></button>
            <h5 class="alert-heading alert-reauthentication">${raw(g.message(code:'views.login.auth.warning.title', default:'<strong>Warning!</strong>'))} </h5>
            <p> ${flash.reauthenticate} </p>
        </div>
    </g:if>

    <!-- Invalid session notification, authentication service exception -->
    <g:if test='${flash.errorInvalidSessionAuthenticationException}'>
        <div class="alert alert-block alert-danger alert-danger-custom alert-dismissable alert-notuser-reauth-invalidsession fade in">
            <button type="button" class="close" data-dismiss="alert" aria-hidden='true'></button>
            <p> ${flash.errorInvalidSessionAuthenticationException} </p>
        </div>
        <g:javascript>
            createAutoClosingAlert('.alert-notuser-reauth-invalidsession');
        </g:javascript>
    </g:if>

    <!-- New password successful TODO -->
    <g:if test='${flash.newPasswordSuccessful}'>
        <div class="alert alert-block alert-success alert-success-custom alert-dismissable alert-restorePasswordSuccessful fade in">
            <button type="button" class="close" data-dismiss="alert" aria-hidden='true'></button>
            <p> ${raw(flash.newPasswordSuccessful)} </p>
        </div>
        <g:javascript>
            createAutoClosingAlert('.alert-restorePasswordSuccessful');
        </g:javascript>
    </g:if>

    <!-- Login form -->
    <form action='${postUrl}' method='POST' class="login-form" autocomplete="on">

        <!-- Username/email Field -->
        <div class="form-group form-md-line-input form-md-floating-label has-success">
            <div class="input-icon right">
                <g:textField class="form-control user-input autofill-input emptySpaces" id="username" name='hyot_username' value="${session['SPRING_SECURITY_LAST_USERNAME']}" autocomplete="on"/>
                <label for="username"><g:message code="views.login.auth.form.username/email" default="Username/Email"/></label>
                <span class="help-block"><g:message code="views.login.auth.form.username/email.help" default="Enter a valid username or email"/></span>
                <i class="fa fa-times i-delete" style="right: 50px; cursor: pointer"></i> <!-- Delete text icon -->
                <i class="icon-user"></i>
            </div>
        </div>

        <!-- Password Field -->
        <div class="form-group form-md-line-input form-md-floating-label has-success">
            <div class="input-icon right">
                <g:passwordField class="form-control password-input autofill-input emptySpaces" id="password" name='hyot_password' autocomplete="off" />
                <label for="password"><g:message code="views.login.auth.form.password" default="Password"/></label>
                <span class="help-block"><g:message code="views.login.auth.form.password.help" default="Enter your password"/></span>
                <i class="fa fa-eye i-show"></i> <!-- Show password icon -->
                <i class="fa fa-key"></i>
            </div>
        </div>

        <!-- Remember me and password -->
        <div class="form-actions action-remember-password">
            <div class="pull-left">
                <div class="md-checkbox rememberme">
                    <input type="checkbox" name='${rememberMeParameter}' id='remember_me' class="md-check" <g:if test='${hasCookie}'>checked='checked'</g:if>/>
                    <label for="remember_me" class="">
                        <span></span>
                        <span class="check"></span>
                        <span class="box"></span>
                        <g:message code="views.login.auth.form.rememberme" default="Remember me"/>
                    </label>
                </div>
            </div>

            <!-- Only it shows when is root path. In reauthentication path does not show TODO -->
            <g:if test='${!flash.reauthenticate}'>
                <!-- Forgot password -->
                <div class="pull-right forget-password-block">
                    <g:link uri="/forgotPassword" id="forget-password" class="forget-password"><g:message code="views.login.auth.form.forgotPassword" default="Forgot Password?"/></g:link>
                </div>
            </g:if>
        </div>

        <!-- Log in -->
        <div class="form-actions">
            <g:submitButton  name="${message(code: "views.login.auth.form.login.button", default: "Log in")}" id="login-button" class="btn green-dark btn-block"/>
        </div>
    </form> <!-- /.Authentication form -->

</div> <!-- /.Authentication -->

<!-- Only it shows when is root path. In reauthentication path is not displayed -->
<g:if test='${!flash.reauthenticate}'>
    <div class="copyright"> 2018 © <a href="http://es.linkedin.com/in/jesusgiglesias" target="_blank"> Jes&uacute;s Iglesias Garc&iacute;a </a></div>
    <div class="logoUAM">
        <g:link uri="https://www.uam.es/UAM/Home.htm" target="_blank">
            <asset:image src="logo/logo_uam.gif" alt="UAM"/>
        </g:link>
        <g:link uri="http://www.uam.es/ss/Satellite/EscuelaPolitecnica/es/home.htm" target="_blank">
            <asset:image src="logo/logo_eps.png" alt="EPS"/>
        </g:link>
    </div>
</g:if>

<asset:javascript src="authentication/authentication.js"/>
<asset:javascript src="overlay/loadingoverlay.min.js"/>

</body>
</html>