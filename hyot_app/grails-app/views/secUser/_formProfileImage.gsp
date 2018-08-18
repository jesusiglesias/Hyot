<%@ page import="Security.SecUser" %>

<div class="form-body">
    <!-- Row -->
    <div class="row space-firstRow">
        <!-- Image profile -->
        <div class="form-group">
            <div class="col-sm-12">
                <legend class="control-label legend-profileImage"><h4 class="title-profileImage size-legend"><g:message code="default.imageProfile.title" default="profile image"/></h4></legend>
                <div class="fileinput fileinput-new" data-provides="fileinput">
                    <div class="fileinput-new thumbnail" data-trigger="fileinput" style="max-width: 160px; max-height: 300px;">
                        <g:if test="${secUser?.avatar}">
                            <img name="avatar" alt="Profile image"  src="${createLink(controller:'controlPanel', action:'profileImage', id:secUser.ident())}" />
                        </g:if>
                        <g:else>
                            <img name="avatar" alt="Profile image" src="${resource(dir: 'img/profile', file: 'user_profile.png')}"/>
                        </g:else>
                    </div>

                    <div class="fileinput-preview fileinput-exists thumbnail" data-trigger="fileinput" style="max-width: 170px; max-height: 300px;"></div>

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
                        ${raw(g.message(code:"default.imageProfile.note.description", default:"For best results, your profile image should have a width-to-height ratio of 4:5. For example, if your image is 80 pixels wide, it should be 100 pixels high.<br/><strong>Maximum image size allowed: 1 MB.</strong>"))}
                    </p>
                </div>
            </div>
        </div>
    </div>
</div>
