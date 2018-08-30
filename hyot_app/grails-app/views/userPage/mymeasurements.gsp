<!DOCTYPE html>
<html>
<head>
    <meta name="layout" content="main_userpage">
    <title><g:message code="layouts.main_userpage.head.title.mymeasurements" default="HYOT | My measurements"/></title>

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
        var _mymeasurementFile = '${g.message(code: "layouts.main_auth_admin.content.mymeasurements.file", default: "HYOT_MyMeasurements")}';
        var _mymeasurementTableTitle = '${g.message(code: "layouts.main_auth_admin.content.mymeasurements.tableTitle", default: "HYOT - My measurements")}';
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

    <!-- Horizontal menu -->
    <content tag="horizontalMenu">
        <div class="hor-menu hidden-sm hidden-xs">
            <ul class="nav navbar-nav">
                <li class="active">
                    <g:link uri="/mymeasurements"><g:message code="layout.main_userpage.horizontal.menu.measurement" default="My measurements"/>
                        <span class="selected"></span>
                    </g:link>
                </li>
                <li>
                    <g:link uri="/myalerts"><g:message code="layout.main_userpage.horizontal.menu.alert" default="My alerts"/></g:link>
                </li>
            </ul>
        </div>
    </content>

    <!-- Responsive horizontal menu -->
    <content tag="responsiveHorizontalMenu">
        <li class="nav-item active">
            <g:link uri="/mymeasurements" class="nav-link">
                <i class="fa fa-archive"></i>
                <span class="title"><g:message code="layout.main_userpage.horizontal.menu.measurement" default="My measurements"/></span>
                <span class="selected"></span>
                <span class="arrow"></span>
            </g:link>
        </li>
        <li class="nav-item">
            <g:link uri="/myalerts" class="nav-link">
                <i class="fa fa-bell"></i>
                <span class="title"><g:message code="layout.main_userpage.horizontal.menu.alert" default="My alerts"/></span>
                <span class="arrow"></span>
            </g:link>
        </li>
        <li class="nav-item">
    </content>

    <!-- Page-bar -->
    <div class="page-bar-user">
        <ul class="page-breadcrumb">
            <li>
                <i class="icon-home"></i>
                <g:link uri="/"><g:message code="layouts.main_auth_admin.pageBreadcrumb.title" default="Homepage"/></g:link>
                <i class="fa fa-circle"></i>
            </li>
            <li>
                <span><g:message code="layout.main_userpage.horizontal.menu.measurement" default="My measurements"/></span>
            </li>
        </ul>
    </div> <!-- /.Page-bar -->

    <!-- Page-title -->
    <div class="row row-userLayoutTitle">
        <div class="col-md-12 col-userLayoutTitle">
            <!-- Page-title -->
            <div class="page-title-user-home">
                <h3 class="page-title-user-home-title">
                    ${raw(g.message(code:"layouts.main_userpage.body.title.home", default:"Welcome to <span>HYOT</span>!"))}
                </h3>
                <p class="page-title-user-home-description">
                    ${raw(g.message(code:"layouts.main_userpage.body.title.home.description", default:"The proof of concept for the traceability of an IoT environment by Hyperledger"))}
                </p>
            </div>
        </div>
    </div>

    <div class="row row-userLayoutTitle-home">
        <div class="col-md-12 col-userLayoutTitle">
            <!-- Page-title -->
            <div class="page-title-user-show-section">
                <h3 class="page-title-user-show-section-title hvr-bubble-float-bottom">
                    <g:message code="layout.main_userpage.horizontal.menu.measurement" default="My measurements"/>
                </h3>
            </div>
        </div>
    </div>

    <!-- Contain page -->
    <div id="list-domain">

        <div class="row">
            <div class="col-xs-10 col-xs-push-1">
                <!-- Portlet -->
                <div class="portlet light bordered">
                    <div class="portlet-title">
                        <div class="tools"> </div>
                    </div>

                    <div class="portlet-body">
                        <table class="table table-striped table-bordered table-hover table-user" id="entity-table">
                            <thead>
                            <tr>
                                <td><g:message code="layouts.main_auth_admin.body.measurement.id" default="ID"/></td>
                                <td><g:message code="layouts.main_auth_admin.body.measurement.timestamp" default="Timestamp"/></td>
                                <td><g:message code="layouts.main_auth_admin.body.measurement.temperature" default="Temperature"/></td>
                                <td><g:message code="layouts.main_auth_admin.body.measurement.humidity" default="Humidity"/></td>
                                <td><g:message code="layouts.main_auth_admin.body.measurement.distance" default="Distance"/></td>
                                <td><g:message code="layouts.main_auth_admin.body.measurement.alertTriggered" default="Alert triggered"/></td>
                                <td><g:message code="layouts.main_auth_admin.body.measurement.sensorOrigin" default="Sensor"/></td>
                                <td><g:message code="layouts.main_auth_admin.body.measurement.eventOrigin" default="Event"/></td>
                                <td><g:message code="layouts.main_auth_admin.body.measurement.threshold" default="Threshold"/></td>
                                <td><g:message code="layouts.main_auth_admin.body.measurement.link" default="Link"/></td>
                                <td><g:message code="layouts.main_auth_admin.body.measurement.mailto" default="Mailto"/></td>
                            </tr>
                            </thead>
                            <tbody>
                            <g:each in="${mymeasurements}" status="i" var="measurement">
                                <tr class="${(i % 2) == 0 ? 'even' : 'odd'}">
                                    <td class="break-word">${measurement?._id}</td>
                                    <td class="break-word">${measurement?.datetime_field}</td>
                                    <td class="break-word">${measurement?.temperature_field}</td>
                                    <td class="break-word">${measurement?.humidity_field}</td>
                                    <td class="break-word">${measurement?.distance_field}</td>
                                    <td>
                                        <g:if test="${measurement?.alert_triggered == true}">
                                            <span class="label label-sm label-success">
                                        </g:if>
                                        <g:else>
                                            <span class="label label-sm label-warning">
                                        </g:else>
                                        <g:formatBoolean boolean="${measurement?.alert_triggered}"/>
                                    </span>
                                    </td>
                                    <td class="break-word">${measurement?.sensor_origin}</td>
                                    <td class="break-word">${measurement?.event_origin}</td>
                                    <td class="break-word">${measurement?.threshold_value}</td>
                                    <td class="break-word">${measurement?.link}</td>
                                    <td class="break-word">${measurement?.mailto}</td>
                                </tr>
                            </g:each>
                            </tbody>
                        </table>
                    </div> <!-- /.Portlet-body -->
                </div> <!-- /.Portlet -->
            </div>
        </div>
    </div> <!-- /.Content page -->

    <!-- LOAD JAVASCRIPT -->
    <asset:javascript src="datatable/datatables.js"/>
    <asset:javascript src="datatable/datatables.bootstrap.js"/>
    <asset:javascript src="datatable/customMyMeasurements-datatable.js"/>

</body>
</html>