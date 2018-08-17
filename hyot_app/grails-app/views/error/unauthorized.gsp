<!-------------------------------------------------------------------------------------------*
 *                                    UNAUTHORIZED PAGE                                      *
 *------------------------------------------------------------------------------------------->

<html>
	<!-- HEAD -->
	<head>
		<meta name="layout" content="main_error"/>
		<title><g:message code="views.errors.unauthorized" default="401 | Unauthorized"/></title>
	</head> <!-- /.HEAD -->

	<!-- BODY -->
	<body>
		<!-- Error description of the container -->
		<div id="error-container">
			<div class="row">
				<div class="col-sm-8 col-sm-offset-2 text-center">
					<h1 class="animation-floatingHor"><i class="fa fa-times-circle-o text-danger"></i> 401 </h1>
					<h3 class="h3 description-error">
						${raw(g.message(code: "views.errors.description.unauthorized",
								default: 'Oops! <strong>You are not authorized to access this page.</strong>'))}</h3>
				</div>
			</div>
		</div>
	</body>
</html>