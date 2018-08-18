/*-------------------------------------------------------------------------------------------*
 *                                JAVASCRIPT - ICONS SEC USER                                *
 *-------------------------------------------------------------------------------------------*/

var iconSecUserHandler = function () {

    /**
     * Handler icons in input fields of secUser
     */
    var handlerIconSecUser = function() {

        var secUserUsername = $('.username-admin');
        var iconSecUserUsername = $('.i-delete-admin-username');
        var secUserEmail = $('.email-admin');
        var iconSecUserEmail = $('.i-delete-admin-email');
        var secUserPassword = $(".password-admin");
        var iconSecUserPassword = $('.i-show-admin-password');
        var secUserConfirmPassword = $(".passwordConfirm-admin");
        var iconSecUserConfirmPassword = $('.i-show-admin-confirmPassword');

        var isMobile = { // Mobile device
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

        /**
         * Username
         */
        // Show delete icon
        secUserUsername.keydown(function(){
            iconSecUserUsername.show();
        });

        // Delete text and hide delete icon
        iconSecUserUsername.click(function() {
            secUserUsername.val('').focus();
            iconSecUserUsername.hide();
        });

        // Hide delete icon when user deletes text with the keyboard
        var toggleClassesUsername = function() {
            if (secUserUsername.val() == '') {
                iconSecUserUsername.hide();
            }
        };
        secUserUsername.on('keyup keydown keypress change paste', function() {
            toggleClassesUsername(); // Still toggles the classes on any of the above events
        });
        toggleClassesUsername(); // And also on document ready

        /**
         * Email
         */
        // Show delete icon
        secUserEmail.keydown(function(){
            iconSecUserEmail.show();
        });

        // Delete text and hide delete icon
        iconSecUserEmail.click(function() {
            secUserEmail.val('').focus();
            iconSecUserEmail.hide();
        });

        // Hide delete icon when user deletes text with the keyboard
        var toggleClassesEmail = function() {
            if (secUserEmail.val() == '') {
                iconSecUserEmail.hide();
            }
        };

        secUserEmail.on('keyup keydown keypress change paste', function() {
            toggleClassesEmail(); // Still toggles the classes on any of the above events
        });
        toggleClassesEmail(); // And also on document ready

        /**
         * Password
         */
        // Show eye icon
        secUserPassword.keydown(function(){
            iconSecUserPassword.show();
            iconSecUserPassword.css( {
                'cursor' : 'pointer',
                'top' : 51,
                'right': 55,
                'position': 'absolute',
                'color': '#AAAAAA' });
        });

        // Hide eye icon when user deletes text with the keyboard
        var toggleClassesPassword = function() {
            if (secUserPassword.val() == '') {
                iconSecUserPassword.hide();
            }
        };
        secUserPassword.on('keyup keydown keypress change paste', function() {
            toggleClassesPassword(); // Still toggles the classes on any of the above events
        });
        toggleClassesPassword(); // and also on document ready


        // Check if it is a mobile device
        if( isMobile.any() ) {

            // Check if it is Internet Explorer - Trident and rv:11 belongs to IE 11
            if ((navigator.userAgent.match(/msie/i)) ||  (navigator.userAgent.match(/Trident/)
                && navigator.userAgent.match(/rv:11/))) {

                // Drop
                iconSecUserPassword.on('touchend click', function(e){
                    e.stopPropagation(); e.preventDefault();
                    secUserPassword.attr('type', 'password');
                });

                // Hold
                iconSecUserPassword.on('touchstart click', function(e){
                    e.stopPropagation(); e.preventDefault();
                    secUserPassword.attr('type', 'field');
                });

            } else {

                // Drop
                iconSecUserPassword.on('touchend click', function(e){
                    e.stopPropagation(); e.preventDefault();
                    secUserPassword.prop('type', 'password');
                });

                // Hold
                iconSecUserPassword.on('touchstart click', function(e){
                    e.stopPropagation(); e.preventDefault();
                    secUserPassword.prop('type', 'field');
                });
            }
        } else {

            // Check if it is Internet Explorer - Trident and rv:11 belongs to IE 11
            if ((navigator.userAgent.match(/msie/i)) ||  (navigator.userAgent.match(/Trident/)
                && navigator.userAgent.match(/rv:11/))) {

                // Drop
                iconSecUserPassword.mouseup(function() {
                    secUserPassword.attr('type', 'password');
                });

                // Hold
                iconSecUserPassword.mousedown(function() {
                    secUserPassword.attr('type', 'field');
                });

            } else {

                // Drop
                iconSecUserPassword.mouseup(function() {
                    secUserPassword.prop('type', 'password');
                });

                // Hold
                iconSecUserPassword.mousedown(function() {
                    secUserPassword.prop('type', 'field');
                });
            }
        }

        /**
         * Confirm password
         */
        // Show eye icon
        secUserConfirmPassword.keydown(function(){
            iconSecUserConfirmPassword.show();
            iconSecUserConfirmPassword.css( {
                'cursor' : 'pointer',
                'top' : 51,
                'right': 55,
                'position': 'absolute',
                'color': '#AAAAAA' });
        });

        // Hide eye icon when user deletes text with the keyboard
        var toggleClassesPasswordConfirm = function() {
            if (secUserConfirmPassword.val() == '') {
                iconSecUserConfirmPassword.hide();
            }
        };
        secUserConfirmPassword.on('keyup keydown keypress change paste', function() {
            toggleClassesPasswordConfirm(); // Still toggles the classes on any of the above events
        });
        toggleClassesPasswordConfirm(); // and also on document ready


        // Check if it is a mobile device
        if( isMobile.any() ) {

            // Check if it is Internet Explorer - Trident and rv:11 belongs to IE 11
            if ((navigator.userAgent.match(/msie/i)) ||  (navigator.userAgent.match(/Trident/)
                && navigator.userAgent.match(/rv:11/))) {

                // Drop
                iconSecUserConfirmPassword.on('touchend click', function(e){
                    e.stopPropagation(); e.preventDefault();
                    secUserConfirmPassword.attr('type', 'password');
                });

                // Hold
                iconSecUserConfirmPassword.on('touchstart click', function(e){
                    e.stopPropagation(); e.preventDefault();
                    secUserConfirmPassword.attr('type', 'field');
                });

            } else {

                // Drop
                iconSecUserConfirmPassword.on('touchend click', function(e){
                    e.stopPropagation(); e.preventDefault();
                    secUserConfirmPassword.prop('type', 'password');
                });

                // Hold
                iconSecUserConfirmPassword.on('touchstart click', function(e){
                    e.stopPropagation(); e.preventDefault();
                    secUserConfirmPassword.prop('type', 'field');
                });
            }
        } else {

            // Check if it is Internet Explorer - Trident and rv:11 belongs to IE 11
            if ((navigator.userAgent.match(/msie/i)) ||  (navigator.userAgent.match(/Trident/)
                && navigator.userAgent.match(/rv:11/))) {

                // Drop
                iconSecUserConfirmPassword.mouseup(function() {
                    secUserConfirmPassword.attr('type', 'password');
                });

                // Hold
                iconSecUserConfirmPassword.mousedown(function() {
                    secUserConfirmPassword.attr('type', 'field');
                });

            } else {

                // Drop
                iconSecUserConfirmPassword.mouseup(function() {
                    secUserConfirmPassword.prop('type', 'password');
                });

                // Hold
                iconSecUserConfirmPassword.mousedown(function() {
                    secUserConfirmPassword.prop('type', 'field');
                });
            }
        }
    };

    return {
        // Main function to initiate the module
        init: function () {
            handlerIconSecUser();
        }
    };
}();

jQuery(document).ready(function() {
    iconSecUserHandler.init();
});
