<%@ page import="User.User;" %>

<div class="form-body">
    <!-- Row -->
    <div class="row">
        <div class="col-xs-12">
            <legend class="control-label legend-profileImage"><h4 class="title-profileImage size-legend xthin"><g:message code="default.accountInformation.title" default="User account"/></h4></legend>
        </div>
        <!-- Username -->
        <div class="col-md-6">
            <div class="form-group ${hasErrors(bean: user, field: 'username', 'error')}">
                <label for="username" class="control-label">
                    <h5 class="xthin">
                        <g:message code="user.username.label" default="Username"/>
                        <span class="required"> * </span>
                    </h5>
                </label>
                <div class="input-group input-icon right">
                    <i class="fa icon-offset"></i>
                    <g:textField name="username" maxlength="30" class="form-control form-shadow emptySpaces username-user backend-input" value="${user?.username}"/>
                    <span class="input-group-btn">
                        <a href="javascript:;" class="btn green-dark" id="username-checker">
                            <i class="fa fa-check"></i><g:message code="default.checker.button" default="Check"/>
                        </a>
                    </span>
                </div>
                <i class="fa fa-times i-delete-username-backend i-delete-user-username"></i> <!-- Delete text icon -->
            </div>
            <div class="help-block username-block">
                <h5 class="text-justify">
                    <g:message code="layouts.main_auth_admin.body.content.admin.create.checker.block.info.username" default="Type a username and check its availability."/>
                </h5>
            </div>
        </div>

        <!-- Email -->
        <div class="col-md-6 space-betweenCol">
            <div class="form-group ${hasErrors(bean: user, field: 'email', 'error')}">
                <label for="email" class="control-label">
                    <h5 class="xthin">
                        <g:message code="user.email.label" default="Email"/>
                        <span class="required"> * </span>
                    </h5>
                </label>
                <div class="input-group input-icon right">
                    <i class="fa icon-offset"></i>
                    <g:field type="email" name="email" maxlength="60" class="form-control form-shadow emptySpaces email-user backend-input" value="${user?.email}"/>
                    <span class="input-group-btn">
                        <a href="javascript:;" class="btn green-dark" id="email-checker">
                            <i class="fa fa-check"></i><g:message code="default.checker.button" default="Check"/>
                        </a>
                    </span>
                </div>
                <i class="fa fa-times i-delete-backend i-delete-user-email"></i> <!-- Delete text icon -->
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
        <!-- Account expired -->
        <div class="col-sm-6">
            <div class="${hasErrors(bean: user, field: 'accountExpired', 'error')}">
                <label for="accountExpired" class="control-label">
                    <h5 class="xthin text-justify">
                        <g:message code="default.user.expired.sublabel" default="Indicate if the user account is expired"/>
                    </h5>
                </label>
                <div class="input-group inputGroup-checkBox">
                    <div class="icheck-list">
                        <g:checkBox name="accountExpired" value="${user?.accountExpired}" class="icheck" data-checkbox="icheckbox_line-green" data-label="${g.message(code:'admin.expired.label', default:'Expired account')}"/>
                    </div>
                </div>
            </div>
        </div>
        <!-- Account locked -->
        <div class="col-sm-6">
            <div class="${hasErrors(bean: user, field: 'accountLocked', 'error')}">
                <label for="accountLocked" class="control-label">
                    <h5 class="xthin text-justify">
                        <g:message code="default.user.locked.sublabel" default="Indicate if the user account is locked"/>
                    </h5>
                </label>
                <div class="input-group inputGroup-checkBox">
                    <div class="icheck-list">
                        <g:checkBox name="accountLocked" value="${user?.accountLocked}" class="icheck" data-checkbox="icheckbox_line-green" data-label="${g.message(code:'admin.locked.label', default:'Locked account')}"/>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Row -->
    <div class="row">
        <!-- Enabled -->
        <div class="col-sm-6">
            <div class="${hasErrors(bean: user, field: 'enabled', 'error')}">
                <label for="enabled" class="control-label">
                    <h5 class="xthin text-justify">
                        <g:message code="default.user.enabled.sublabel" default="Indicate if the user account is enabled"/>
                    </h5>
                </label>
                <div class="input-group inputGroup-checkBox">
                    <div class="icheck-list">
                        <g:checkBox name="enabled" value="${user?.enabled}" class="icheck" data-checkbox="icheckbox_line-green" data-label="${g.message(code:'admin.enabled.label', default:'Enabled account')}"/>
                    </div>
                </div>
            </div>
        </div>
        <!-- Password expired -->
        <div class="col-sm-6">
            <div class="${hasErrors(bean: user, field: 'passwordExpired', 'error')}">
                <label for="passwordExpired" class="control-label">
                    <h5 class="xthin text-justify">
                        <g:message code="default.user.passwordExpired.sublabel" default="Indicate if the user password is expired"/>
                    </h5>
                </label>
                <div class="input-group inputGroup-checkBox">
                    <div class="icheck-list">
                        <g:checkBox name="passwordExpired" value="${user?.passwordExpired}" class="icheck" data-checkbox="icheckbox_line-green" data-label="${g.message(code:'admin.passwordExpired.label', default:'Expired password')}"/>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Row -->
    <div class="row space-secondRow">
        <div class="col-xs-12">
            <legend class="control-label legend-profileImage"><h4 class="title-profileImage size-legend"><g:message code="default.privateInformation.title" default="Personal information"/></h4></legend>
        </div>
        <!-- Name -->
        <div class="col-md-6">
            <div class="form-group ${hasErrors(bean: user, field: 'name', 'error')}">
                <label for="name" class="control-label">
                    <h5 class="xthin">
                        <g:message code="user.name.label" default="Name"/>
                        <span class="required"> * </span>
                    </h5>
                </label>
                <div class="input-icon right">
                    <i class="fa"></i>
                    <g:textField name="name" maxlength="25" value="${user?.name}" class="form-control form-shadow name-user backend-input"/>
                </div>
                <i class="fa fa-times i-delete-without-name-backend i-delete-user-name"></i> <!-- Delete text icon -->
            </div>
        </div>

        <!-- Surname -->
        <div class="col-md-6 space-betweenCol">
            <div class="form-group ${hasErrors(bean: user, field: 'surname', 'error')}">
                <label for="surname" class="control-label">
                    <h5 class="xthin">
                        <g:message code="user.surname.label" default="Surname"/>
                        <span class="required"> * </span>
                    </h5>
                </label>
                <div class="input-icon right">
                    <i class="fa"></i>
                    <g:textField name="surname" maxlength="40" value="${user?.surname}" class="form-control form-shadow surname-user backend-input"/>
                </div>
                <i class="fa fa-times i-delete-without-backend i-delete-user-surname"></i> <!-- Delete text icon -->
            </div>
        </div>
    </div>
</div>