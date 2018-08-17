<!-------------------------------------------------------------------------------------------*
 *                                     FORBIDDEN PAGE                                        *
 *------------------------------------------------------------------------------------------->

<html>
<!-- HEAD -->
<head>
    <meta name="layout" content="main_error"/>
    <title><g:message code="views.errors.denied" default="403 | Forbidden"/></title>
</head> <!-- /.HEAD -->

<!-- BODY -->
<body>
<!-- Error description of the container -->
<div id="error-container">
    <div class="row">
        <div class="col-sm-8 col-sm-offset-2 text-center">
            <h1 class="animation-hatch"><i class="fa fa-times text-danger"></i> 403 </h1>
            <h3 class="h3 description-error">
                ${raw(g.message(code: "views.errors.description.forbidden",
                        default: 'Oops! An error has occurred.<br/><strong>You do not have permission to access.</strong>'))}</h3>
        </div>
    </div>
</div>
</body>
</html>