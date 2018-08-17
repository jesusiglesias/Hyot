<!-------------------------------------------------------------------------------------------*
 *                                UNAVAILABLE SERVICE PAGE                                    *
 *------------------------------------------------------------------------------------------->

<html>
    <!-- HEAD -->
    <head>
        <meta name="layout" content="main_error"/>
        <title><g:message code="views.errors.unavailableService" default="503 | Unavailable service"/></title>
    </head> <!-- /.HEAD -->

    <!-- BODY -->
    <body>
    <!-- Error description of the container -->
    <div id="error-container">
        <div class="row">
            <div class="col-sm-8 col-sm-offset-2 text-center">
                <h1 class="animation-tossing"><i class="fa fa-bullhorn text-success"></i> 503 </h1>
                <h3 class="h3 description-error">
                    ${raw(g.message(code: "views.errors.description.unavailableService",
                            default: 'Oops! <strong>Service is currently not available.</strong> <br/> Please try again later.'))}</h3>
            </div>
        </div>
    </div>
    </body>
</html>
