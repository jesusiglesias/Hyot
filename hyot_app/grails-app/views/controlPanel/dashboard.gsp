<!DOCTYPE html>
<html>
<head>
    <meta name="layout" content="main_controlpanel">
    <title><g:message code="layouts.main_auth_admin.head.title" default="HYOT | Control panel"/></title>
    <link rel="stylesheet" href="${resource(dir: 'css/select', file: 'bootstrap-select.min.css')}" type="text/css"/>
</head>

<body>

<script type="text/javascript">
    // Variables to use in javascript
    var fullscreenTooltip = '${g.message(code:'layouts.main_auth_admin.body.content.tooltip.fullscreen', default:'Fullscreen!')}';
    var removeTooltip = '${g.message(code:'layouts.main_auth_admin.body.content.tooltip.remove', default:'Remove')}';
    var collapseTooltip = '${g.message(code:'layouts.main_auth_admin.body.content.tooltip.collapse', default:'Collapse/Expand')}';
    var reloadTooltip = '${g.message(code:'default.button.reload.tooltip', default:'Reload')}';
    var reloadAjaxError = '${g.message(code:'default.ajax.error', default:'Error on reloading the content. Please, you try again later.')}';
    var reloadNormalUserURL = '${g.createLink(controller: "controlPanel", action: 'reloadNormalUser')}';
    var reloadAdminURL = '${g.createLink(controller: "controlPanel", action: 'reloadAdmin')}';
</script>

