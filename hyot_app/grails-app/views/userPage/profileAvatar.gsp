<%@ page import="org.springframework.validation.FieldError" contentType="text/html;charset=UTF-8" %>
<!DOCTYPE html>
<html>
<head>
    <meta name="layout" content="main_userpage">
    <title><g:message code="layouts.main_userpage.head.title.myProfile" default="HYOT | My profile"/></title>
    <link rel="stylesheet" href="${resource(dir: 'css/normalUser', file: 'profile.css')}" type="text/css"/>
    <link rel="stylesheet" href="${resource(dir: 'css/fileInput', file: 'bootstrap-fileinput.css')}" type="text/css"/>

    <script>

        // Variables to use in script
        var _requiredField = '${g.message(code:'default.validation.required', default:'This field is required.')}';

        // Handler auto close alert
        function createAutoClosingAlert(selector) {
            var alert = $(selector);
            window.setTimeout(function () {
                alert.slideUp(1000, function () {
                    $(this).remove();
                });
            }, 5000);
        }
    </script>
</head>

<body>

    <!-- Horizontal menu -->
    <content tag="horizontalMenu">
        <div class="hor-menu hidden-sm hidden-xs">
            <ul class="nav navbar-nav">
                <li>
                    <g:link uri="/mymeasurements"><g:message code="layout.main_userpage.horizontal.menu.measurement" default="My measurements"/></g:link>
                </li>
                <li>
                    <g:link uri="/myalerts"><g:message code="layout.main_userpage.horizontal.menu.alert" default="My alerts"/></g:link>
                </li>
            </ul>
        </div>
    </content>

    <!-- Responsive horizontal menu -->
    <content tag="responsiveHorizontalMenu">
        <li class="nav-item">
            <g:link uri="/mymeasurements" class="nav-link">
                <i class="fa fa-archive"></i>
                <span class="title"><g:message code="layout.main_userpage.horizontal.menu.measurement" default="My measurements"/></span>
                <span class="arrow"></span>
            </g:link>
        </li>
        <li class="nav-item">
            <g:link uri="/myalerts" class="nav-link">
                <i class="fa fa-bell"></i>
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
            <li>
                <span><g:message code="layouts.main_userpage.body.title.myProfile" default="My profile"/></span>
            </li>
        </ul>
    </div> <!-- /.Page-bar -->

    <!-- Page-title -->
    <div class="row row-userLayoutTitle">
        <div class="col-md-12 col-userLayoutTitle">
            <!-- Page-title -->
            <div class="page-title-user-profile">
                <h3 class="page-title-user-profile-title">
                    <g:message code="layouts.main_userpage.body.title.myProfile" default="My profile"/>
                </h3>

                <p class="page-title-user-profile-description">
                    ${raw(g.message(code: "layouts.main_userpage.body.title.myProfile.description", default: "Data associated with your user account are displayed here. <strong>Remember:</strong> " +
                            "Username can not be modified directly."))}
                </p>
            </div>
        </div>
    </div>

