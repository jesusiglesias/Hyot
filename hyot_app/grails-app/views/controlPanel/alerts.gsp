<!DOCTYPE html>
<html>
<head>
    <meta name="layout" content="main_controlpanel">
    <title><g:message code="layouts.main_auth_admin.head.title.alert" default="HYOT | Alerts management"/></title>

    <!-- LOAD CSS -->
    <link rel="stylesheet" href="${resource(dir: 'css/datatable', file: 'datatables.css')}" type="text/css"/>
    <link rel="stylesheet" href="${resource(dir: 'css/datatable', file: 'datatables.bootstrap.css')}" type="text/css"/>
</head>

<body>

<script type="text/javascript">

    // Variables to use in javascript
    var _print = '${g.message(code:'layouts.main_auth_admin.content.print', default:'Print')}';
    var _copy = '${g.message(code: "layouts.main_auth_admin.content.copy", default: "Copy")}';
    var _pdf = '${g.message(code: "layouts.main_auth_admin.content.pdf", default: "PDF")}';
    var _csv = '${g.message(code: "layouts.main_auth_admin.content.csv", default: "CSV")}';
    var _columns = '${g.message(code: "layouts.main_auth_admin.content.columns", default: "Columns")}';
    var _restore = '${g.message(code: "layouts.main_auth_admin.content.restore", default: "Restore")}';
    var _alertFile = '${g.message(code: "layouts.main_auth_admin.content.alert.file", default: "HYOT_Alerts")}';
    var _alertTableTitle = '${g.message(code: "layouts.main_auth_admin.content.alert.tableTitle", default: "HYOT - Alerts management")}';
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
            <li class="nav-item active open">
                <a href="javascript:;" class="nav-link nav-toggle">
                    <i class="fa fa-bell"></i><span class="title"><g:message code="layouts.main_auth_admin.sidebar.alert" default="Alert"/></span>
                    <span class="selected"></span>
                    <span class="arrow open"></span>
                </a>
                <ul class="sub-menu">
                    <li class="nav-item active open">
                        <g:link uri="/alert" class="nav-link">
                            <i class="fa fa-list"></i>
                            <span class="title"><g:message code="layouts.main_auth_admin.sidebar.list" default="List"/></span>
                            <span class="selected"></span>
                        </g:link>
                    </li>
                </ul>
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
                    <span><g:message code="layouts.main_auth_admin.pageBreadcrumb.subtitle.alert" default="alert"/></span>
                </li>
            </ul>
        </div> <!-- /.Page-bar -->

        <!-- Page-title -->
        <h3 class="page-title">
            <g:link uri="/alert"><g:message code="layouts.main_auth_admin.body.title.alert" default="alerts management"/></g:link>
            <i class="icon-arrow-right icon-title-domain"></i>
            <small><g:message code="layouts.main_auth_admin.body.subtitle.alert" default="Alerts list"/></small>
        </h3>

        <!-- Contain page -->
        <div id="list-domain">

            <div class="row">
                <div class="col-md-12">
                    <!-- Portlet -->
                    <div class="portlet light bg-inverse bordered">
                        <div class="portlet-title">
                            <div class="tools"> </div>
                        </div>

                        <div class="portlet-body">
                            <table class="table table-striped table-bordered table-hover table-alert" id="entity-table">
                                <thead>
                                <tr>
                                    <td><g:message code="layouts.main_auth_admin.body.alert.id" default="ID"/></td>
                                    <td><g:message code="layouts.main_auth_admin.body.alert.timestamp" default="Timestamp"/></td>
                                    <td><g:message code="layouts.main_auth_admin.body.alert.sensorOrigin" default="Sensor"/></td>
                                    <td><g:message code="layouts.main_auth_admin.body.alert.eventOrigin" default="Event"/></td>
                                    <td><g:message code="layouts.main_auth_admin.body.alert.hash" default="Hash"/></td>
                                    <td><g:message code="layouts.main_auth_admin.body.alert.link" default="Link"/></td>
                                    <td><g:message code="layouts.main_auth_admin.body.alert.owner" default="Owner"/></td>
                                </tr>
                                </thead>
                                <tbody>
                                    <g:each in="${alerts}" status="i" var="alert">
                                        <tr class="${(i % 2) == 0 ? 'even' : 'odd'}">
                                            <td class="break-word">${alert?.alert_id}</td>
                                            <td class="break-word">${alert?.alert_details?.timestamp}</td>
                                            <td class="break-word">${alert?.alert_details?.sensor_origin}</td>
                                            <td class="break-word">${alert?.alert_details?.event_origin}</td>
                                            <td class="break-word">${alert?.alert_details?.hash}</td>
                                            <td class="break-word">${alert?.alert_details?.link}</td>
                                            <td class="break-word">${alert?.alert_details?.owner?.replaceAll('resource:org.hyot.network.User#', '')}</td>
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
<asset:javascript src="datatable/customAlert-datatable.js"/>

</body>
</html>