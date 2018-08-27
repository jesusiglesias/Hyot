<%@ page import="User.User;" %>

<div class="form-body">
    <!-- Row -->
    <div class="row space-firstRow-profile-user">
        <!-- Username -->
        <div class="col-md-6">
            <div class="form-group ${hasErrors(bean: currentUserInstance, field: 'username', 'error')}">
                <label for="username" class="control-label">
                    <h5 class="xthin">
                        <g:message code="user.username.label" default="Username"/>
                        <span class="required"> * </span>
                    </h5>
                </label>
                <div class="input-icon right">
                    <i class="fa"></i>
                    <g:textField name="username" maxlength="30" class="form-control form-shadow emptySpaces" value="${currentUser?.username}" disabled="true"/>
                </div>
                <div class="help-block">
                    <h5 class="text-justify">
                        <g:message code="layouts.main_userpage.content.myProfile.personalInformation.username.message" default="It is not possible to change the username directly."/>
                    </h5>
                </div>
            </div>
        </div>

        <!-- Email -->
        <div class="col-md-6 space-betweenCol-profile-user">
            <div class="form-group ${hasErrors(bean: currentUserInstance, field: 'email', 'error')}">
                <label for="email" class="control-label">
                    <h5 class="xthin">
                        <g:message code="user.email.label" default="Email"/>
                        <span class="required"> * </span>
                    </h5>
                </label>
                <div class="input-group input-icon right">
                    <i class="fa icon-offset"></i>
                    <g:field type="email" name="email" maxlength="60" class="form-control form-shadow emptySpaces email-userProfile user-profile-input" value="${currentUser?.email}"/>
                    <span class="input-group-btn">
                        <a href="javascript:;" class="btn green-dark" id="email-profile-checker">
                            <i class="fa fa-check"></i><g:message code="default.checker.button" default="Check"/>
                        </a>
                    </span>
                </div>
                <i class="fa fa-times i-delete-email-profile i-delete-userProfile-email"></i> <!-- Delete text icon -->
            </div>
            <div class="help-block emailProfile-block">
                <h5 class="text-justify">
                    <g:message code="layouts.main_auth_admin.body.content.admin.create.checker.block.info.email" default="Type an email and check its availability."/>
                </h5>
            </div>
        </div>
    </div>

    <!-- Row -->
    <div class="row space-secondRow-profile-user">

        <!-- Name -->
        <div class="col-md-6">
            <div class="form-group ${hasErrors(bean: currentUserInstance, field: 'name', 'error')}">
                <label for="name" class="control-label">
                    <h5 class="xthin">
                        <g:message code="user.name.label" default="Name"/>
                        <span class="required"> * </span>
                    </h5>
                </label>
                <div class="input-icon right">
                    <i class="fa"></i>
                    <g:textField name="name" maxlength="25" value="${currentUser?.name}" class="form-control form-shadow name-userProfile user-profile-input"/>
                </div>
                <i class="fa fa-times i-delete-userProfile i-delete-userProfile-name"></i> <!-- Delete text icon -->
            </div>
        </div>

        <!-- Surname -->
        <div class="col-md-6 space-betweenCol-profile-user">
            <div class="form-group ${hasErrors(bean: currentUserInstance, field: 'surname', 'error')}">
                <label for="surname" class="control-label">
                    <h5 class="xthin">
                        <g:message code="user.surname.label" default="Surname"/>
                        <span class="required"> * </span>
                    </h5>
                </label>
                <div class="input-icon right">
                    <i class="fa"></i>
                    <g:textField name="surname" maxlength="40" value="${currentUser?.surname}" class="form-control form-shadow surname-userProfile user-profile-input"/>
                </div>
                <i class="fa fa-times i-delete-userProfile i-delete-userProfile-surname"></i> <!-- Delete text icon -->
            </div>
        </div>
    </div>
</div>
