<%@ page import="User.User" %>
<!DOCTYPE html>
<html>
<head>
    <meta name="layout" content="main_controlpanel">
    <title><g:message code="layouts.main_auth_admin.head.title.user" default="HYOT | Normal users management"/></title>

    <!-- LOAD CSS -->
    <link rel="stylesheet" href="${resource(dir: 'css/datatable', file: 'datatables.css')}" type="text/css"/>
    <link rel="stylesheet" href="${resource(dir: 'css/datatable', file: 'datatables.bootstrap.css')}" type="text/css"/>

    <script>
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

<!-- Search request from quick search -->
<g:if test="${params.quickSearch}">
    <script type="text/javascript">
        var _textSearch = '${params.quickSearch}'
    </script>
</g:if>
<g:else>
    <script type="text/javascript">
        var _textSearch = ''
    </script>
</g:else>

<script type="text/javascript">

    // Variables to use in javascript
    var _print = '${g.message(code:'layouts.main_auth_admin.content.print', default:'Print')}';
    var _copy = '${g.message(code: "layouts.main_auth_admin.content.copy", default: "Copy")}';
    var _pdf = '${g.message(code: "layouts.main_auth_admin.content.pdf", default: "PDF")}';
    var _csv = '${g.message(code: "layouts.main_auth_admin.content.csv", default: "CSV")}';
    var _columns = '${g.message(code: "layouts.main_auth_admin.content.columns", default: "Columns")}';
    var _restore = '${g.message(code: "layouts.main_auth_admin.content.restore", default: "Restore")}';
    var _userFile = '${g.message(code: "layouts.main_auth_admin.content.user.file", default: "HYOT_NormalUsers")}';
    var _userTableTitle = '${g.message(code: "layouts.main_auth_admin.content.user.tableTitle", default: "HYOT - Normal users management")}';
    var _search = '${g.message(code: "layouts.main_auth_admin.content.search", default: "Search:")}';
    var _sortAscending = '${g.message(code: "layouts.main_auth_admin.content.sortAscending", default: ": activate to sort column ascending")}';
    var _sortDescending = '${g.message(code: "layouts.main_auth_admin.content.sortDescending", default: ": activate to sort column descending")}';
    var _emptyTable = '${g.message(code: "layouts.main_auth_admin.content.emptyTable", default: "No data available in table")}';
    var _zeroRecords = '${g.message(code: "layouts.main_auth_admin.content.zeroRecords", default: "No matching records found")}';
    var _processing = '${g.message(code: "layouts.main_auth_admin.content.processing", default: "Processing...")}';
    var _infoThousands = '${g.message(code: "layouts.main_auth_admin.content.infoThousands", default: ",")}';
    var _loadingRecords = '${g.message(code: "layouts.main_auth_admin.content.loadingRecords", default: "Loading...")}';
    var _first = '${g.message(code: "layouts.main_auth_admin.content.pagination.first", default: "First")}';
    var _last = '${g.message(code: "layouts.main_auth_admin.content.pagination.last", default: "Last")}';
    var _next = '${g.message(code: "layouts.main_auth_admin.content.pagination.next", default: "Next")}';
    var _previous = '${g.message(code: "layouts.main_auth_admin.content.pagination.previous", default: "Previous")}';
    var _lengthMenu = '${g.message(code: "layouts.main_auth_admin.content.lengthMenu", default: "Show _MENU_ entries")}';
    var _info = '${g.message(code: "layouts.main_auth_admin.content.info", default: "Showing _START_ to _END_ of _TOTAL_ entries")}';
    var _infoEmpty = '${g.message(code: "layouts.main_auth_admin.content.infoEmpty", default: "No entries found")}';
    var _infoFiltered = '${g.message(code: "layouts.main_auth_admin.content.infoFiltered", default: "(filtered from _MAX_ total entries)")}';
    var _all = '${g.message(code: "layouts.main_auth_admin.content.all", default: "All")}';
    var _page = '${g.message(code: "layouts.main_auth_admin.content.bootstrap.page", default: "Page")}';
    var _pageOf = '${g.message(code: "layouts.main_auth_admin.content.bootstrap.pageOf", default: "of")}';
    var _clipboard = '${g.message(code: "layouts.main_auth_admin.content.clipboard", default: "Copy to clipboard")}';
    var _rows = '${g.message(code: "layouts.main_auth_admin.content.rows", default: "Copied %d rows to clipboard")}';
    var _row = '${g.message(code: "layouts.main_auth_admin.content.row", default: "Copied 1 row to clipboard")}';

