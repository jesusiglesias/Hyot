<%@ page import="User.User" %>

<div class="form-body">
    <!-- Row -->
    <div class="row space-firstRow-profile-user">
        <!-- Old password -->
        <div class="col-lg-6 col-lg-offset-3">
            <div class="form-group">
                <label for="currentPassword" class="control-label">
                    <h5 class="xthin">
                        <g:message code="layouts.main_userpage.content.myProfile.sidebar.oldPassword.title" default="Current password"/>
                        <span class="required"> * </span>
                    </h5>
                </label>
                <div class="input-icon right">
                    <i class="fa"></i>
                    <g:passwordField name="currentPassword" class="form-control form-shadow emptySpaces profile-current-password profilePassword-input" maxlength="32" autocomplete="off"/>
                </div>
                <i class="fa fa-eye i-show-profile-currentPassword"></i> <!-- Show password icon -->
            </div>
        </div>
    </div>

    <!-- Row -->
    <div class="row">
        <!-- Password -->
        <div class="col-lg-6 col-lg-offset-3">
            <div class="form-group">
                <label for="password" class="control-label">
                    <h5 class="xthin">
                        <g:message code="layouts.main_userpage.content.myProfile.sidebar.newPassword.title" default="New password"/>
                        <span class="required"> * </span>
                    </h5>
                </label>
                <div class="input-icon right">
                    <i class="fa"></i>
                    <g:passwordField name="password" class="form-control form-shadow emptySpaces password-space-progress profile-new-password profilePassword-input" maxlength="32" autocomplete="off"/>
                </div>
                <i class="fa fa-eye i-show-profile-newPassword"></i> <!-- Show password icon -->
            </div>
        </div>
    </div>

    <!-- Row -->
    <div class="row">
        <!-- Confirm password -->
        <div class="col-lg-6 col-lg-offset-3">
            <div class="form-group">
                <label for="confirmPassword" class="control-label">
                    <h5 class="xthin">
                        <g:message code="layouts.main_userpage.content.myProfile.sidebar.confirmPassword.title" default="Confirm password"/>
                        <span class="required"> * </span>
                    </h5>
                </label>
                <div class="input-icon right">
                    <i class="fa"></i>
                    <g:passwordField name="confirmPassword" class="form-control form-shadow emptySpaces profile-confirm-password profilePassword-input" maxlength="32" autocomplete="off"/>
                </div>
                <i class="fa fa-eye i-show-profile-confirmPassword"></i> <!-- Show password icon -->
            </div>
        </div>
    </div>
</div>
