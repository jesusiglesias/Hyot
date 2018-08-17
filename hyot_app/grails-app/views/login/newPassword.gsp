<!-------------------------------------------------------------------------------------------*
 *                                       NEW PASSWORD                                        *
 *------------------------------------------------------------------------------------------->

<html>
<!-- HEAD -->
<head>
    <meta name="layout" content="main_login"/>
    <title><g:message code="views.login.auth.newPassword.head.title" default="HYOT | New password"/></title>

    <script type="text/javascript">

        // Variables to use in script
        var _weak = '${g.message(code:'default.password.strength.weak', default:'Weak')}';
        var _normal = '${g.message(code:'default.password.strength.normal', default:'Normal')}';
        var _medium = '${g.message(code:'default.password.strength.medium', default:'Medium')}';
        var _strong = '${g.message(code:'default.password.strength.strong', default:'Strong')}';
        var _veryStrong = '${g.message(code:'default.password.strength.veryStrong', default:'Very strong')}';
        var _minlengthField = '${g.message(code:'default.validation.minlength', default:'Please, enter more than {0} characters.')}';
        var _maxlengthField = '${g.message(code:'default.validation.maxlength', default:'Please, enter less than {0} characters.')}';
        var _requiredField = '${g.message(code:'default.validation.required', default:'This filed is required.')}';
        var _equalPassword = '${raw(g.message(code:'default.password.notsame', default:'<strong>Password</strong> and <strong>Confirm password</strong> fields must match.'))}';
        var _confirming = '${g.message(code: "customUserTasks.updatePassword.submitButton.confirming", default: "Confirming...")}';

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
<!-- Forgot password form -->
    <g:form class="forget-form" controller="customUserTasks" action="updatePass" method="post" autocomplete="off">

        <div class="form-title newPassword-form">
            <span class="form-title"><g:message code="views.login.auth.newPassword.title" default="New password"/></span>
            <p>
                <span class="form-subtitle"><g:message code="views.login.auth.newPassword.subtitle" default="Please, you make sure to read the following instructions:"/></span>
            </p>
        </div>

        <!-- Accordion -->
        <div class="portlet-body">
            <div class="panel-group accordion" id="accordionNewPassword">
                <div class="panel panel-default">
                    <div class="panel-heading profileNewPassword-instructions-head">
                        <h4 class="panel-title">
                            <a class="accordion-toggle accordion-toggle-styled" data-toggle="collapse" data-parent="#accordionNewPassword" href="#collapseNewPassword"> <g:message code="views.login.auth.newPassword.description" default="New password instructions"/> </a>
                        </h4>
                    </div>
                    <div id="collapseNewPassword" class="panel-collapse collapse">
                        <div class="panel-body">
                            <ul>
                                <li> <g:message code="views.login.auth.newPassword.longitude" default="It must contain a length between 8 characters and 32 characters."/> </li>
                                <li> <g:message code="views.login.auth.newPassword.number" default="It must contain at least one number."/> </li>
                                <li> <g:message code="views.login.auth.newPassword.lowercase" default="It must contain at least one lowercase letter."/> </li>
                                <li> <g:message code="views.login.auth.newPassword.uppercase" default="It must contain at least one uppercase letter."/> </li>
                                <li> <g:message code="views.login.auth.newPassword.whitespace" default="It must not contain whitespaces."/> </li>
                                <li> <g:message code="views.login.auth.newPassword.character" default="It can contain special characters."/> </li>
                                <li> <g:message code="views.login.auth.newPassword.username" default="It must not be equal to username."/> </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Failure alert -->
        <g:if test='${flash.errorNewPassword}'>
            <div class="alert alert-block alert-danger alert-danger-custom alert-dismissable alert-newPassword fade in">
                <button type="button" class="close" data-dismiss="alert" aria-hidden='true'></button>
                <p> ${raw(flash.errorNewPassword)} </p>
            </div>

            <g:javascript>
                createAutoClosingAlert('.alert-newPassword');
            </g:javascript>
        </g:if>

        <!-- Password field -->
        <div class="form-group form-md-line-input form-md-floating-label has-success">
            <div class="input-icon right">
                <g:field type="password" class="form-control password-input autofill-input emptySpaces" id="password" name="password" maxlength="32" autocomplete="off"/>
                <label for="password"><g:message code="views.login.auth.newPassword.password" default="New password"/></label>
                <span class="help-block"><g:message code="views.login.auth.newPassword.password.help" default="Enter a valid password"/></span>
                <i class="fa fa-eye i-show"></i> <!-- Show password icon -->
                <i class="fa fa-key"></i>
            </div>
            <div id="container-password">
                <div class='pwstrength-viewport-progress'></div>
                <div class='pwstrength-viewport-verdict'></div>
            </div>
        </div>

        <!-- Password confirm field -->
        <div class="form-group form-md-line-input form-md-floating-label has-success form-confirmPassword">
            <div class="input-icon right">
                <g:field type="password" class="form-control password-confirm-input autofill-input emptySpaces" id="passwordConfirm" name="passwordConfirm" maxlength="32" autocomplete="off"/>
                <label for="passwordConfirm"><g:message code="views.login.auth.newPassword.passwordConfirm" default="Confirm password"/></label>
                <span class="help-block"><g:message code="views.login.auth.newPassword.passwordConfirm.help" default="Repeat your password"/></span>
                <i class="fa fa-eye i-show-confirm"></i> <!-- Show password icon -->
                <i class="fa fa-key i-checkPassword"></i>
            </div>
        </div>

        <!-- Token -->
        <g:hiddenField name="token" value="${params.token}"/>

        <div class="form-actions">
            <g:link type="button" uri="/" id="back-btn" class="btn green-dark back-button"><g:message code="views.login.auth.newPassword.homepage" default="Homepage"/></g:link>
            <button type="submit" id="newPassword-button" class="btn green-dark pull-right">
                <i class="fa fa-refresh refresh-icon-stop refreshIcon"></i>
                <span><g:message code="views.login.auth.newPassword.send" default="Confirm"/></span>
            </button>
        </div>
    </g:form> <!-- /. Forgot password form -->
</div> <!-- /.Authentication -->

<!-- LOAD JAVASCRIPT  -->
<asset:javascript src="password/pwstrength-bootstrap.min.js"/>
<asset:javascript src="password/custom-passwordRegister.js"/>
<asset:javascript src="maxLength/bootstrap-maxlength.min.js"/>
<asset:javascript src="authentication/newPassword.js"/>

</body>
</html>