/*-------------------------------------------------------------------------------------------*
 *                            CUSTOM JAVASCRIPT - GENERAL ELEMENTS                           *
 *-------------------------------------------------------------------------------------------*/

var CustomScript = function () {

    /**
     * Scroll Back to Top
     */
    var scrollBackTop = function() {

        // Browser window scroll (in pixels) after which the "back to top" link is shown
        var offset = 300;
        // Browser window scroll (in pixels) after which the "back to top" link opacity is reduced
        var offset_opacity = 400;
        // Duration of the top scrolling animation (in ms)
        var scroll_top_duration = 700;

        // Grab the "back to top" link
        var back_to_top = $('.back-to-top');

        // Hide or show the "back to top" link
        $(window).scroll(function(){
            ( $(this).scrollTop() > offset ) ? back_to_top.addClass('cd-is-visible cd-fade-out') : back_to_top.removeClass('cd-is-visible');
            if( $(this).scrollTop() > offset_opacity ) {
                back_to_top.removeClass('cd-fade-out');
            }
        });

        // Smooth scroll to top
        back_to_top.on('click', function(event){
            event.preventDefault();
            $('body,html').animate({
                    scrollTop: 0
                }, scroll_top_duration
            );
        });
    };

    /**
     * Handler input function
     */
    var handlerInput = function() {

        /**** INPUT - ICONS ****/
        var userInput = $('.user-input');
        var deleteIcon = $('.i-delete');
        var passwordInput = $(".password-input");
        var showIcon = $('.i-show');
        var passwordConfirmInput = $(".password-confirm-input");
        var showConfirmIcon = $('.i-show-confirm');
        var isMobile = { /* Mobile device */
            Android: function() {
                return navigator.userAgent.match(/Android/i);
            },
            BlackBerry: function() {
                return navigator.userAgent.match(/BlackBerry/i);
            },
            iOS: function() {
                return navigator.userAgent.match(/iPhone|iPad|iPod/i);
            },
            Opera: function() {
                return navigator.userAgent.match(/Opera Mini/i);
            },
            Windows: function() {
                return navigator.userAgent.match(/IEMobile/i) || navigator.userAgent.match(/WPDesktop/i);
            },
            any: function() {
                return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows());
            }
        };

        /**** USERNAME/EMAIL FIELD ****/
        /* Show delete icon */
        userInput.keydown(function(){
            deleteIcon.show();
        });

        /* Delete text and hide delete icon */
        deleteIcon.click(function() {
            userInput.val('').focus();
            deleteIcon.hide();

        });

        /* Hide delete icon when user deletes text with the keyboard */
        var toggleClasses = function() {
            if (userInput.val() == '') {
                deleteIcon.hide();
            }
        };
        userInput.on('keyup keydown keypress change paste', function() {
            toggleClasses(); // Still toggles the classes on any of the above events
        });
        toggleClasses(); // And also on document ready

        /**** PASSWORD FIELD ****/
        /* Show eye icon */
        passwordInput.keydown(function(){
            showIcon.show();
            showIcon.css( {
                'cursor' : 'pointer',
                'right' : 50 });
        });

        /* Hide eye icon when user deletes text with the keyboard */
        var toggleClassesPassword = function() {
            if (passwordInput.val() == '') {
                showIcon.hide();
            }
        };
        passwordInput.on('keyup keydown keypress change paste', function() {
            toggleClassesPassword(); // Still toggles the classes on any of the above events
        });
        toggleClassesPassword(); // and also on document ready


        /* Check if it is a mobile device */
        if( isMobile.any() ) {

            /* Check if it is Internet Explorer - Trident and rv:11 belongs to IE 11 */
            if ((navigator.userAgent.match(/msie/i)) ||  (navigator.userAgent.match(/Trident/)
                && navigator.userAgent.match(/rv:11/))) {

                /* Drop */
                showIcon.on('touchend click', function(e){
                    e.stopPropagation(); e.preventDefault();
                    passwordInput.attr('type', 'password');
                });

                /* Hold */
                showIcon.on('touchstart click', function(e){
                    e.stopPropagation(); e.preventDefault();
                    passwordInput.attr('type', 'field');
                });

            } else {

                /* Drop */
                showIcon.on('touchend click', function(e){
                    e.stopPropagation(); e.preventDefault();
                    passwordInput.prop('type', 'password');
                });

                /* Hold */
                showIcon.on('touchstart click', function(e){
                    e.stopPropagation(); e.preventDefault();
                    passwordInput.prop('type', 'field');
                });
            }
        } else {

            /* Check if it is Internet Explorer - Trident and rv:11 belongs to IE 11 */
            if ((navigator.userAgent.match(/msie/i)) ||  (navigator.userAgent.match(/Trident/)
                && navigator.userAgent.match(/rv:11/))) {

                /* Drop */
                showIcon.mouseup(function() {
                    passwordInput.attr('type', 'password');
                });

                /* Hold */
                showIcon.mousedown(function() {
                    passwordInput.attr('type', 'field');
                });

            } else {

                /* Drop */
                showIcon.mouseup(function() {
                    passwordInput.prop('type', 'password');
                });

                /* Hold */
                showIcon.mousedown(function() {
                    passwordInput.prop('type', 'field');
                });
            }
        }
        /**** PASSWORD CONFIRM FIELD ****/
        /* Show eye icon */
        passwordConfirmInput.keydown(function(){
            showConfirmIcon.show();
            showConfirmIcon.css( {
                'cursor' : 'pointer',
                'right' : 50 });
        });

        /* Hide eye icon when user deletes text with the keyboard */
        var toggleClassesPasswordConfirm = function() {
            if (passwordConfirmInput.val() == '') {
                showConfirmIcon.hide();
            }
        };
        passwordConfirmInput.on('keyup keydown keypress change paste', function() {
            toggleClassesPasswordConfirm(); // Still toggles the classes on any of the above events
        });
        toggleClassesPasswordConfirm(); // and also on document ready


        /* Check if it is a mobile device */
        if( isMobile.any() ) {

            /* Check if it is Internet Explorer - Trident and rv:11 belongs to IE 11 */
            if ((navigator.userAgent.match(/msie/i)) ||  (navigator.userAgent.match(/Trident/)
                && navigator.userAgent.match(/rv:11/))) {

                /* Drop */
                showConfirmIcon.on('touchend click', function(e){
                    e.stopPropagation(); e.preventDefault();
                    passwordConfirmInput.attr('type', 'password');
                });

                /* Hold */
                showConfirmIcon.on('touchstart click', function(e){
                    e.stopPropagation(); e.preventDefault();
                    passwordConfirmInput.attr('type', 'field');
                });

            } else {

                /* Drop */
                showConfirmIcon.on('touchend click', function(e){
                    e.stopPropagation(); e.preventDefault();
                    passwordConfirmInput.prop('type', 'password');
                });

                /* Hold */
                showConfirmIcon.on('touchstart click', function(e){
                    e.stopPropagation(); e.preventDefault();
                    passwordConfirmInput.prop('type', 'field');
                });
            }
        } else {

            /* Check if it is Internet Explorer - Trident and rv:11 belongs to IE 11 */
            if ((navigator.userAgent.match(/msie/i)) ||  (navigator.userAgent.match(/Trident/)
                && navigator.userAgent.match(/rv:11/))) {

                /* Drop */
                showConfirmIcon.mouseup(function() {
                    passwordConfirmInput.attr('type', 'password');
                });

                /* Hold */
                showConfirmIcon.mousedown(function() {
                    passwordConfirmInput.attr('type', 'field');
                });

            } else {

                /* Drop */
                showConfirmIcon.mouseup(function() {
                    passwordConfirmInput.prop('type', 'password');
                });

                /* Hold */
                showConfirmIcon.mousedown(function() {
                    passwordConfirmInput.prop('type', 'field');
                });
            }
        }
    };

    /**
     * It handles datatable
     */
    var handlerDatatable = function() {
        $('.dataTables_filter').find('input').addClass('form-shadow');
        $('.dataTables_filter').find('input').after('<i class="fa fa-search search-datatable"></i>');
        $('.dataTables_length').find('select').addClass('form-shadow');
    };

    /**
     * It disallows the empty spaces
     */
    var handlerDisallowSpaces = function() {
        
        $(".emptySpaces").on({
            keydown: function(e) {
                if (e.which === 32)
                    return false;
            },
            change: function() {
                this.value = this.value.replace(/\s/g, "");
            }
        });
    };

    /**
     * Handler icons in input fields of secUser
     */
    var handlerIconQuickSearch = function() {

        var quickSearchInput = $('.quickSearch-input');
        var iconQuickSearch = $('.i-delete-quickSearch');

        // Show delete icon
        quickSearchInput.keydown(function () {
            iconQuickSearch.show();
        });

        // Delete text and hide delete icon
        iconQuickSearch.click(function () {
            quickSearchInput.val('').focus();
            iconQuickSearch.hide();
        });

        // Hide delete icon when user deletes text with the keyboard
        var toggleClasses = function () {
            if (quickSearchInput.val() == '') {
                iconQuickSearch.hide();
            }
        };
        quickSearchInput.on('keyup keydown keypress change paste', function () {
            toggleClasses(); // Still toggles the classes on any of the above events
        });
        toggleClasses(); // And also on document ready
    };

    /**
     * It handles the icon colour in user pages (page bar)
     */
    var handlerIconColourPageBar = function() {

        var homePageBreadcumb = $('.page-bar-user .page-breadcrumb > li > a');
        var iconHomeBreadcumb = $('.page-bar-user .page-breadcrumb .icofont-ui-home');

        homePageBreadcumb.mouseover(function () {
            iconHomeBreadcumb.addClass('ui-home-hover')
        });

        homePageBreadcumb.mouseout(function () {
            iconHomeBreadcumb.removeClass('ui-home-hover')
        });
    };

    return {
        // Main function to initiate the module
        init: function () {
            scrollBackTop();
            handlerInput();
            handlerDatatable();
            handlerDisallowSpaces();
            handlerIconQuickSearch();
            handlerIconColourPageBar();
        }
    };
}();

jQuery(document).ready(function() {
    CustomScript.init();
});