<div class="row row-userLayoutTitle">
    <div class="col-md-12 col-userLayoutTitle">
        <!-- Profile -->
        <div class="profile-sidebar">
            <!-- Sidebar - left -->
            <div class="portlet light customColor-profile profile-sidebar-portlet">
                <!-- Image profile -->
                <div class="profile-userpic">
                    <g:if test="${infoCurrentUser?.avatar}">
                        <img class="profileImage-view" alt="Profile image"
                             src="${createLink(controller: 'controlPanel', action: 'profileImage', id: infoCurrentUser.ident())}"/>
                    </g:if>
                    <g:else>
                        <img class="profileImage-view" alt="Profile image"
                             src="${resource(dir: 'img/profile', file: 'user_profile.png')}"/>
                    </g:else>
                </div>
                <!-- User information -->
                <div class="profile-usertitle">
                    <div class="profile-usertitle-name">${infoCurrentUser?.name} ${infoCurrentUser?.surname}</div>
                </div>

                <!-- Menu -->
                <div class="profile-usermenu">
                    <ul class="nav">
                        <li>
                            <g:link uri="/profile">
                                <i class="fa fa-user"></i>
                                <g:message code="layouts.main_userpage.content.myProfile.sidebar.personal" default="Personal information"/>
                            </g:link>
                        </li>
                        <li>
                            <g:link uri="/profilePassword">
                                <i class="fa fa-key"></i>
                                <g:message code="layouts.main_userpage.content.myProfile.sidebar.password" default="Change password"/>
                            </g:link>
                        </li>
                        <li class="active">
                            <g:link uri="/profileAvatar">
                                <i class="icofont icofont-image"></i>
                                <g:message code="layouts.main_userpage.content.myProfile.sidebar.avatar" default="Change profile image"/>
                            </g:link>
                        </li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- Personal information -->
        <div class="profile-content">
            <div class="row row-userLayoutTitle">
                <div class="col-md-12 col-userLayoutTitle">

                <!-- Alerts -->
                    <g:if test="${flash.userProfileAvatarMessage}">
                        <div class='alert alert-success-custom-backend alert-dismissable alert-entity-info-profile fade in'>
                            <button type='button' class='close' data-dismiss='alert' aria-hidden='true'></button>
                            <span class="xthin" role="status">${raw(flash.userProfileAvatarMessage)}</span>
                        </div>

                        <g:javascript>
                            createAutoClosingAlert('.alert-entity-info-profile');
                        </g:javascript>
                    </g:if>

                    <g:if test="${flash.userProfileAvatarErrorMessage}">
                        <div class='alert alert-danger-custom-backend alert-dismissable alert-entity-error-profile fade in'>
                            <button type='button' class='close' data-dismiss='alert' aria-hidden='true'></button>
                            <span class="xthin" role="status"> ${raw(flash.userProfileAvatarErrorMessage)} </span>
                        </div>

                        <g:javascript>
                            createAutoClosingAlert('.alert-entity-error-profile');
                        </g:javascript>
                    </g:if>

                    <!-- Error in validation -->
                    <g:hasErrors bean="${currentUser}">
                        <div class='alert alert-danger-custom-backend alert-dismissable alert-entity-error-profile fade in'>
                            <button type='button' class='close' data-dismiss='alert' aria-hidden='true'></button>
                            <g:eachError bean="${currentUser}" var="error">
                                <p role="status" class="xthin" <g:if test="${error in FieldError}">data-field-id="${error.field}"</g:if>><g:message error="${error}"/></p>
                            </g:eachError>
                        </div>

                        <g:javascript>
                            createAutoClosingAlert('.alert-entity-error-profile');
                        </g:javascript>
                    </g:hasErrors>

                    <div class="portlet light">
                        <div class="portlet-title">
                            <div class="caption caption-md">
                                <span class="caption-subject sbold uppercase font-green-dark avatar-subject">
                                    <g:message code="layouts.main_userpage.content.myProfile.sidebar.avatar.title" default="Profile image"/>
                                </span>
                            </div>
                        </div>
                        <div class="portlet-body">
                            <!-- Edit form -->
                            <g:form controller="userPage" action="updateAvatar" enctype="multipart/form-data" class="horizontal-form profileAvatarUser-form">
                                <g:hiddenField name="version" value="${currentUser?.version}" />
                                <fieldset class="form">
                                    <!-- Personal information -->
                                    <g:render template="avatarData"/>
                                </fieldset>

                                <div class="domain-button-group-less-avatar">
                                    <!-- Cancel button -->
                                    <g:link type="button" uri="/profile" class="btn grey-mint"><g:message code="default.button.cancel.label" default="Cancel"/></g:link>
                                    <button type="submit" class="btn green-dark icon-button-container" name="update">
                                        <i class="fa fa-check icon-button"></i>
                                        <g:message code="default.button.update.label" default="Update"/>
                                    </button>
                                </div>
                            </g:form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

    <!-- LOAD JAVASCRIPT -->
    <script src="//cdnjs.cloudflare.com/ajax/libs/waypoints/2.0.3/waypoints.min.js"></script>
    <asset:javascript src="counter/jquery.counterup.min.js"/>
    <asset:javascript src="domain-validation/avatar-profile-validation.js"/>
    <asset:javascript src="fileInput/bootstrap-fileinput.js"/>
    <script src="https://cdn.jsdelivr.net/jquery.validation/1.15.0/jquery.validate.min.js"></script>
    <script src="https://cdn.jsdelivr.net/jquery.validation/1.15.0/additional-methods.min.js"></script>

</body>
</html>