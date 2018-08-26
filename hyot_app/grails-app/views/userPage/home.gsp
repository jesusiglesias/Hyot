<!DOCTYPE html>
<html>
<head>
    <meta name="layout" content="main_userpage">
    <title><g:message code="layouts.main_userpage.head.title.home" default="HYOT | Home page"/></title>
    <link rel="stylesheet" href="${resource(dir: 'css/select', file: 'bootstrap-select.min.css')}" type="text/css"/>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/toastr/2.1.2/toastr.min.css">
    <script src="https://cdn.jsdelivr.net/toastr/2.1.2/toastr.min.js"></script>

    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>

    <script>
        var _sensorDHT = '${g.message(code: "layouts.main_auth_admin.body.portlet.alertSensor.dht11", default: "DHT11")}';
        var _sensorHCSR = '${g.message(code: "layouts.main_auth_admin.body.portlet.alertSensor.hcsr04", default: "HCSR-04")}';
        var _sensorTEM = '${g.message(code: "layouts.main_auth_admin.body.portlet.alertEvent.temperature", default: "Temperature")}';
        var _sensorHUM = '${g.message(code: "layouts.main_auth_admin.body.portlet.alertEvent.humidity", default: "Humidity")}';
        var _sensorDIS = '${g.message(code: "layouts.main_auth_admin.body.portlet.alertEvent.distance", default: "Distance")}';
        var _alertsTitle = '${g.message(code: "layouts.main_auth_admin.body.portlet.myalerts.title", default: "My alerts")}';
        var _alertsSubtitle = '${g.message(code: "layouts.main_auth_admin.body.portlet.myalerts.subtitle", default: "Total of my alerts")}';

        // Load the Visualization API and the piechart package.
        google.charts.load("current", {packages:['corechart']});

        // Set a callback to run when the Google Visualization API is loaded.
        google.setOnLoadCallback(drawVisualization);

        var dataJSON_MyAlertSensor, dataJSON_MyAlertEvent;

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
            drawChartMyAlertSensor();
            drawChartMyAlertEvent();
        }

        // It draws the column chart when the window resizes
        function drawChartResizeMyAlertSensor() {

            // Create the data table out of JSON data loaded from server
            var dataMASResize = google.visualization.arrayToDataTable([
                [_alertsTitle, _alertsSubtitle, { role: "style" } ],
                [_sensorDHT, dataJSON_MyAlertSensor.dht, "#d6c152"],
                [_sensorHCSR, dataJSON_MyAlertSensor.hcsr, "#4eb48a"]
            ]);

            var chartHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0) + 'px';
            var chartWidth = Math.max(document.documentElement.clientWidth, window.innerWidth || 0) + 'px';

            var viewMASResize = new google.visualization.DataView(dataMASResize);

            viewMASResize.setColumns([0, 1,
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
            var chartMASResize =  new google.visualization.ColumnChart(document.getElementById('chart_MyAlertSensor'));
            chartMASResize.draw(viewMASResize, options);
        }

        // It draws the column chart when the window resizes
        function drawChartResizeMyAlertEvent() {

            // Create the data table out of JSON data loaded from server
            var dataMAEResize = google.visualization.arrayToDataTable([
                [_alertsTitle, _alertsSubtitle, { role: "style" } ],
                [_sensorTEM, dataJSON_MyAlertEvent.temperature, "#5862d6"],
                [_sensorHUM, dataJSON_MyAlertEvent.humidity, "#b45665"],
                [_sensorDIS, dataJSON_MyAlertEvent.distance, "#b4a271"]
            ]);

            var chartHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0) + 'px';
            var chartWidth = Math.max(document.documentElement.clientWidth, window.innerWidth || 0) + 'px';

            var viewMAEResize = new google.visualization.DataView(dataMAEResize);

            viewMAEResize.setColumns([0, 1,
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
            var chartMAEResize =  new google.visualization.ColumnChart(document.getElementById('chart_MyAlertEvent'));
            chartMAEResize.draw(viewMAEResize, options);
        }

        // It draws the column chart (alerts of an user by sensor)
        function drawChartMyAlertSensor() {

            var contentChartMyAlertSensor = $('.portlet-graphMyAlertSensor');

            $.ajax({
                url: "${createLink(controller:'userPage', action:'myalertBySensor')}",
                dataType: "json",
                beforeSend: function () {
                    contentChartMyAlertSensor.LoadingOverlay("show", {
                        image: "",
                        fontawesome: "fa fa-spinner fa-spin"
                    });
                },
                success: function (jsonDataMAS) {
                    // It is used to resize
                    dataJSON_MyAlertSensor = jsonDataMAS;

                    // Create the data table out of JSON data loaded from server
                    var dataMyAlertSensor = google.visualization.arrayToDataTable([
                        [_alertsTitle, _alertsSubtitle, { role: "style" } ],
                        [_sensorDHT, jsonDataMAS.dht, "#d6c152"],
                        [_sensorHCSR, jsonDataMAS.hcsr, "#4eb48a"]
                    ]);

                    var chartHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0) + 'px';
                    var chartWidth = Math.max(document.documentElement.clientWidth, window.innerWidth || 0) + 'px';

                    var viewMAS = new google.visualization.DataView(dataMyAlertSensor);

                    viewMAS.setColumns([0, 1,
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
                    var chartMAS =  new google.visualization.ColumnChart(document.getElementById('chart_MyAlertSensor'));
                    chartMAS.draw(viewMAS, options);
                },
                error: function () {
                    var listMessageMAS = $('.list-messageMAS');

                    // Avoid duplicates
                    if (listMessageMAS.length) {
                        listMessageMAS.remove();
                    }

                    // Message
                    $('#chart_MyAlertSensor').prepend("<ul class='list-group list-messageAS'><li class='list-group-item bg-red-intense bg-font-red-intense' style='margin-right: -12px'>" + reloadAjaxError + "</li></ul>");
                    createAutoClosingAlert('.list-messageMAS');
                },
                complete: function () {
                    setTimeout(function () {
                        contentChartMyAlertSensor.LoadingOverlay("hide");
                    }, 500);
                }
            });
        }

        // It draws the column chart (alerts of an user by event)
        function drawChartMyAlertEvent() {

            var contentChartMyAlertEvent = $('.portlet-graphMyAlertEvent');

            $.ajax({
                url: "${createLink(controller:'userPage', action:'myalertByEvent')}",
                dataType: "json",
                beforeSend: function () {
                    contentChartMyAlertEvent.LoadingOverlay("show", {
                        image: "",
                        fontawesome: "fa fa-spinner fa-spin"
                    });
                },
                success: function (jsonDataMAE) {
                    // It is used to resize
                    dataJSON_MyAlertEvent = jsonDataMAE;

                    // Create the data table out of JSON data loaded from server
                    var dataMyAlertEvent = google.visualization.arrayToDataTable([
                        [_alertsTitle, _alertsSubtitle, { role: "style" } ],
                        [_sensorTEM, jsonDataMAE.temperature, "#5862d6"],
                        [_sensorHUM, jsonDataMAE.humidity, "#b45665"],
                        [_sensorDIS, jsonDataMAE.distance, "#b4a271"]
                    ]);

                    var chartHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0) + 'px';
                    var chartWidth = Math.max(document.documentElement.clientWidth, window.innerWidth || 0) + 'px';

                    var viewMAE = new google.visualization.DataView(dataMyAlertEvent);

                    viewMAE.setColumns([0, 1,
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
                    var chartMAE =  new google.visualization.ColumnChart(document.getElementById('chart_MyAlertEvent'));
                    chartMAE.draw(viewMAE, options);
                },
                error: function () {
                    var listMessageMAE = $('.list-messageMAE');

                    // Avoid duplicates
                    if (listMessageMAE.length) {
                        listMessageMAE.remove();
                    }

                    // Message
                    $('#chart_MyAlertEvent').prepend("<ul class='list-group list-messageAE'><li class='list-group-item bg-red-intense bg-font-red-intense' style='margin-right: -12px'>" + reloadAjaxError + "</li></ul>");
                    createAutoClosingAlert('.list-messageMAE');
                },
                complete: function () {
                    setTimeout(function () {
                        contentChartMyAlertEvent.LoadingOverlay("hide");
                    }, 500);
                }
            });
        }

        jQuery(document).ready(function() {
            // Resizing the column charts (alerts by sensor and alerts by event)
            $(window).resize(function(){
                drawChartResizeMyAlertSensor();
                drawChartResizeMyAlertEvent();
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
        var reloadMymeasurementURL = '${g.createLink(controller: "userPage", action: 'reloadMymeasurement')}';
        var reloadMyalertURL = '${g.createLink(controller: "userPage", action: 'reloadMyalert')}';
    </script>

    <!-- Horizontal menu -->
    <content tag="horizontalMenu">
        <div class="hor-menu hidden-sm hidden-xs">
            <ul class="nav navbar-nav">
                <li> <!-- TODO -->
                    <g:link uri="/mymeasurements"><g:message code="layout.main_userpage.horizontal.menu.measurement" default="My measurements"/></g:link>
                </li>
                <li>
                    <g:link uri="/myalerts"><g:message code="layout.main_userpage.horizontal.menu.alert" default="My alerts"/></g:link>
                </li>
            </ul>
        </div>
    </content>

    <!-- Responsive horizontal menu TODO -->
    <content tag="responsiveHorizontalMenu">
        <li class="nav-item">
            <g:link uri="/mymeasurements" class="nav-link">
                <i class="icofont icofont-info"></i>
                <span class="title"><g:message code="layout.main_userpage.horizontal.menu.measurement" default="My measurements"/></span>
                <span class="arrow"></span>
            </g:link>
        </li>
        <li class="nav-item">
            <g:link uri="/myalerts" class="nav-link">
                <i class="icofont icofont-speech-comments"></i>
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
                    <g:message code="layouts.main_auth_user.body.title.statistic" default="Statistics"/>
                </h3>
            </div>
        </div>
    </div>

    <!-- Graphs -->
    <div class="row row-userLayoutTitle graphs-home">

        <div class="col-md-5 col-xs-offset-1 col-xs-10">
            <!-- Widget thumb -->
            <div class="widget-thumb widget-bg-color-white text-uppercase margin-bottom-20 bordered widget-mymeasurement">
                <h4 class="widget-thumb-heading"><g:message code="layouts.main_auth_admin.body.widget.measurements" default="Measurements"/></h4>
                <i class="fa fa-refresh iconReload reloadMymeasurement"></i>
                <div class="widget-thumb-wrap">
                    <i class="widget-thumb-icon bg-green-dark icofont icon-user"></i>
                    <div class="widget-thumb-body">
                        <span class="widget-thumb-subtitle"><g:message code="layouts.main_auth_admin.body.widget.total" default="Total"/></span>
                        <span class="widget-thumb-body-stat counterMymeasurement" data-counter="counterup" data-value="${totalMeasurements}">${totalMeasurements}</span>
                    </div>
                </div>
            </div> <!-- /.Widget thumb -->
        </div>

        <div class="col-md-5 col-md-offset-0 col-xs-offset-1 col-xs-10">
            <!-- Widget thumb -->
            <div class="widget-thumb widget-bg-color-white text-uppercase margin-bottom-20 bordered widget-myalert">
                <h4 class="widget-thumb-heading"><g:message code="layouts.main_auth_admin.body.widget.bc.alerts" default="Hyperledger Fabric - Alerts"/></h4>
                <i class="fa fa-refresh iconReload reloadMyalert"></i>
                <div class="widget-thumb-wrap">
                    <i class="widget-thumb-icon bg-red-sunglo icofont icofont-alarm"></i>
                    <div class="widget-thumb-body">
                        <span class="widget-thumb-subtitle"><g:message code="layouts.main_auth_admin.body.widget.total" default="Total"/></span>
                        <span class="widget-thumb-body-stat counterMyalert" data-counter="counterup" data-value="${totalAlerts}">${totalAlerts}</span>
                    </div>
                </div>
            </div> <!-- /.Widget thumb -->
        </div>

    </div>

    <!-- Graphs -->
    <div class="row row-userLayoutTitle graphs-home">

        <!-- Alerts of a user triggered by each sensor -->
        <div class="col-md-5 col-xs-offset-1 col-xs-10">
            <!-- Portlet -->
            <div class="portlet light portlet-graphMyAlertSensor">
                <div class="portlet-title">
                    <div class="caption font-green-dark">
                        <i class="fa fa-bar-chart font-green-dark"></i>
                        <span class="caption-subject sbold uppercase"><g:message code="layouts.main_auth_admin.body.portlet.myalertSensor" default="My alerts by sensor"/></span>
                    </div>
                    <div class="tools">
                        <i class="fa fa-refresh reloadGraph reloadMyAlertSensor" onclick="drawChartMyAlertSensor()"></i>
                        <a href="" class="collapse"> </a>
                        <a href="" class="remove"> </a>
                    </div>
                </div>
                <div class="portlet-body">
                    <div class="scroller" style="height:350px" data-rail-visible="1" data-rail-color="#105d41" data-handle-color="#4A9F60">
                        <div id="chart_MyAlertSensor" style="width:100%; height:100%"></div>
                    </div>
                </div>
            </div> <!-- /.Portlet -->
        </div>

        <!-- Events of an user triggered by each sensor -->
        <div class="col-md-5 col-md-offset-0 col-xs-offset-1 col-xs-10">
            <!-- Portlet -->
            <div class="portlet light portlet-graphMyAlertEvent">
                <div class="portlet-title">
                    <div class="caption font-green-dark">
                        <i class="fa fa-bar-chart font-green-dark"></i>
                        <span class="caption-subject sbold uppercase"><g:message code="layouts.main_auth_admin.body.portlet.myalertEvent" default="My alerts by event"/></span>
                    </div>
                    <div class="tools">
                        <i class="fa fa-refresh reloadGraph reloadMyAlertEvent" onclick="drawChartMyAlertEvent()"></i>
                        <a href="" class="collapse"> </a>
                        <a href="" class="remove"> </a>
                    </div>
                </div>
                <div class="portlet-body">
                    <div class="scroller" style="height:350px" data-rail-visible="1" data-rail-color="#105d41" data-handle-color="#4A9F60">
                        <div id="chart_MyAlertEvent" style="width:100%; height:100%"></div>
                    </div>
                </div>
            </div> <!-- /.Portlet -->
        </div>
    </div> <!-- /.Graphs -->

    <asset:javascript src="custom/userpage.js"/>
    <script src="//cdnjs.cloudflare.com/ajax/libs/waypoints/2.0.3/waypoints.min.js"></script>
    <asset:javascript src="counter/jquery.counterup.min.js"/>
    <asset:javascript src="overlay/loadingoverlay.min.js"/>

</body>
</html>