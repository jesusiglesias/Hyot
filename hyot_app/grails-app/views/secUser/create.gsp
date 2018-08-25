<%@ page import="org.springframework.validation.FieldError" %>
<!DOCTYPE html>
<html>
<head>
    <meta name="layout" content="main_controlpanel">
    <title><g:message code="layouts.main_auth_admin.head.title.admin" default="HYOT | Administrators management"/></title>
    <link rel="stylesheet" href="${resource(dir: 'css/iCheck', file: 'green.css')}" type="text/css"/>
    <link rel="stylesheet" href="${resource(dir: 'css/fileInput', file: 'bootstrap-fileinput.css')}" type="text/css"/>

    <script>
        // Variables to use in script
        var _weak = '${g.message(code:'default.password.strength.weak', default:'Weak')}';
        var _normal = '${g.message(code:'default.password.strength.normal', default:'Normal')}';
        var _medium = '${g.message(code:'default.password.strength.medium', default:'Medium')}';
        var _strong = '${g.message(code:'default.password.strength.strong', default:'Strong')}';
        var _veryStrong = '${g.message(code:'default.password.strength.veryStrong', default:'Very strong')}';
        var _checkerUsernameBlockInfo = '${g.message(code:'layouts.main_auth_admin.body.content.admin.create.checker.block.info.username', default:'Type an username and check its availability.')}';
        var _checkUsernameAvailibility = '${g.createLink(controller: "secUser", action: 'checkUsernameAvailibility')}';
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
            <li class="nav-item active open">
                <a href="javascript:;" class="nav-link nav-toggle">
                    <i class="fa fa-user-secret"></i>
                    <span class="title"><g:message code="layouts.main_auth_admin.sidebar.admin" default="Administrator user"/></span>
                    <span class="selected"></span>
                    <span class="arrow open"></span>
                </a>
                <ul class="sub-menu">
                    <li class="nav-item active open">
                        <g:link uri="/administrator/create" class="nav-link">
                            <i class="fa fa-user-plus"></i>
                            <span class="title"><g:message code="layouts.main_auth_admin.sidebar.new" default="New"/></span>
                            <span class="selected"></span>
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
            <li class="nav-item">
                <a href="javascript:;" class="nav-link nav-toggle">
                    <i class="fa fa-user"></i>
                    <span class="title"><g:message code="layouts.main_auth_admin.sidebar.normalUser" default="Normal user"/></span>
                    <span class="arrow"></span>
                </a>
                <ul class="sub-menu">
                    <li class="nav-item">
                        <g:link uri="/user/create" class="nav-link">
                            <i class="fa fa-user-plus"></i>
                            <span class="title"><g:message code="layouts.main_auth_admin.sidebar.new" default="New"/></span>
                        </g:link>
                    </li>
                    <li class="nav-item">
                        <g:link uri="/user" class="nav-link">
                            <i class="fa fa-list"></i>
                            <span class="title"><g:message code="layouts.main_auth_admin.sidebar.list" default="List"/></span>
                        </g:link>
                    </li>
                </ul>
            </li>
            <!-- /.USERS -->

            <!-- GENERAL -->
            <li class="heading">
                <h3 class="uppercase"><g:message code="layouts.main_auth_admin.sidebar.title.general" default="General"/></h3>
            </li>

            <!-- Measurements -->
            <li class="nav-item">
                <a href="javascript:;" class="nav-link nav-toggle">
                    <i class="fa fa-archive"></i>
                    <span class="title"><g:message code="layouts.main_auth_admin.sidebar.measurement" default="Measurement"/></span>
                    <span class="arrow"></span>
                </a>
                <ul class="sub-menu">
                    <li class="nav-item">
                        <g:link uri="/measurement" class="nav-link">
                            <i class="fa fa-list"></i>
                            <span class="title"><g:message code="layouts.main_auth_admin.sidebar.list" default="List"/></span>
                        </g:link>
                    </li>
                </ul>
            </li>

            <!-- Alerts -->
            <li class="nav-item">
                <a href="javascript:;" class="nav-link nav-toggle">
                    <i class="fa fa-bell"></i><span class="title"><g:message code="layouts.main_auth_admin.sidebar.alert" default="Alert"/></span>
                    <span class="arrow"></span>
                </a>
                <ul class="sub-menu">
                    <li class="nav-item">
                        <g:link uri="/alert" class="nav-link">
                            <i class="fa fa-list"></i>
                            <span class="title"><g:message code="layouts.main_auth_admin.sidebar.list" default="List"/></span>
                        </g:link>
                    </li>
                </ul>
            </li>

            <!-- /.GENERAL -->
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
                    <span><g:message code="layouts.main_auth_admin.pageBreadcrumb.subtitle.admin" default="administrator user"/></span>
                </li>
            </ul>
        </div> <!-- /.Page-bar -->

        <!-- Page-title -->
        <h3 class="page-title">
            <g:link uri="/administrator"><g:message code="layouts.main_auth_admin.body.title.admin" default="administrators management"/></g:link>
            <i class="icon-arrow-right icon-title-domain"></i>
            <small><g:message code="layouts.main_auth_admin.body.subtitle.admin.create" default="Create administrator"/></small>
        </h3>

        <!-- Contain page -->
        <div id="create-domain">

            <!-- Accordion -->
            <div class="portlet-body">
                <div class="panel-group accordion panel-instruction-create" id="accordionPassword">
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            <h4 class="panel-title">
                                <a class="accordion-toggle accordion-toggle-styled" data-toggle="collapse" data-parent="#accordionPassword" href="#collapsePassword"> <g:message code="views.login.auth.newPassword.description" default="New password instructions"/> </a>
                            </h4>
                        </div>
                        <div id="collapsePassword" class="panel-collapse collapse">
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

            <!-- Alerts -->
            <g:if test="${flash.secUserErrorMessage}">
                <div class='alert alert-error alert-danger-custom-backend alert-dismissable alert-entity-error fade in'>
                    <button type='button' class='close' data-dismiss='alert' aria-hidden='true'></button>
                    <span class="xthin" role="status"> ${raw(flash.secUserErrorMessage)} </span>
                </div>

                <g:javascript>
                    createAutoClosingAlert('.alert-entity-error');
                </g:javascript>
            </g:if>

            <!-- Error in validation -->
            <g:hasErrors bean="${secUser}">
                <div class='alert alert-error alert-danger-custom-backend alert-dismissable alert-entity-error fade in'>
                    <button type='button' class='close' data-dismiss='alert' aria-hidden='true'></button>
                    <g:eachError bean="${secUser}" var="error">
                        <p role="status" class="xthin" <g:if test="${error in FieldError}">data-field-id="${error.field}"</g:if>><g:message error="${error}"/></p>
                    </g:eachError>
                </div>

                <g:javascript>
                    createAutoClosingAlert('.alert-entity-error');
                </g:javascript>
            </g:hasErrors>

            <!-- Creation form -->
            <g:form url="[resource:secUser, action:'save']" enctype="multipart/form-data" autocomplete="on" class="horizontal-form admin-form">
                <fieldset class="form">
                    <g:render template="form"/>
                </fieldset>

                <div class="domain-button-group-less">
                    <!-- Cancel button -->
                    <g:link type="button" uri="/administrator" class="btn grey-mint"><g:message code="default.button.cancel.label" default="Cancel"/></g:link>
                    <button type="submit" class="btn green-dark icon-button-container" name="create">
                        <i class="fa fa-check icon-button"></i>
                        <g:message code="default.button.create.label" default="Create"/>
                    </button>
                </div>
            </g:form>
        </div> <!-- /.Content page -->
    </div> <!-- /.Page-content -->
</div> <!-- /. Page-content-wrapper -->

<!-- LOAD JAVASCRIPT -->
<asset:javascript src="iCheck/icheck.min.js"/>
<asset:javascript src="password/custom-password.js"/>
<asset:javascript src="password/pwstrength-bootstrap.min.js"/>
<asset:javascript src="maxLength/bootstrap-maxlength.min.js"/>
<asset:javascript src="customIcons/secUser-handler.js"/>
<asset:javascript src="domain-validation/admin-validation.js"/>
<asset:javascript src="fileInput/bootstrap-fileinput.js"/>

</body>
</html>