<!-- Page-sidebar-wrapper -->
<div class="page-sidebar-wrapper">
    <!-- Page-sidebar -->
    <div class="page-sidebar navbar-collapse collapse">
        <!-- Page-sidebar-menu -->
        <ul class="page-sidebar-menu page-header-fixed" data-keep-expanded="true" data-auto-scroll="true" data-slide-speed="200" style="padding-top: 30px">

            <!-- Load search action TODO -->
            <g:render template="./searchControlPanel"/>

            <li class="nav-item start active open">
                <a href="javascript:;" class="nav-link nav-toggle">
                    <i class="icon-home"></i>
                    <span class="title"><g:message code="layouts.main_auth_admin.sidebar.title.dashboard" default="Dashboard"/></span>
                    <span class="selected"></span>
                    <span class="arrow open"></span>
                </a>
                <ul class="sub-menu">
                    <li class="nav-item start active open">
                        <g:link controller="controlPanel" action="dashboard" class="nav-link">
                            <i class="icofont icofont-dashboard-web"></i>
                            <span class="title"><g:message code="layouts.main_auth_admin.sidebar.title.dashboard.statistics" default="Statistics"/></span>
                            <span class="selected"></span>
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
                    <span class="title"><g:message code="layouts.main_auth_admin.sidebar.admin" default="Admin user"/></span>
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
                        <g:link controller="user" action="create" class="nav-link">
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
                    <span><g:message code="layouts.main_auth_admin.pageBreadcrumb.subtitle.dashboard" default="dashboard & statistics"/></span>
                </li>
            </ul>
        </div> <!-- /.Page-bar -->

    <!-- Page-title -->
        <h3 class="page-title">
            <g:link controller="controlPanel" action="dashboard"><g:message code="layouts.main_auth_admin.body.title.controlPanel" default="control panel"/></g:link>
            <i class="icon-arrow-right icon-title-domain"></i>
            <small class="subtitle-inlinePage"><g:message code="layouts.main_auth_admin.body.subtitle.controlPanel" default="Statistics"/></small>
        </h3>

        <!-- Contain page -->
        <div id="list-panel">

            <!-- Widget -->
            <div class="row panel-row-dashboard">
                <div class="col-md-6">
                    <!-- Widget thumb -->
                    <div class="widget-thumb widget-bg-color-white text-uppercase margin-bottom-20 bordered widget-admin">
                        <h4 class="widget-thumb-heading"><g:message code="layouts.main_auth_admin.body.widget.admin" default="Admin users"/></h4>
                        <i class="fa fa-refresh iconReload reloadAdmin"></i>
                        <div class="widget-thumb-wrap">
                            <i class="widget-thumb-icon bg-yellow-saffron icon-user"></i>
                            <div class="widget-thumb-body">
                                <span class="widget-thumb-subtitle"><g:message code="layouts.main_auth_admin.body.widget.total" default="Total"/></span>
                                <span class="widget-thumb-body-stat counterAdmin" data-counter="counterup" data-value="${adminUsers}">${adminUsers}</span>
                            </div>
                        </div>
                    </div> <!-- /.Widget thumb -->
                </div>
                <div class="col-md-6">
                    <!-- Widget thumb -->
                    <div class="widget-thumb widget-bg-color-white text-uppercase margin-bottom-20 bordered widget-normaluser">
                        <h4 class="widget-thumb-heading"><g:message code="layouts.main_auth_admin.body.widget.user" default="Normal users"/></h4>
                        <i class="fa fa-refresh iconReload reloadNormalUser"></i>
                        <div class="widget-thumb-wrap">
                            <i class="widget-thumb-icon bg-green-dark icon-user"></i>
                            <div class="widget-thumb-body">
                                <span class="widget-thumb-subtitle"><g:message code="layouts.main_auth_admin.body.widget.total" default="Total"/></span>
                                <span class="widget-thumb-body-stat counterNormalUser" data-counter="counterup" data-value="${normalUsers}">${normalUsers}</span>
                            </div>
                        </div>
                    </div> <!-- /.Widget thumb -->
                </div>
            </div>

            <div class="row panel-row-dashboard">
           <!-- TODO     <div class="col-md-6">
                    <!-- Widget thumb
                    <div class="widget-thumb widget-bg-color-white text-uppercase margin-bottom-20 bordered widget-event">
                        <h4 class="widget-thumb-heading"><g:message code="layouts.main_auth_admin.body.widget.event" default="Events"/></h4>
                        <i class="fa fa-refresh iconReload reloadEvent"></i>
                        <div class="widget-thumb-wrap">
                            <i class="widget-thumb-icon bg-blue-steel icofont icofont-paper"></i>
                            <div class="widget-thumb-body">
                                <span class="widget-thumb-subtitle"><g:message code="layouts.main_auth_admin.body.widget.total" default="Total"/></span>
                                <span class="widget-thumb-body-stat counterEvent" data-counter="counterup" data-value="${events}">${events}</span>
                            </div>
                        </div>
                    </div> <!-- /.Widget thumb
                </div> -->
           <!--  TODO   <div class="col-md-6">
                    <!-- Widget thumb
                    <div class="widget-thumb widget-bg-color-white text-uppercase margin-bottom-20 bordered widget-booking">
                        <h4 class="widget-thumb-heading"><g:message code="layouts.main_auth_admin.body.widget.booking" default="Bookings"/></h4>
                        <i class="fa fa-refresh iconReload reloadBooking"></i>
                        <div class="widget-thumb-wrap">
                            <i class="widget-thumb-icon bg-red icon-note"></i>
                            <div class="widget-thumb-body">
                                <span class="widget-thumb-subtitle"><g:message code="layouts.main_auth_admin.body.widget.total" default="Total"/></span>
                                <span class="widget-thumb-body-stat counterBooking" data-counter="counterup" data-value="${bookings}">${bookings}</span>
                            </div>
                        </div>
                    </div> <!-- /.Widget thumb
                </div> -->

            </div> <!-- /.Widget -->

            <!-- Graphs -->
            <div class="row">

                <!-- Last 10 users registered -->
                <div class="col-md-6">
                    <!-- Portlet -->
                    <div class="portlet light bg-inverse portlet-users">
                        <div class="portlet-title">
                            <div class="caption font-green-dark">
                                <i class="icon-people font-green-dark"></i>
                                <span class="caption-subject xthin uppercase"><g:message code="layouts.main_auth_admin.body.portlet.recentUsers" default="Recent users"/></span>
                            </div>
                            <div class="tools">
                                <i class="fa fa-refresh reloadGraph reloadLastUsers"></i>
                                <a href="" class="collapse"> </a>
                                <a href="" class="remove"> </a>
                            </div>
                        </div>
                        <div class="portlet-body">
                            <div class="scroller" style="height:505px" data-rail-visible="1" data-rail-color="#105d41" data-handle-color="#4A9F60">
                                <div class="content-lastUsers">
                                    <g:render template="lastUsers"  model="['lastUsers':lastUsers]"/>
                                </div>
                            </div>
                        </div>
                    </div> <!-- /.Portlet -->
                </div>
            </div> <!-- /.Graphs -->
        </div>
    </div> <!-- Page-content -->
</div> <!-- /. Page-content-wrapper -->

<!-- LOAD JAVASCRIPT -->
<asset:javascript src="select/bootstrap-select.min.js"/>
<asset:javascript src="select/boostrap-select_i18n/defaults-es_CL.min.js"/>
<asset:javascript src="custom/dashboard.js"/>
<script src="//cdnjs.cloudflare.com/ajax/libs/waypoints/2.0.3/waypoints.min.js"></script>
<asset:javascript src="counter/jquery.counterup.min.js"/>
<asset:javascript src="overlay/loadingoverlay.min.js"/>

</body>
</html>