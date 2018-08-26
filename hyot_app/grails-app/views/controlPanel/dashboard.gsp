<!DOCTYPE html>
<html>
<head>
    <meta name="layout" content="main_controlpanel">
    <title><g:message code="layouts.main_auth_admin.head.title" default="HYOT | Control panel"/></title>
    <link rel="stylesheet" href="${resource(dir: 'css/select', file: 'bootstrap-select.min.css')}" type="text/css"/>

    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>

    <script>
        var _sensorDHT = '${g.message(code: "layouts.main_auth_admin.body.portlet.alertSensor.dht11", default: "DHT11")}';
        var _sensorHCSR = '${g.message(code: "layouts.main_auth_admin.body.portlet.alertSensor.hcsr04", default: "HCSR-04")}';
        var _sensorTEM = '${g.message(code: "layouts.main_auth_admin.body.portlet.alertEvent.temperature", default: "Temperature")}';
        var _sensorHUM = '${g.message(code: "layouts.main_auth_admin.body.portlet.alertEvent.humidity", default: "Humidity")}';
        var _sensorDIS = '${g.message(code: "layouts.main_auth_admin.body.portlet.alertEvent.distance", default: "Distance")}';
        var _measurementsTitle = '${g.message(code: "layouts.main_auth_admin.body.portlet.measurements.title", default: "Measurements")}';
        var _measurementsSubtitle = '${g.message(code: "layouts.main_auth_admin.body.portlet.measurements.title", default: "Total of measurements")}';
        var _alertsTitle = '${g.message(code: "layouts.main_auth_admin.body.portlet.alerts.title", default: "Alerts")}';
        var _alertsSubtitle = '${g.message(code: "layouts.main_auth_admin.body.portlet.alerts.subtitle", default: "Total of alerts")}';

        // Load the Visualization API and the piechart package.
        google.charts.load("current", {packages:['corechart']});

        // Set a callback to run when the Google Visualization API is loaded.
        google.setOnLoadCallback(drawVisualization);

        var dataJSON_AlertSensor, dataJSON_AlertEvent, dataJSON_MAU;

        // Auto close alert
        function createAutoClosingAlert(selector) {
            var messageAlert = $(selector);
            window.setTimeout(function() {
                messageAlert.slideUp(1000, function(){
                    $(this).remove();
                });
            }, 5000);
        }

        function drawVisualization() {
            drawChartAlertSensor();
            drawChartAlertEvent();
            drawChartMeasurementAlertUser();
        }

        // It draws the column chart when the window resizes
        function drawChartResizeAlertSensor() {

            // Create the data table out of JSON data loaded from server
            var dataASResize = google.visualization.arrayToDataTable([
                [_alertsTitle, _alertsSubtitle, { role: "style" } ],
                [_sensorDHT, dataJSON_AlertSensor.dht, "#d6c152"],
                [_sensorHCSR, dataJSON_AlertSensor.hcsr, "#4eb48a"]
            ]);

            var chartHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0) + 'px';
            var chartWidth = Math.max(document.documentElement.clientWidth, window.innerWidth || 0) + 'px';

            var viewASResize = new google.visualization.DataView(dataASResize);

            viewASResize.setColumns([0, 1,
                { calc: "stringify",
                    sourceColumn: 1,
                    type: "string",
                    role: "annotation" },
                2]);

            var options = {
                chartArea: {width: '80%', height: '80%'},
                legend: "none",
                height: chartHeight,
                width: chartWidth,
                backgroundColor: {fill: "transparent"},
                vAxis: {
                    logScale: true, scaleType:"mirrorLog"
                }
            };

            // Instantiate and draw the chart, passing in some options
            var chartASResize =  new google.visualization.ColumnChart(document.getElementById('chart_AlertSensor'));
            chartASResize.draw(viewASResize, options);
        }

        // It draws the column chart when the window resizes
        function drawChartResizeAlertEvent() {

            // Create the data table out of JSON data loaded from server
            var dataAEResize = google.visualization.arrayToDataTable([
                [_alertsTitle, _alertsSubtitle, { role: "style" } ],
                [_sensorTEM, dataJSON_AlertEvent.temperature, "#5862d6"],
                [_sensorHUM, dataJSON_AlertEvent.humidity, "#b45665"],
                [_sensorDIS, dataJSON_AlertEvent.distance, "#b4a271"]
            ]);

            var chartHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0) + 'px';
            var chartWidth = Math.max(document.documentElement.clientWidth, window.innerWidth || 0) + 'px';

            var viewAEResize = new google.visualization.DataView(dataAEResize);

            viewAEResize.setColumns([0, 1,
                { calc: "stringify",
                    sourceColumn: 1,
                    type: "string",
                    role: "annotation" },
                2]);

            var options = {
                chartArea: {width: '80%', height: '80%'},
                legend: "none",
                height: chartHeight,
                width: chartWidth,
                backgroundColor: {fill: "transparent"},
                vAxis: {
                    logScale: true, scaleType:"mirrorLog"
                }
            };

            // Instantiate and draw the chart, passing in some options
            var chartAEResize =  new google.visualization.ColumnChart(document.getElementById('chart_AlertEvent'));
            chartAEResize.draw(viewAEResize, options);
        }

        // It draws the bubble chart when the window resizes
        function drawChartResizeMeasurementAlertUser() {

            var dataMAUResize = google.visualization.arrayToDataTable(dataJSON_MAU);


            var chartHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0) + 'px';
            var chartWidth = Math.max(document.documentElement.clientWidth, window.innerWidth || 0) + 'px';

            var viewMAUResize = new google.visualization.DataView(dataMAUResize);

            var options = {
                chartArea: {width: '80%', height: '80%'},
                legend: "none",
                height: chartHeight,
                width: chartWidth,
                backgroundColor: {fill: "transparent"},
                vAxis: {
                    title: _measurementsTitle,
                    titleTextStyle: {
                        italic: false
                    },
                    logScale: true, scaleType:"mirrorLog",
                    viewWindow: {
                        min: 0,
                        max: 50
                    }
                },
                hAxis: {
                    title: _alertsTitle,
                    titleTextStyle: {
                        italic: false
                    },
                    logScale: true, scaleType:"mirrorLog",
                    viewWindow: {
                        min: 0,
                        max: 50
                    }
                },
                sizeAxis: {
                    maxSize: 25
                },
                bubble: {
                    textStyle: {
                        fontSize: 12,
                        italic: false
                    }
                }
            };

            // Instantiate and draw the chart, passing in some options
            var chartMAUResize =  new google.visualization.BubbleChart(document.getElementById('chart_MeasurementAlertUser'));
            chartMAUResize.draw(viewMAUResize, options);
        }

        // It draws the column chart (alerts by sensor)
        function drawChartAlertSensor() {

            var contentChartAlertSensor = $('.portlet-graphAlertSensor');

            $.ajax({
                url: "${createLink(controller:'controlPanel', action:'alertBySensor')}",
                dataType: "json",
                beforeSend: function () {
                    contentChartAlertSensor.LoadingOverlay("show", {
                        image: "",
                        fontawesome: "fa fa-spinner fa-spin"
                    });
                },
                success: function (jsonDataAS) {
                    // It is used to resize
                    dataJSON_AlertSensor = jsonDataAS;

                    // Create the data table out of JSON data loaded from server
                    var dataAlertSensor = google.visualization.arrayToDataTable([
                        [_alertsTitle, _alertsSubtitle, { role: "style" } ],
                        [_sensorDHT, jsonDataAS.dht, "#d6c152"],
                        [_sensorHCSR, jsonDataAS.hcsr, "#4eb48a"]
                    ]);

                    var chartHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0) + 'px';
                    var chartWidth = Math.max(document.documentElement.clientWidth, window.innerWidth || 0) + 'px';

                    var viewAS = new google.visualization.DataView(dataAlertSensor);

                    viewAS.setColumns([0, 1,
                        { calc: "stringify",
                            sourceColumn: 1,
                            type: "string",
                            role: "annotation" },
                        2]);

                    var options = {
                        chartArea: {width: '80%', height: '80%'},
                        legend: "none",
                        height: chartHeight,
                        width: chartWidth,
                        backgroundColor: {fill: "transparent"},
                        vAxis: {
                            logScale: true, scaleType:"mirrorLog"
                        }
                    };

                    // Instantiate and draw the chart, passing in some options
                    var chartAS =  new google.visualization.ColumnChart(document.getElementById('chart_AlertSensor'));
                    chartAS.draw(viewAS, options);
                },
                error: function () {
                    var listMessageAS = $('.list-messageAS');

                    // Avoid duplicates
                    if (listMessageAS.length) {
                        listMessageAS.remove();
                    }

                    // Message
                    $('#chart_AlertSensor').prepend("<ul class='list-group list-messageAS'><li class='list-group-item bg-red-intense bg-font-red-intense' style='margin-right: -12px'>" + reloadAjaxError + "</li></ul>");
                    createAutoClosingAlert('.list-messageAS');
                },
                complete: function () {
                    setTimeout(function () {
                        contentChartAlertSensor.LoadingOverlay("hide");
                    }, 500);
                }
            });
        }

        // It draws the column chart (alerts by event)
        function drawChartAlertEvent() {

            var contentChartAlertEvent = $('.portlet-graphAlertEvent');

            $.ajax({
                url: "${createLink(controller:'controlPanel', action:'alertByEvent')}",
                dataType: "json",
                beforeSend: function () {
                    contentChartAlertEvent.LoadingOverlay("show", {
                        image: "",
                        fontawesome: "fa fa-spinner fa-spin"
                    });
                },
                success: function (jsonDataAE) {
                    // It is used to resize
                    dataJSON_AlertEvent = jsonDataAE;

                    // Create the data table out of JSON data loaded from server
                    var dataAlertEvent = google.visualization.arrayToDataTable([
                        [_alertsTitle, _alertsSubtitle, { role: "style" } ],
                        [_sensorTEM, jsonDataAE.temperature, "#5862d6"],
                        [_sensorHUM, jsonDataAE.humidity, "#b45665"],
                        [_sensorDIS, jsonDataAE.distance, "#b4a271"]
                    ]);

                    var chartHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0) + 'px';
                    var chartWidth = Math.max(document.documentElement.clientWidth, window.innerWidth || 0) + 'px';

                    var viewAE = new google.visualization.DataView(dataAlertEvent);

                    viewAE.setColumns([0, 1,
                        { calc: "stringify",
                            sourceColumn: 1,
                            type: "string",
                            role: "annotation" },
                        2]);

                    var options = {
                        chartArea: {width: '80%', height: '80%'},
                        legend: "none",
                        height: chartHeight,
                        width: chartWidth,
                        backgroundColor: {fill: "transparent"},
                        vAxis: {
                            logScale: true, scaleType:"mirrorLog"
                        }
                    };

                    // Instantiate and draw the chart, passing in some options
                    var chartAE =  new google.visualization.ColumnChart(document.getElementById('chart_AlertEvent'));
                    chartAE.draw(viewAE, options);
                },
                error: function () {
                    var listMessageAE = $('.list-messageAE');

                    // Avoid duplicates
                    if (listMessageAE.length) {
                        listMessageAE.remove();
                    }

                    // Message
                    $('#chart_AlertEvent').prepend("<ul class='list-group list-messageAE'><li class='list-group-item bg-red-intense bg-font-red-intense' style='margin-right: -12px'>" + reloadAjaxError + "</li></ul>");
                    createAutoClosingAlert('.list-messageAE');
                },
                complete: function () {
                    setTimeout(function () {
                        contentChartAlertEvent.LoadingOverlay("hide");
                    }, 500);
                }
            });
        }

        // It draws the bubble chart (measurements and alerts of each user)
        function drawChartMeasurementAlertUser() {

            var contentChartMeasurementAlertUser = $('.portlet-graphMeasurementAlertUser');

            $.ajax({
                url: "${createLink(controller:'controlPanel', action:'measurementAlertByUser')}",
                //dataType: "json",
                beforeSend: function () {
                    contentChartMeasurementAlertUser.LoadingOverlay("show", {
                        image: "",
                        fontawesome: "fa fa-spinner fa-spin"
                    });
                },
                success: function (dataMAU) {

                    dataJSON_MAU = dataMAU;

                    var dataMeasurementAlertUser = google.visualization.arrayToDataTable(dataMAU);

                    var chartHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0) + 'px';
                    var chartWidth = Math.max(document.documentElement.clientWidth, window.innerWidth || 0) + 'px';

                    var viewMAU = new google.visualization.DataView(dataMeasurementAlertUser);

                    var options = {
                        chartArea: {width: '80%', height: '80%'},
                        legend: "none",
                        height: chartHeight,
                        width: chartWidth,
                        backgroundColor: {fill: "transparent"},
                        vAxis: {
                            title: _measurementsTitle,
                            titleTextStyle: {
                                italic: false
                            },
                            logScale: true, scaleType:"mirrorLog",
                            viewWindow: {
                                min: 0,
                                max: 50
                            }
                        },
                        hAxis: {
                            title: _alertsTitle,
                            titleTextStyle: {
                                italic: false
                            },
                            logScale: true, scaleType:"mirrorLog",
                            viewWindow: {
                                min: 0,
                                max: 50
                            }
                        },
                        sizeAxis: {
                            maxSize: 25
                        },
                        bubble: {
                            textStyle: {
                                fontSize: 12,
                                italic: false
                            }
                        }
                    };

                    // Instantiate and draw the chart, passing in some options
                    var chartMAU =  new google.visualization.BubbleChart(document.getElementById('chart_MeasurementAlertUser'));
                    chartMAU.draw(viewMAU, options);
                },
                error: function () {
                    var listMessageMAU = $('.list-messageMAU');

                    // Avoid duplicates
                    if (listMessageMAU.length) {
                        listMessageMAU.remove();
                    }

                    // Message
                    $('#chart_MeasurementAlertUser').prepend("<ul class='list-group list-messageMAU'><li class='list-group-item bg-red-intense bg-font-red-intense' style='margin-right: -12px'>" + reloadAjaxError + "</li></ul>");
                    createAutoClosingAlert('.list-messageMAU');
                },
                complete: function () {
                    setTimeout(function () {
                        contentChartMeasurementAlertUser.LoadingOverlay("hide");
                    }, 500);
                }
            });
        }

        jQuery(document).ready(function() {
            // Resizing the column charts (alerts by sensor and alerts by event)
            $(window).resize(function(){
                drawChartResizeAlertSensor();
                drawChartResizeAlertEvent();
                drawChartResizeMeasurementAlertUser();
            });
        });
    </script>
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
    var reloadMeasurementURL = '${g.createLink(controller: "controlPanel", action: 'reloadMeasurement')}';
    var reloadAlertURL = '${g.createLink(controller: "controlPanel", action: 'reloadAlert')}';
    var reloadAdminURL = '${g.createLink(controller: "controlPanel", action: 'reloadAdmin')}';
    var reloadUserBCURL = '${g.createLink(controller: "controlPanel", action: 'reloadUserBC')}';
