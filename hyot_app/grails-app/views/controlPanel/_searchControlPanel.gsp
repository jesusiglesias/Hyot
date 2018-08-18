<li class="sidebar-search-wrapper">
    <g:form class="sidebar-search" controller="user" action="index">
        <a href="javascript:;" class="remove">
            <i class="icon-close"></i>
        </a>
        <div class="input-group">
            <!-- ie8, ie9 does not support html5 placeholder, so it just shows field title for that-->
            <label class="control-label visible-ie8 visible-ie9" for="quickSearch"><g:message code="layouts.main_auth_admin.sidebar.search" default="Search..."/></label>
            <g:textField name="quickSearch" class="form-control placeholder-no-fix quickSearch-input backend-input" placeholder="${message(code:'layouts.main_auth_admin.sidebar.search', default:'Search...')}" autocomplete="on"/>
            <i class="fa fa-times i-delete-quickSearch"></i> <!-- Delete text icon -->
            <span class="input-group-btn">
                <a href="javascript:;" class="btn submit search-custom">
                    <i class="icon-magnifier"></i>
                </a>
            </span>
        </div>
    </g:form>
</li> <!-- /.Search form -->
