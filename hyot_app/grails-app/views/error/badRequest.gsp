<!-------------------------------------------------------------------------------------------*
 *                                   BAD REQUEST PAGE                                        *
 *------------------------------------------------------------------------------------------->

<html>
	<!-- HEAD -->
	<head>
		<meta name="layout" content="main_error"/>
		<title><g:message code="views.errors.badRequest" default="400 | Bad request"/></title>
	</head> <!-- /.HEAD -->

	<!-- BODY -->
	<body>
		<!-- Error description of the container -->
		<div id="error-container">
			<div class="row">
				<div class="col-sm-8 col-sm-offset-2 text-center">
					<h1 class="animation-bigEntrance"><i class="fa fa-exclamation-triangle text-warning"></i> 400 </h1>
					<h3 class="h3 description-error">
						${raw(g.message(code: "views.errors.description.badRequest",
								default: 'Oops! <strong>Your request contains bad syntax and cannot be fulfilled.</strong>'))}</h3>
				</div>
			</div>
		</div>
	</body>
</html>