</script>

<!-- Page-sidebar-wrapper -->
<div class="page-sidebar-wrapper">
    <!-- Page-sidebar -->
    <div class="page-sidebar navbar-collapse collapse">
        <!-- Page-sidebar-menu -->
        <ul class="page-sidebar-menu page-header-fixed" data-keep-expanded="true" data-auto-scroll="true" data-slide-speed="200" style="padding-top: 30px">

            <!-- Load search action -->
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
                <div class="col-md-12">
                    <!-- Widget thumb -->
                    <div class="widget-thumb widget-bg-color-white text-uppercase margin-bottom-20 bordered widget-measurement">
                        <h4 class="widget-thumb-heading"><g:message code="layouts.main_auth_admin.body.widget.measurements" default="Measurements"/></h4>
                        <i class="fa fa-refresh iconReload reloadMeasurement"></i>
                        <div class="widget-thumb-wrap">
                            <i class="widget-thumb-icon bg-blue-soft fa fa-archive"></i>
                            <div class="widget-thumb-body">
                                <span class="widget-thumb-subtitle"><g:message code="layouts.main_auth_admin.body.widget.total" default="Total"/></span>
                                <span class="widget-thumb-body-stat counterMeasurement" data-counter="counterup" data-value="${totalMeasurements}">${totalMeasurements}</span>
                            </div>
                        </div>
                    </div> <!-- /.Widget thumb -->
                </div>
            </div> <!-- /.Widget -->

            <div class="row panel-row-dashboard">
               <div class="col-md-6">
                    <!-- Widget thumb -->
                    <div class="widget-thumb widget-bg-color-white text-uppercase margin-bottom-20 bordered widget-alert">
                        <h4 class="widget-thumb-heading"><g:message code="layouts.main_auth_admin.body.widget.bc.alerts" default="Hyperledger Fabric - Alerts"/></h4>
                        <i class="fa fa-refresh iconReload reloadAlert"></i>
                        <div class="widget-thumb-wrap">
                            <i class="widget-thumb-icon bg-red-sunglo icofont icofont-alarm"></i>
                            <div class="widget-thumb-body">
                                <span class="widget-thumb-subtitle"><g:message code="layouts.main_auth_admin.body.widget.total" default="Total"/></span>
                                <span class="widget-thumb-body-stat counterAlert" data-counter="counterup" data-value="${totalAlerts}">${totalAlerts}</span>
                            </div>
                        </div>
                    </div> <!-- /.Widget thumb -->
               </div>

                <div class="col-md-6">
                    <!-- Widget thumb -->
                    <div class="widget-thumb widget-bg-color-white text-uppercase margin-bottom-20 bordered widget-userBC">
                        <h4 class="widget-thumb-heading"><g:message code="layouts.main_auth_admin.body.widget.bc.users" default="Hyperledger Fabric - Users"/></h4>
                        <i class="fa fa-refresh iconReload reloadUserBC"></i>
                        <div class="widget-thumb-wrap">
                            <i class="widget-thumb-icon bg-green-dark icofont icon-user"></i>
                            <div class="widget-thumb-body">
                                <span class="widget-thumb-subtitle"><g:message code="layouts.main_auth_admin.body.widget.total" default="Total"/></span>
                                <span class="widget-thumb-body-stat counterUserBC" data-counter="counterup" data-value="${totalUsers}">${totalUsers}</span>
                            </div>
                        </div>
                    </div> <!-- /.Widget thumb -->
                </div>
            </div> <!-- /.Widget -->

            <!-- Graphs -->
            <div class="row panel-row-dashboard">

                <!-- Alerts triggered by each sensor -->
                <div class="col-md-6">
                    <!-- Portlet -->
                    <div class="portlet light bg-inverse portlet-graphAlertSensor">
                        <div class="portlet-title">
                            <div class="caption font-green-dark">
                                <i class="fa fa-bar-chart font-green-dark"></i>
                                <span class="caption-subject sbold uppercase"><g:message code="layouts.main_auth_admin.body.portlet.alertSensor" default="Alerts by sensor"/></span>
                            </div>
                            <div class="tools">
                                <i class="fa fa-refresh reloadGraph reloadAlertSensor" onclick="drawChartAlertSensor()"></i>
                                <a href="" class="collapse"> </a>
                                <a href="" class="remove"> </a>
                            </div>
                        </div>
                        <div class="portlet-body">
                            <div class="scroller" style="height:350px" data-rail-visible="1" data-rail-color="#105d41" data-handle-color="#4A9F60">
                                <div id="chart_AlertSensor" style="width:100%; height:100%"></div>
                            </div>
                        </div>
                    </div> <!-- /.Portlet -->
                </div>

                <!-- Events triggered by each sensor -->
                <div class="col-md-6">
                    <!-- Portlet -->
                    <div class="portlet light bg-inverse portlet-graphAlertEvent">
                        <div class="portlet-title">
                            <div class="caption font-green-dark">
                                <i class="fa fa-bar-chart font-green-dark"></i>
                                <span class="caption-subject sbold uppercase"><g:message code="layouts.main_auth_admin.body.portlet.alertEvent" default="Alerts by event"/></span>
                            </div>
                            <div class="tools">
                                <i class="fa fa-refresh reloadGraph reloadAlertEvent" onclick="drawChartAlertEvent()"></i>
                                <a href="" class="collapse"> </a>
                                <a href="" class="remove"> </a>
                            </div>
                        </div>
                        <div class="portlet-body">
                            <div class="scroller" style="height:350px" data-rail-visible="1" data-rail-color="#105d41" data-handle-color="#4A9F60">
                                <div id="chart_AlertEvent" style="width:100%; height:100%"></div>
                            </div>
                        </div>
                    </div> <!-- /.Portlet -->
                </div>
            </div> <!-- /.Graphs -->

            <!-- Graphs -->
            <div class="row panel-row-dashboard">

                <!-- Measurements and alerts of each user -->
                <div class="col-md-12">
                    <!-- Portlet -->
                    <div class="portlet light bg-inverse portlet-graphMeasurementAlertUser">
                        <div class="portlet-title">
                            <div class="caption font-green-dark">
                                <i class="fa fa-bar-chart font-green-dark"></i>
                                <span class="caption-subject sbold uppercase"><g:message code="layouts.main_auth_admin.body.portlet.measurementAlertUser" default="Correlation between measurements and alerts of the users"/></span>
                            </div>
                            <div class="tools">
                                <i class="fa fa-refresh reloadGraph reloadMeasurementAlertUser" onclick="drawChartMeasurementAlertUser()"></i>
                                <a href="" class="collapse"> </a>
                                <a href="" class="remove"> </a>
                            </div>
                        </div>
                        <div class="portlet-body">
                            <div class="scroller" style="height:350px" data-rail-visible="1" data-rail-color="#105d41" data-handle-color="#4A9F60">
                                <div id="chart_MeasurementAlertUser" style="width:100%; height:100%"></div>
                            </div>
                        </div>
                    </div> <!-- /.Portlet -->
                </div>
            </div> <!-- /.Graphs -->

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