</script>

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

            <!-- GENERAL TODO -->
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
                    <span><g:message code="layouts.main_auth_admin.pageBreadcrumb.subtitle.user" default="normal user"/></span>
                </li>
            </ul>
        </div> <!-- /.Page-bar -->

        <!-- Page-title -->
        <h3 class="page-title">
            <g:link uri="/user"><g:message code="layouts.main_auth_admin.body.title.user" default="normal users management"/></g:link>
            <i class="icon-arrow-right icon-title-domain"></i>
            <small><g:message code="layouts.main_auth_admin.body.subtitle.user" default="Normal users list"/></small>
        </h3>

        <!-- Contain page -->
        <div id="list-domain">

            <!-- Alerts -->
            <g:if test="${flash.userMessage}">
                <div class='alert alert-info alert-info-custom-backend alert-dismissable alert-entity fade in'>
                    <button type='button' class='close' data-dismiss='alert' aria-hidden='true'></button>
                    <span class="xthin" role="status"> ${raw(flash.userMessage)} </span>
                </div>

                <g:javascript>
                    createAutoClosingAlert('.alert-entity');
                </g:javascript>
            </g:if>

            <g:if test="${flash.userErrorMessage}">
                <div class='alert alert-error alert-danger-custom-backend alert-dismissable alert-entity fade in'>
                    <button type='button' class='close' data-dismiss='alert' aria-hidden='true'></button>
                    <span class="xthin" role="status"> ${raw(flash.userErrorMessage)} </span>
                </div>

                <g:javascript>
                    createAutoClosingAlert('.alert-entity');
                </g:javascript>
            </g:if>

            <div class="row">
                <div class="col-md-12">
                    <!-- Portlet -->
                    <div class="portlet light bg-inverse bordered">
                        <div class="portlet-title">
                            <div class="caption font-green-dark">
                                <div class="btn-group">
                                    <g:link uri="/user/create" class="btn green-dark icon-button-container">
                                        <i class="fa fa-plus icon-button"></i>
                                        <g:message code="layouts.main_auth_admin.body.content.user.new" default="New normal user"/>
                                    </g:link>
                                </div>
                            </div>
                            <div class="tools"> </div>
                        </div>

                        <div class="portlet-body">
                            <table class="table table-striped table-bordered table-hover table-user" id="entity-table">
                                <thead>
                                <tr>
                                    <td><g:message code="user.avatar.label" default="Profile image"/></td>
                                    <td><g:message code="user.username.label" default="Username"/></td>
                                    <td><g:message code="user.email.label" default="Email"/></td>
                                    <td><g:message code="user.enabled.label" default="Enabled account"/></td>
                                    <td><g:message code="user.accountLocked.label" default="Locked account"/></td>
                                    <td><g:message code="user.accountExpired.label" default="Expired account"/></td>
                                    <td><g:message code="user.passwordExpired.label" default="Expired password"/></td>
                                    <td><g:message code="user.name.label" default="Name"/></td>
                                    <td><g:message code="user.surname.label" default="Surname"/></td>
                                </tr>
                                </thead>
                                <tbody>
                                <g:each in="${userList}" status="i" var="userInstance">
                                    <tr class="${(i % 2) == 0 ? 'even' : 'odd'}">
                                        <td>
                                            <g:if test="${userInstance?.avatar}">
                                                <g:link controller="user" action="editProfileImage" id="${userInstance.id}">
                                                    <img class="img-circle profileImage-view" alt="Profile image"  src="${createLink(controller:'controlPanel', action:'profileImage', id:userInstance.ident())}" />
                                                </g:link>
                                            </g:if>
                                            <g:else>
                                                <g:link controller="user" action="editProfileImage" id="${userInstance.id}">
                                                    <img class="img-circle profileImage-view" alt="Profile image" src="${resource(dir: 'img/profile', file: 'user_profile.png')}"/>
                                                </g:link>
                                            </g:else>
                                        </td>
                                        <td><g:link controller="user" action="edit" id="${userInstance.id}" class="break-word">${fieldValue(bean: userInstance, field: "username")}</g:link></td>
                                        <td class="break-word">${fieldValue(bean: userInstance, field: "email")}</td>
                                        <td>
                                            <g:if test="${userInstance.enabled}">
                                                <span class="label label-sm label-success">
                                            </g:if>
                                            <g:else>
                                                <span class="label label-sm label-info">
                                            </g:else>
                                            <g:formatBoolean boolean="${userInstance.enabled}" true="${g.message(code: "default.enabled.label.true", default: "Confirmed")}" false="${g.message(code: "default.enabled.label.false", default: "Pending")}"/>
                                        </span>
                                        </td>
                                        <td>
                                            <g:if test="${userInstance.accountLocked}">
                                                <span class="label label-sm label-danger">
                                            </g:if>
                                            <g:else>
                                                <span class="label label-sm label-success">
                                            </g:else>
                                            <g:formatBoolean boolean="${userInstance.accountLocked}" true="${g.message(code: "default.locked.label.true", default: "Locked")}" false="${g.message(code: "default.expiredLocked.label.false", default: "Active")}"/>
                                        </span>
                                        </td>
                                        <td>
                                            <g:if test="${userInstance.accountExpired}">
                                                <span class="label label-sm label-warning">
                                            </g:if>
                                            <g:else>
                                                <span class="label label-sm label-success">
                                            </g:else>
                                            <g:formatBoolean boolean="${userInstance.accountExpired}" true="${g.message(code: "default.expired.label.true", default: "Expired")}" false="${g.message(code: "default.expiredLocked.label.false", default: "Active")}"/>
                                        </span>
                                        </td>
                                        <td>
                                            <g:if test="${userInstance.passwordExpired}">
                                                <span class="label label-sm label-warning">
                                            </g:if>
                                            <g:else>
                                                <span class="label label-sm label-success">
                                            </g:else>
                                            <g:formatBoolean boolean="${userInstance.passwordExpired}" true="${g.message(code: "default.expired.label.true", default: "Expired")}" false="${g.message(code: "default.expiredLocked.label.false", default: "Active")}"/>
                                        </span>
                                        </td>
                                        <td class="break-word">${fieldValue(bean: userInstance, field: "name")}</td>
                                        <td class="break-word">${fieldValue(bean: userInstance, field: "surname")}</td>
                                    </tr>
                                </g:each>
                                </tbody>
                            </table>
                        </div> <!-- /.Portlet-body -->
                    </div> <!-- /.Portlet -->
                </div>
            </div>
        </div> <!-- /.Content page -->
    </div> <!-- /.Page-content -->
</div> <!-- /. Page-content-wrapper -->

<!-- LOAD JAVASCRIPT -->
<asset:javascript src="datatable/datatables.js"/>
<asset:javascript src="datatable/datatables.bootstrap.js"/>
<asset:javascript src="datatable/customUser-datatable.js"/>

</body>
</html>