<%@ page import="User.User" %>
<%@ page import="org.springframework.validation.FieldError" %>
<!DOCTYPE html>
<html>
<head>
    <meta name="layout" content="main_controlpanel">
    <title><g:message code="layouts.main_auth_admin.head.title.user" default="HYOT | Normal users management"/></title>
    <link rel="stylesheet" href="${resource(dir: 'css/iCheck', file: 'green.css')}" type="text/css"/>
    <link rel="stylesheet" href="${resource(dir: 'css/fileInput', file: 'bootstrap-fileinput.css')}" type="text/css"/>

    <script>

        // Variables to use in script
        var _weak = '${g.message(code:'default.password.strength.weak', default:'Weak')}';
        var _normal = '${g.message(code:'default.password.strength.normal', default:'Normal')}';
        var _medium = '${g.message(code:'default.password.strength.medium', default:'Medium')}';
        var _strong = '${g.message(code:'default.password.strength.strong', default:'Strong')}';
        var _veryStrong = '${g.message(code:'default.password.strength.veryStrong', default:'Very strong')}';
        var _checkerUsernameBlockInfo = '${g.message(code:'layouts.main_auth_admin.body.content.admin.create.checker.block.info.username', default:'Type a username and check its availability.')}';
        var _checkUsernameAvailibilityAndBlockchain = '${g.createLink(controller: "user", action: 'checkUsernameAvailibilityAndBlockchain')}';
        var _checkerEmailBlockInfo = '${g.message(code:'layouts.main_auth_admin.body.content.admin.create.checker.block.info.email', default:'Type an email and check its availability.')}';
        var _checkEmailAvailibility = '${g.createLink(controller: "secUser", action: 'checkEmailAvailibility')}';
        var _requiredField = '${g.message(code:'default.validation.required', default:'This field is required.')}';
        var _minlengthField = '${g.message(code:'default.validation.minlength', default:'Please, enter more than {0} characters.')}';
        var _maxlengthField = '${g.message(code:'default.validation.maxlength', default:'Please, enter less than {0} characters.')}';
        var _emailField = '${g.message(code:'default.validation.email', default:'Please, enter a valid email address.')}';
        var _equalPassword = '${raw(g.message(code:'default.password.notsame', default:'<strong>Password</strong> and <strong>Confirm password</strong> fields must match.'))}';
        var _equalPasswordUsername = '${raw(g.message(code:'default.password.username', default:'<strong>Password</strong> field must not be equal to username.'))}';

        // Handler auto close alert
        function createAutoClosingAlert(selector) {
            var alert = $(selector);
            window.setTimeout(function () {
                alert.slideUp(1000, function () {
                    $(this).remove();
                });
            }, 5000);
        }
    </script>
</head>
<body>

<!-- Page-sidebar-wrapper -->
<div class="page-sidebar-wrapper">
    <!-- Page-sidebar -->
    <div class="page-sidebar navbar-collapse collapse">
        <!-- Page-sidebar-menu -->
        <ul class="page-sidebar-menu page-header-fixed" data-keep-expanded="true" data-auto-scroll="true" data-slide-speed="200" style="padding-top: 30px">

            <!-- Load search action -->
            <g:render template="/controlPanel/searchControlPanel"/>

            <li class="nav-item start">
                <a href="javascript:;" class="nav-link nav-toggle">
                    <i class="icon-home"></i>
                    <span class="title"><g:message code="layouts.main_auth_admin.sidebar.title.dashboard" default="Dashboard"/></span>
                    <span class="arrow"></span>
                </a>
                <ul class="sub-menu">
                    <li class="nav-item start">
                        <g:link controller="controlPanel" action="dashboard" class="nav-link">
                            <i class="icofont icofont-dashboard-web"></i>
                            <span class="title"><g:message code="layouts.main_auth_admin.sidebar.title.dashboard.statistics" default="Statistics"/></span>
                        </g:link>
                    </li>
                </ul>
            </li>

            <!-- USERS -->
            <li class="heading">
                <h3 class="uppercase"><g:message code="layouts.main_auth_admin.sidebar.title.users" default="Users"/></h3>
            </li>
            <!-- Admin user -->
            <li class="nav-item">
                <a href="javascript:;" class="nav-link nav-toggle">
                    <i class="fa fa-user-secret"></i>
                    <span class="title"><g:message code="layouts.main_auth_admin.sidebar.admin" default="Administrator user"/></span>
                    <span class="arrow"></span>
                </a>
                <ul class="sub-menu">
                    <li class="nav-item">
                        <g:link uri="/administrator/create" class="nav-link">
                            <i class="fa fa-user-plus"></i>
                            <span class="title"><g:message code="layouts.main_auth_admin.sidebar.new" default="New"/></span>
                        </g:link>
                    </li>
                    <li class="nav-item">
                        <g:link uri="/administrator" class="nav-link">
                            <i class="fa fa-list"></i>
                            <span class="title"><g:message code="layouts.main_auth_admin.sidebar.list" default="List"/></span>
                        </g:link>
                    </li>
                </ul>
            </li>

            <!-- Normal user -->
            <li class="nav-item active open">
                <a href="javascript:;" class="nav-link nav-toggle">
                    <i class="fa fa-user"></i>
                    <span class="title"><g:message code="layouts.main_auth_admin.sidebar.normalUser" default="Normal user"/></span>
                    <span class="selected"></span>
                    <span class="arrow open"></span>
                </a>
                <ul class="sub-menu">
                    <li class="nav-item">
                        <g:link uri="/user/create" class="nav-link">
                            <i class="fa fa-user-plus"></i>
                            <span class="title"><g:message code="layouts.main_auth_admin.sidebar.new" default="New"/></span>
                        </g:link>
                    </li>
                    <li class="nav-item active open">
                        <g:link uri="/user" class="nav-link">
                            <i class="fa fa-list"></i>
                            <span class="title"><g:message code="layouts.main_auth_admin.sidebar.list" default="List"/></span>
                            <span class="selected"></span>
                        </g:link>
                    </li>
                </ul>
            </li>
            <!-- /.USERS -->

            <!-- GENERAL -->
            <li class="heading">
                <h3 class="uppercase"><g:message code="layouts.main_auth_admin.sidebar.title.general" default="General"/></h3>
            </li>
        </ul> <!-- /.Page-sidebar-menu -->
    </div> <!-- Page-sidebar -->
