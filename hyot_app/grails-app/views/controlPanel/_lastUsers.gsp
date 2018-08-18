<!-- Users registered: lastest 10 -->
<g:each in="${lastUsers}" var="user">
    <div class="mt-comments">
        <div class="mt-comment">
            <div class="mt-comment-img">
                <img class="img-circle recentUser-image" alt="Profile image" src="${resource(dir: 'img/profile', file: 'user_profile.png')}"/>
            </div>
            <div class="mt-comment-body">
                <div class="mt-comment-info">
                    <span class="mt-comment-author">${user?.username}</span>
                    <span class="mt-comment-date"><g:formatDate formatName="custom.date.format" date="${user?.dateCreated}" class="format-date"/></span>
                </div>
                <div class="mt-comment-text">${user?.email}</div>
                <div class="mt-comment-details">
                    <g:if test="${user?.enabled}">
                        <span class="mt-comment-status label label-sm label-success circle">
                    </g:if>
                    <g:else>
                        <span class="mt-comment-status label label-sm label-info circle">
                    </g:else>
                    <g:formatBoolean boolean="${user?.enabled}" true="${g.message(code: "default.enabled.label.true", default: "Confirmed")}" false="${g.message(code: "default.enabled.label.false", default: "Pending")}"/>
                </span>
                    <ul class="mt-comment-actions">
                        <li>
                            <g:link controller="user" action="edit" id="${user?.id}" class="btn blue-soft"><g:message code="default.button.edit.label" default="Edit"/></g:link>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</g:each>