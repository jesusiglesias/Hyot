<!-------------------------------------------------------------------------------------------*
 *                                   NOT ALLOWED PAGE                                        *
 *------------------------------------------------------------------------------------------->

<html>
	<!-- HEAD -->
	<head>
		<meta name="layout" content="main_error"/>
		<title><g:message code="views.errors.notAllowed" default="405 | Method not allowed"/></title>
	</head> <!-- /.HEAD -->

	<!-- BODY -->
	<body>
		<!-- Error description of the container -->
		<div id="error-container">
			<div class="row">
				<div class="col-sm-8 col-sm-offset-2 text-center">
					<h1 class="animation-fadeInLeft"><i class="fa fa-exclamation-triangle text-warning"></i> 405 </h1>
					<h3 class="h3 description-error">
						${raw(g.message(code: "views.errors.description.notAllowed",
								default: 'Oops! <strong>The request method is not allowed.</strong>'))}</h3>
				</div>
			</div>
		</div>
	</body>
</html>
