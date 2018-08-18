<%@ page import="Security.SecUser" %>

<div class="form-body">
    <!-- Row -->
    <div class="row">
        <!-- Username -->
        <div class="col-md-6">
            <div class="form-group ${hasErrors(bean: secUserInstance, field: 'username', 'error')}">
                <label for="username" class="control-label">
                    <h5 class="xthin">
                        <g:message code="admin.username.label" default="Username"/>
                        <span class="required"> * </span>
                    </h5>
                </label>
                <div class="input-group input-icon right">
                    <i class="fa icon-offset"></i>
                    <g:textField name="username" maxlength="30" class="form-control form-shadow emptySpaces username-admin backend-input" value="${secUserInstance?.username}"/>
                    <span class="input-group-btn">
                        <a href="javascript:;" class="btn green-dark" id="username-checker">
                            <i class="fa fa-check"></i><g:message code="default.checker.button" default="Check"/>
                        </a>
                    </span>
                </div>
                <i class="fa fa-times i-delete-backend i-delete-admin-username"></i> <!-- Delete text icon -->
            </div>
            <div class="help-block username-block">
                <h5 class="text-justify">
                    <g:message code="layouts.main_auth_admin.body.content.admin.create.checker.block.info.username" default="Type a username and check its availability."/>
                </h5>
            </div>
        </div>

        <!-- Email -->
        <div class="col-md-6 space-betweenCol">
            <div class="form-group ${hasErrors(bean: secUserInstance, field: 'email', 'error')}">
                <label for="email" class="control-label">
                    <h5 class="xthin">
                        <g:message code="admin.email.label" default="Email"/>
                        <span class="required"> * </span>
                    </h5>
                </label>
                <div class="input-group input-icon right">
                    <i class="fa icon-offset"></i>
                    <g:field type="email" name="email" maxlength="60" class="form-control form-shadow emptySpaces email-admin backend-input" value="${secUserInstance?.email}"/>
                    <span class="input-group-btn">
                        <a href="javascript:;" class="btn green-dark" id="email-checker">
                            <i class="fa fa-check"></i><g:message code="default.checker.button" default="Check"/>
                        </a>
                    </span>
                </div>
                <i class="fa fa-times i-delete-backend i-delete-admin-email"></i> <!-- Delete text icon -->
            </div>
            <div class="help-block email-block">
                <h5 class="text-justify">
                    <g:message code="layouts.main_auth_admin.body.content.admin.create.checker.block.info.email" default="Type an email and check its availability."/>
                </h5>
            </div>
        </div>
    </div>

    <!-- Row -->
    <div class="row space-secondRow">
        <!-- Password -->
        <div class="col-md-6">
            <div class="form-group ${hasErrors(bean: secUserInstance, field: 'password', 'error')}">
                <label for="password" class="control-label">
                    <h5 class="xthin">
                        <g:message code="admin.password.label" default="Password"/>
                        <span class="required"> * </span>
                    </h5>
                </label>
                <div class="input-icon right">
                    <i class="fa"></i>
                    <g:passwordField name="password" class="form-control form-shadow emptySpaces password-space-progress password-admin backendPassword-input" maxlength="32" autocomplete="off"/>
                </div>
                <i class="fa fa-eye i-show-admin-password"></i> <!-- Show password icon -->
            </div>
        </div>

        <!-- Confirm password -->
        <div class="col-md-6 space-betweenCol">
            <div class="form-group ${hasErrors(bean: secUserInstance, field: 'confirmPassword', 'error')}">
                <label for="confirmPassword" class="control-label">
                    <h5 class="xthin">
                        <g:message code="admin.confirmPassword.label" default="Confirm password"/>
                        <span class="required"> * </span>
                    </h5>
                </label>
                <div class="input-icon right">
                    <i class="fa"></i>
                    <g:passwordField name="confirmPassword" class="form-control form-shadow emptySpaces passwordConfirm-admin backendPassword-input" maxlength="32" autocomplete="off"/>
                </div>
                <i class="fa fa-eye i-show-admin-confirmPassword"></i> <!-- Show password icon -->
            </div>
        </div>
    </div>

    <!-- Row -->
    <div class="row">
        <!-- Account expired -->
        <div class="col-sm-6">
            <div class="${hasErrors(bean: secUserInstance, field: 'accountExpired', 'error')}">
                <label for="accountExpired" class="control-label">
                    <h5 class="xthin text-justify">
                        <g:message code="default.user.expired.sublabel" default="Indicate if the user account is expired"/>
                    </h5>
                </label>
                <div class="input-group inputGroup-checkBox">
                    <div class="icheck-list">
                        <g:checkBox name="accountExpired" value="${secUserInstance?.accountExpired}" class="icheck" data-checkbox="icheckbox_line-green" data-label="${g.message(code:'admin.expired.label', default:'Expired account')}"/>
                    </div>
                </div>
            </div>
        </div>
        <!-- Account locked -->
        <div class="col-sm-6">
            <div class="${hasErrors(bean: secUserInstance, field: 'accountLocked', 'error')}">
                <label for="accountLocked" class="control-label">
                    <h5 class="xthin text-justify">
                        <g:message code="default.user.locked.sublabel" default="Indicate if the user account is locked"/>
                    </h5>
                </label>
                <div class="input-group inputGroup-checkBox">
                    <div class="icheck-list">
                        <g:checkBox name="accountLocked" value="${secUserInstance?.accountLocked}" class="icheck" data-checkbox="icheckbox_line-green" data-label="${g.message(code:'admin.locked.label', default:'Locked account')}"/>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Row -->
    <div class="row">
        <!-- Enabled -->
        <div class="col-sm-6">
            <div class="${hasErrors(bean: secUserInstance, field: 'enabled', 'error')}">
                <label for="enabled" class="control-label">
                    <h5 class="xthin text-justify">
                        <g:message code="default.user.enabled.sublabel" default="Indicate if the user account is enabled"/>
                    </h5>
                </label>
                <div class="input-group inputGroup-checkBox">
                    <div class="icheck-list">
                        <g:checkBox name="enabled" value="true" class="icheck" data-checkbox="icheckbox_line-green" data-label="${g.message(code:'admin.enabled.label', default:'Enabled account')}"/>
                    </div>
                </div>
            </div>
        </div>
        <!-- Password expired -->
        <div class="col-sm-6">
            <div class="${hasErrors(bean: secUserInstance, field: 'passwordExpired', 'error')}">
                <label for="passwordExpired" class="control-label">
                    <h5 class="xthin text-justify">
                        <g:message code="default.user.passwordExpired.sublabel" default="Indicate if the user password is expired"/>
                    </h5>
                </label>
                <div class="input-group inputGroup-checkBox">
                    <div class="icheck-list">
                        <g:checkBox name="passwordExpired" value="${secUserInstance?.passwordExpired}" class="icheck" data-checkbox="icheckbox_line-green" data-label="${g.message(code:'admin.passwordExpired.label', default:'Expired password')}"/>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Row -->
    <div class="row space-imageRow">
        <!-- Image profile -->
        <div class="form-group">
            <div class="col-sm-12">
                <legend class="control-label legend-profileImage"><h4 class="title-profileImage size-legend"><g:message code="default.imageProfile.title" default="profile image"/></h4></legend>
                <div class="fileinput fileinput-new" data-provides="fileinput">
                    <div class="fileinput-new thumbnail" data-trigger="fileinput" style="max-width: 160px; max-height: 200px;">
                       <g:if test="${secUserInstance?.avatar}">
                            <img name="avatar" alt="Profile image"  src="${createLink(controller:'controlPanel', action:'profileImage', id:secUserInstance.ident())}" />
                       </g:if>
                       <g:else>
                            <img name="avatar" alt="Profile image" src="${resource(dir: 'img/profile', file: 'user_profile.png')}"/>
                       </g:else>
                    </div>

                    <div class="fileinput-preview fileinput-exists thumbnail" data-trigger="fileinput" style="max-width: 160px; max-height: 200px;"></div>

                    <div>
                        <span class="btn green-dark btn-outline btn-file">
                            <span class="fileinput-new"><g:message code="default.imageProfile.select" default="Select image"/></span>
                            <span class="fileinput-exists"><g:message code="default.imageProfile.change" default="Change"/></span>
                            <input type="file" accept="image/png,image/jpeg,image/gif" name="avatar" id="avatar">
                        </span>
                        <a href="javascript:;" class="btn red-soft fileinput-exists" data-dismiss="fileinput"><g:message code="default.imageProfile.remove" default="Remove"/></a>
                    </div>
                </div>
                <div class="clearfix profileImage-note xthin">
                    <span class="label label-warning"><g:message code="default.imageProfile.note" default="NOTE!"/></span>
                    <p class="text-justify">
                        ${raw(g.message(code:"default.imageProfile.note.description", default:"For best results, your profile image should have a width-to-height ratio of 4:5. For example, if your image is 80 pixels wide, it should be 100 pixels high.<br/><span class='thin'>Maximum image size allowed: 1 MB.</span>"))}
                    </p>
                </div>
            </div>
        </div>
    </div>
</div>
