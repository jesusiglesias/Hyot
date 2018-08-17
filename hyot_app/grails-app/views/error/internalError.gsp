<!-------------------------------------------------------------------------------------------*
 *                               INTERNAL SERVER ERROR PAGE                                  *
 *------------------------------------------------------------------------------------------->

<html>
    <!-- HEAD -->
    <head>
        <meta name="layout" content="main_error"/>
        <title><g:message code="views.errors.internalError" default="500 | Internal server error"/></title>

        <!-- Development environment -->
        <g:if env="development"><asset:stylesheet src="errors.css"/></g:if>
    </head> <!-- /.HEAD -->

    <!-- BODY -->
    <body>

        <!-- Development environment -->
        <g:if env="development">
            <div class="exception-dev-container">
                <g:renderException exception="${exception}"/>
            </div>
        </g:if>
        <g:else>
            <!-- Error description of the container -->
            <div id="error-container">
                <div class="row">
                    <div class="col-sm-8 col-sm-offset-2 text-center">
                        <h1 class="animation-pulse"><i class="fa fa-cog fa-spin text-danger"></i> 500 </h1>
                        <h3 class="h3 description-error">
                            ${raw(g.message(code: "views.errors.description.internalError",
                                    default: 'Oops! <strong>An internal server error has occurred.</strong>'))}</h3>
                    </div>
                </div>
            </div>
        </g:else>
    </body>
</html>



