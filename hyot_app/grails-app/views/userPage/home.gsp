<!DOCTYPE html>
<html>
<head>
    <meta name="layout" content="main_userpage">
    <title><g:message code="layouts.main_userpage.head.title.home" default="HYOT | Home page"/></title>
    <link rel="stylesheet" href="${resource(dir: 'css/select', file: 'bootstrap-select.min.css')}" type="text/css"/>
</head>
<body>

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

<!-- Page-title TODO -->
<div class="row row-userLayoutTitle">
    <div class="col-md-12 col-userLayoutTitle">
        <!-- Page-title -->
        <div class="page-title-user-home">
            <h3 class="page-title-user-home-title">
                ${raw(g.message(code:"layouts.main_userpage.body.title.home", default:"Welcome to <span>HYOT</span>!"))}
            </h3>
            <p class="page-title-user-home-description">
                ${raw(g.message(code:"layouts.main_userpage.body.title.home.description", default:"The proof of concept for the traceability of an IoT environment by Hyperledger."))}
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

<!-- Search input -->
<div class="row row-userLayoutTitle searchForm-home">
    <div class="col-md-12 text-center">

    </div>
</div>

<div class="row row-userLayoutTitle">
    <div class="col-md-12 text-center">

    </div>
</div>

</body>
</html>