</div> <!-- Page-sidebar-wrapper -->

<!-- Page-content-wrapper -->
<div class="page-content-wrapper">
    <!-- Page-content -->
    <div class="page-content">
        <!-- Page-bar -->
        <div class="page-bar">
            <ul class="page-breadcrumb">
                <li class="iconBar-admin-container">
                    <i class="fa fa-home home-icon iconBar-admin"></i>
                    <g:link uri="/"><g:message code="layouts.main_auth_admin.pageBreadcrumb.title" default="Homepage"/></g:link>
                    <i class="fa fa-circle"></i>
                </li>
                <li>
                    <span><g:message code="layouts.main_auth_admin.pageBreadcrumb.subtitle.user" default="Normal user"/></span>
                </li>
            </ul>
        </div> <!-- /.Page-bar -->

        <!-- Page-title -->
        <h3 class="page-title">
            <g:link uri="/user"><g:message code="layouts.main_auth_admin.body.title.user" default="normal users management"/></g:link>
            <i class="icon-arrow-right icon-title-domain"></i>
            <small><g:message code="layouts.main_auth_admin.body.subtitle.user.edit" default="Edit normal user"/></small>
        </h3>

        <!-- Contain page -->
        <div id="edit-domain">

            <!-- Alerts -->
            <g:if test="${flash.userErrorMessage}">
                <div class='alert alert-error alert-danger-custom-backend alert-dismissable alert-entity-error fade in'>
                    <button type='button' class='close' data-dismiss='alert' aria-hidden='true'></button>
                    <span class="xthin" role="status"> ${raw(flash.userErrorMessage)} </span>
                </div>

                <g:javascript>
                    createAutoClosingAlert('.alert-entity-error');
                </g:javascript>
            </g:if>

            <!-- Error in validation -->
            <g:hasErrors bean="${user}">
                <div class='alert alert-error alert-danger-custom-backend alert-dismissable alert-entity-error fade in'>
                    <button type='button' class='close' data-dismiss='alert' aria-hidden='true'></button>
                    <g:eachError bean="${user}" var="error">
                        <p role="status" class="xthin" <g:if test="${error in FieldError}">data-field-id="${error.field}"</g:if>><g:message error="${error}"/></p>
                    </g:eachError>
                </div>

                <g:javascript>
                    createAutoClosingAlert('.alert-entity-error');
                </g:javascript>
            </g:hasErrors>

            <!-- Delete button -->
            <g:form url="[resource:user, controller: 'user', action: 'delete']" method="DELETE"
                    class="form-delete">
                <div class="btn-group delete-confirm-popover-custom">
                    <button class="btn red-soft btn-block iconDelete-button-container" id="delete-confirm-popover" data-toggle="confirmation"
                            data-placement="rigth" data-popout="true" data-singleton="true"
                            data-original-title="${message(code: 'layouts.main_auth_admin.content.delete.confirm.message', default: 'Are you sure?')}"
                            data-btn-ok-label="${message(code: 'default.button.delete.label', default: 'Delete')}"
                            data-btn-cancel-label="${message(code: 'default.button.cancel.label', default: 'Cancel')}"
                            data-btnOkIcon="glyphicon glyphicon-ok" data-btnOkClass="btn btn-sm btn-success"
                            data-btnCancelIcon="glyphicon glyphicon-remove" data-btnCancelClass="btn btn-sm btn-danger">
                        <i class="fa fa-trash iconDelete-button"></i>
                        <g:message code="layouts.main_auth_admin.body.content.user.delete" default="Delete normal user"/>
                    </button>
                </div>
            </g:form>

            <!-- Edit form -->
            <g:form url="[resource:user, action:'update']" method="PUT" autocomplete="on" class="horizontal-form user-form">
                <g:hiddenField name="version" value="${user?.version}" />
                <fieldset class="form">
                    <g:render template="formEdit"/>
                </fieldset>
                <div class="domain-button-group">
                    <!-- Cancel button -->
                    <g:link type="button" uri="/user" class="btn grey-mint"><g:message code="default.button.cancel.label" default="Cancel"/></g:link>
                    <button type="submit" class="btn green-dark icon-button-container" name="update">
                        <i class="fa fa-check icon-button"></i>
                        <g:message code="default.button.update.label" default="Update"/>
                    </button>
                </div>
            </g:form>
        </div> <!-- /.Content page -->
    </div> <!-- /.Page-content -->
</div> <!-- /. Page-content-wrapper -->

<!-- LOAD JAVASCRIPT -->
<asset:javascript src="confirmation/bootstrap-confirmation.min.js"/>
<asset:javascript src="confirmation/custom-delete.js"/>
<asset:javascript src="iCheck/icheck.min.js"/>
<asset:javascript src="maxLength/bootstrap-maxlength.min.js"/>
<asset:javascript src="customIcons/user-handler.js"/>
<asset:javascript src="domain-validation/userSelectEdit-validation.js"/>

</body>
</html>