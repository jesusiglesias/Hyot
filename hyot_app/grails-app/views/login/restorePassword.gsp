<!-------------------------------------------------------------------------------------------*
 *                                     RESTORE PASSWORD                                      *
 *------------------------------------------------------------------------------------------->

<html>
<!-- HEAD -->
<head>
    <meta name="layout" content="main_login"/>
    <title><g:message code="views.login.auth.forgotPassword.head.title" default="HYOT | Restore password"/></title>
</head> <!-- /.HEAD -->

<!-- BODY -->
<body>

<script type="text/javascript">

    // Variables to use in javascript
    var _forgotPassword = '${g.message(code:'views.login.auth.forgotPassword.email.help', default:'Enter a valid email')}';
    var _sending = '${g.message(code: "customUserTasks.login.stateAccount.sending", default: "Sending...")}';

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

<!-- Authentication -->
<div class="content">
    <!-- Forgot password form -->
    <g:form class="forget-form" controller="customUserTasks" action="sendEmail" method="post" autocomplete="off">

        <div class="form-title">
            <span class="form-title"><g:message code="views.login.auth.forgotPassword.title" default="Forgot password?"/></span>
            <p>
                <span class="form-subtitle"><g:message code="views.login.auth.forgotPassword.subtitle" default="Enter your e-mail to reset it."/></span>
            </p>
        </div>

        <!-- Success alert -->
        <g:if test='${flash.successRestorePassword}'>
            <div class="alert alert-block alert-success alert-success-custom alert-dismissable alert-restorePassword fade in">
                <button type="button" class="close" data-dismiss="alert"></button>
                <p> ${raw(flash.successRestorePassword)} </p>
            </div>
            <g:javascript>
                createAutoClosingAlert('.alert-restorePassword');
            </g:javascript>
        </g:if>

        <!-- Failure alert -->
        <g:if test='${flash.errorRestorePassword}'>
            <div class="alert alert-block alert-danger alert-danger-custom alert-dismissable alert-restorePassword fade in">
                <button type="button" class="close" data-dismiss="alert" aria-hidden='true'></button>
                <p> ${raw(flash.errorRestorePassword)} </p>
            </div>
            <g:javascript>
                createAutoClosingAlert('.alert-restorePassword');
            </g:javascript>
        </g:if>

        <div class="form-group form-md-line-input form-md-floating-label has-success">
            <div class="input-icon right">
                <g:field type="email" class="form-control user-input autofill-input emptySpaces" id="email" name="email" autocomplete="off"/>
                <label for="email"><g:message code="views.login.auth.forgotPassword.email" default="Email"/></label>
                <span class="help-block"><g:message code="views.login.auth.forgotPassword.email.help" default="Enter a valid email"/></span>
                <i class="fa fa-times i-delete" style="right: 50px; cursor: pointer"></i> <!-- Delete text icon -->
                <i class="fa fa-envelope"></i>
            </div>
        </div>

        <div class="form-actions">
            <g:link type="button" uri="/" id="back-btn" class="btn green-dark back-button"><g:message code="views.login.auth.forgotPassword.back" default="Back"/></g:link>
            <button type="submit" id="restore-button" class="btn green-dark pull-right">
                <i class="fa fa-refresh refresh-icon-stop refreshIcon"></i>
                <span><g:message code="views.login.auth.forgotPassword.submit" default="Submit"/></span>
            </button>
        </div>
    </g:form> <!-- /. Forgot password form -->
</div> <!-- /.Authentication -->

<asset:javascript src="authentication/resetPassword.js"/>

</body>
</html>