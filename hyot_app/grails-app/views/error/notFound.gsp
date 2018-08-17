<!-------------------------------------------------------------------------------------------*
 *                                     NOT FOUND PAGE                                        *
 *------------------------------------------------------------------------------------------->

<html>
	<!-- HEAD -->
	<head>
		<meta name="layout" content="main_error"/>
		<title><g:message code="views.errors.notFound" default="404 | Page not found"/></title>
	</head> <!-- /.HEAD -->

	<!-- BODY -->
	<body>
		<!-- Error description of the container -->
		<div id="error-container">
			<div class="row">
				<div class="col-sm-8 col-sm-offset-2 text-center">
					<h1 class="animation-pulse"><i class="fa fa-exclamation-circle text-danger"></i> 404 </h1>
					<h3 class="h3 description-error">
						${raw(g.message(code: "views.errors.description.notFound",
								default: 'Oops! An error has occurred.<br/><strong>Page not found!</strong>'))}</h3>
				</div>
			</div>
		</div>
	</body>
</html>