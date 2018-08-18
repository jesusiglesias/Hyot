/*-------------------------------------------------------------------------------------------*
 *                                  JAVASCRIPT - ICONS USER                                  *
 *-------------------------------------------------------------------------------------------*/

var iconUserHandler = function () {

    /**
     * Handler icons in input fields of user
     */
    var handlerIconUser = function() {

        var userUsername = $('.username-user');
        var iconUserUsername = $('.i-delete-user-username');
        var userEmail = $('.email-user');
        var iconUserEmail = $('.i-delete-user-email');
        var userPassword = $(".password-user");
        var iconUserPassword = $('.i-show-user-password');
        var userConfirmPassword = $(".passwordConfirm-user");
        var iconUserConfirmPassword = $('.i-show-user-confirmPassword');
        var userName = $('.name-user');
        var iconUserName = $('.i-delete-user-name');
        var userSurname = $('.surname-user');
        var iconUserSurname = $('.i-delete-user-surname');

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
        userUsername.keydown(function(){
            iconUserUsername.show();
        });

        // Delete text and hide delete icon
        iconUserUsername.click(function() {
            userUsername.val('').focus();
            iconUserUsername.hide();
        });

        // Hide delete icon when user deletes text with the keyboard
        var toggleClassesUsername = function() {
            if (userUsername.val() == '') {
                iconUserUsername.hide();
            }
        };

        userUsername.on('keyup keydown keypress change paste', function() {
            toggleClassesUsername(); // Still toggles the classes on any of the above events
        });
        toggleClassesUsername(); // And also on document ready

        /**
         * Email
         */
        // Show delete icon
        userEmail.keydown(function(){
            iconUserEmail.show();
        });

        // Delete text and hide delete icon
        iconUserEmail.click(function() {
            userEmail.val('').focus();
            iconUserEmail.hide();
        });

        // Hide delete icon when user deletes text with the keyboard
        var toggleClassesEmail = function() {
            if (userEmail.val() == '') {
                iconUserEmail.hide();
            }
        };

        userEmail.on('keyup keydown keypress change paste', function() {
            toggleClassesEmail(); // Still toggles the classes on any of the above events
        });
        toggleClassesEmail(); // And also on document ready

        /**
         * Password
         */
        // Show eye icon
        userPassword.keydown(function(){
            iconUserPassword.show();
            iconUserPassword.css( {
                'cursor' : 'pointer',
                'top' : 51,
                'right': 55,
                'position': 'absolute',
                'color': '#AAAAAA' });
        });

        // Hide eye icon when user deletes text with the keyboard
        var toggleClassesPassword = function() {
            if (userPassword.val() == '') {
                iconUserPassword.hide();
            }
        };
        userPassword.on('keyup keydown keypress change paste', function() {
            toggleClassesPassword(); // Still toggles the classes on any of the above events
        });
        toggleClassesPassword(); // and also on document ready


        // Check if it is a mobile device
        if( isMobile.any() ) {

            // Check if it is Internet Explorer - Trident and rv:11 belongs to IE 11
            if ((navigator.userAgent.match(/msie/i)) ||  (navigator.userAgent.match(/Trident/)
                && navigator.userAgent.match(/rv:11/))) {

                // Drop
                iconUserPassword.on('touchend click', function(e){
                    e.stopPropagation(); e.preventDefault();
                    userPassword.attr('type', 'password');
                });

                // Hold
                iconUserPassword.on('touchstart click', function(e){
                    e.stopPropagation(); e.preventDefault();
                    userPassword.attr('type', 'field');
                });

            } else {

                // Drop
                iconUserPassword.on('touchend click', function(e){
                    e.stopPropagation(); e.preventDefault();
                    userPassword.prop('type', 'password');
                });

                // Hold
                iconUserPassword.on('touchstart click', function(e){
                    e.stopPropagation(); e.preventDefault();
                    userPassword.prop('type', 'field');
                });
            }
        } else {

            // Check if it is Internet Explorer - Trident and rv:11 belongs to IE 11
            if ((navigator.userAgent.match(/msie/i)) ||  (navigator.userAgent.match(/Trident/)
                && navigator.userAgent.match(/rv:11/))) {

                // Drop
                iconUserPassword.mouseup(function() {
                    userPassword.attr('type', 'password');
                });

                // Hold
                iconUserPassword.mousedown(function() {
                    userPassword.attr('type', 'field');
                });

            } else {

                // Drop
                iconUserPassword.mouseup(function() {
                    userPassword.prop('type', 'password');
                });

                // Hold
                iconUserPassword.mousedown(function() {
                    userPassword.prop('type', 'field');
                });
            }
        }

        /**
         * Confirm password
         */
        // Show eye icon
        userConfirmPassword.keydown(function(){
            iconUserConfirmPassword.show();
            iconUserConfirmPassword.css( {
                'cursor' : 'pointer',
                'top' : 51,
                'right': 55,
                'position': 'absolute',
                'color': '#AAAAAA' });
        });

        // Hide eye icon when user deletes text with the keyboard
        var toggleClassesPasswordConfirm = function() {
            if (userConfirmPassword.val() == '') {
                iconUserConfirmPassword.hide();
            }
        };
        userConfirmPassword.on('keyup keydown keypress change paste', function() {
            toggleClassesPasswordConfirm(); // Still toggles the classes on any of the above events
        });
        toggleClassesPasswordConfirm(); // and also on document ready


        // Check if it is a mobile device
        if( isMobile.any() ) {

            // Check if it is Internet Explorer - Trident and rv:11 belongs to IE 11
            if ((navigator.userAgent.match(/msie/i)) ||  (navigator.userAgent.match(/Trident/)
                && navigator.userAgent.match(/rv:11/))) {

                // Drop
                iconUserConfirmPassword.on('touchend click', function(e){
                    e.stopPropagation(); e.preventDefault();
                    userConfirmPassword.attr('type', 'password');
                });

                // Hold
                iconUserConfirmPassword.on('touchstart click', function(e){
                    e.stopPropagation(); e.preventDefault();
                    userConfirmPassword.attr('type', 'field');
                });

            } else {

                // Drop
                iconUserConfirmPassword.on('touchend click', function(e){
                    e.stopPropagation(); e.preventDefault();
                    userConfirmPassword.prop('type', 'password');
                });

                // Hold
                iconUserConfirmPassword.on('touchstart click', function(e){
                    e.stopPropagation(); e.preventDefault();
                    userConfirmPassword.prop('type', 'field');
                });
            }
        } else {

            // Check if it is Internet Explorer - Trident and rv:11 belongs to IE 11
            if ((navigator.userAgent.match(/msie/i)) ||  (navigator.userAgent.match(/Trident/)
                && navigator.userAgent.match(/rv:11/))) {

                // Drop
                iconUserConfirmPassword.mouseup(function() {
                    userConfirmPassword.attr('type', 'password');
                });

                // Hold
                iconUserConfirmPassword.mousedown(function() {
                    userConfirmPassword.attr('type', 'field');
                });

            } else {

                // Drop
                iconUserConfirmPassword.mouseup(function() {
                    userConfirmPassword.prop('type', 'password');
                });

                // Hold
                iconUserConfirmPassword.mousedown(function() {
                    userConfirmPassword.prop('type', 'field');
                });
            }
        }

        /**
         * Name
         */
        // Show delete icon
        userName.keydown(function(){
            iconUserName.show();
        });

        // Delete text and hide delete icon
        iconUserName.click(function() {
            userName.val('').focus();
            iconUserName.hide();
        });

        // Hide delete icon when user deletes text with the keyboard
        var toggleClassesName = function() {
            if (userName.val() == '') {
                iconUserName.hide();
            }
        };

        userName.on('keyup keydown keypress change paste', function() {
            toggleClassesName(); // Still toggles the classes on any of the above events
        });
        toggleClassesName(); // And also on document ready

        /**
         * Surname
         */
        // Show delete icon
        userSurname.keydown(function(){
            iconUserSurname.show();
        });

        // Delete text and hide delete icon
        iconUserSurname.click(function() {
            userSurname.val('').focus();
            iconUserSurname.hide();
        });

        // Hide delete icon when user deletes text with the keyboard
        var toggleClassesSurname = function() {
            if (userSurname.val() == '') {
                iconUserSurname.hide();
            }
        };

        userSurname.on('keyup keydown keypress change paste', function() {
            toggleClassesSurname(); // Still toggles the classes on any of the above events
        });
        toggleClassesSurname(); // And also on document ready
    };

    return {
        // Main function to initiate the module
        init: function () {
            handlerIconUser();
        }
    };
}();

jQuery(document).ready(function() {
    iconUserHandler.init();
});
