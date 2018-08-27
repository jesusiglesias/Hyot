/*-------------------------------------------------------------------------------------------*
 *                         PROFILE USER - PASSWORD VALIDATION JAVASCRIPT                     *
 *-------------------------------------------------------------------------------------------*/

var DomainPasswordProfileValidation = function () {

    /**
     * Profile user validation - Password
     */
    var handlerPasswordProfileValidation = function() {

        var profilePasswordForm = $('.profilePassword-form');

        jQuery.validator.addMethod("notEqualToUsername", function(value, element, param) {
            return this.optional(element) || value.toLowerCase() != $(param).val().toLowerCase();
        }, _equalPasswordUsername);

        profilePasswordForm.validate({
            errorElement: 'span', // Default input error message container
            errorClass: 'help-block help-block-error', // Default input error message class
            focusInvalid: false, // Do not focus the last invalid input
            ignore: "",  // Validate all fields including form hidden input
            rules: {
                currentPassword: {
                    required: true,
                    minlength: 8,
                    maxlength: 32
                },
                password: {
                    required: true,
                    minlength: 8,
                    maxlength: 32,
                    notEqualToUsername:'#username'
                },
                confirmPassword: {
                    required: true,
                    minlength:8,
                    maxlength: 32,
                    equalTo: "#password"
                }
            },
            messages: {
                currentPassword: {
                    required: _requiredField,
                    minlength: _minlengthField,
                    maxlength: _maxlengthField
                },
                password: {
                    required: _requiredField,
                    minlength: _minlengthField,
                    maxlength: _maxlengthField,
                    notEqualToUsername: _equalPasswordUsername
                },
                confirmPassword: {
                    required: _requiredField,
                    minlength: _minlengthField,
                    maxlength: _maxlengthField,
                    equalTo: _equalPassword
                }
            },

            // Render error placement for each input type
            errorPlacement: function (error, element) {
                var icon = $(element).parent('.input-icon').children('i');
                icon.removeClass('fa-check').addClass("fa-warning");
                icon.attr("data-original-title", error.text()).tooltip({'container': 'body'});
            },

            // Set error class to the control group
            highlight: function (element) {
                $(element)
                    .closest('.form-group').removeClass("has-success").addClass('has-error');
            },

            // Set success class to the control group
            success: function (label, element) {
                var icon = $(element).parent('.input-icon').children('i');
                $(element).closest('.form-group').removeClass('has-error').addClass('has-success');
                icon.removeClass("fa-warning").addClass("fa-check");
            },

            submitHandler: function (form) {
                form.submit(); // Submit the form
            }
        });
    };

    /**
     * Handler icons in input fields of user profile
     */
    var handlerIconUserProfile = function() {

        /**** INPUT - ICONS ****/
        var currentPasswordInput = $(".profile-current-password");
        var currentPassowrdIcon = $('.i-show-profile-currentPassword');
        var passwordInput = $(".profile-new-password");
        var passwordIcon = $('.i-show-profile-newPassword');
        var confirmPasswordInput = $(".profile-confirm-password");
        var confirmPasswordIcon = $('.i-show-profile-confirmPassword');

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

        /**** CURRENT PASSWORD FIELD ****/
        /* Show eye icon */
        currentPasswordInput.keydown(function () {
            currentPassowrdIcon.show();
            currentPassowrdIcon.css({
                'cursor': 'pointer',
                'top' : 51,
                'right': 55,
                'position': 'absolute',
                'color': '#AAAAAA'
            });
        });

        /* Hide eye icon when user deletes text with the keyboard */
        var toggleClassesCurrentPassword = function () {
            if (currentPasswordInput.val() == '') {
                currentPassowrdIcon.hide();
            }
        };
        currentPasswordInput.on('keyup keydown keypress change paste', function () {
            toggleClassesCurrentPassword(); // Still toggles the classes on any of the above events
        });
        toggleClassesCurrentPassword(); // and also on document ready


        /* Check if it is a mobile device */
        if (isMobile.any()) {

            /* Check if it is Internet Explorer - Trident and rv:11 belongs to IE 11 */
            if ((navigator.userAgent.match(/msie/i)) || (navigator.userAgent.match(/Trident/)
                && navigator.userAgent.match(/rv:11/))) {

                /* Drop */
                currentPassowrdIcon.on('touchend click', function (e) {
                    e.stopPropagation();
                    e.preventDefault();
                    currentPasswordInput.attr('type', 'password');
                });

                /* Hold */
                currentPassowrdIcon.on('touchstart click', function (e) {
                    e.stopPropagation();
                    e.preventDefault();
                    currentPasswordInput.attr('type', 'field');
                });

            } else {

                /* Drop */
                currentPassowrdIcon.on('touchend click', function (e) {
                    e.stopPropagation();
                    e.preventDefault();
                    currentPasswordInput.prop('type', 'password');
                });

                /* Hold */
                currentPassowrdIcon.on('touchstart click', function (e) {
                    e.stopPropagation();
                    e.preventDefault();
                    currentPasswordInput.prop('type', 'field');
                });
            }
        } else {

            /* Check if it is Internet Explorer - Trident and rv:11 belongs to IE 11 */
            if ((navigator.userAgent.match(/msie/i)) || (navigator.userAgent.match(/Trident/)
                && navigator.userAgent.match(/rv:11/))) {

                /* Drop */
                currentPassowrdIcon.mouseup(function () {
                    currentPasswordInput.attr('type', 'password');
                });

                /* Hold */
                currentPassowrdIcon.mousedown(function () {
                    currentPasswordInput.attr('type', 'field');
                });

            } else {

                /* Drop */
                currentPassowrdIcon.mouseup(function () {
                    currentPasswordInput.prop('type', 'password');
                });

                /* Hold */
                currentPassowrdIcon.mousedown(function () {
                    currentPasswordInput.prop('type', 'field');
                });
            }
        }

        /**** PASSWORD FIELD ****/
        /* Show eye icon */
        passwordInput.keydown(function () {
            passwordIcon.show();
            passwordIcon.css({
                'cursor': 'pointer',
                'top' : 51,
                'right': 55,
                'position': 'absolute',
                'color': '#AAAAAA'
            });
        });

        /* Hide eye icon when user deletes text with the keyboard */
        var toggleClassesPassword = function () {
            if (passwordInput.val() == '') {
                passwordIcon.hide();
            }
        };
        passwordInput.on('keyup keydown keypress change paste', function () {
            toggleClassesPassword(); // Still toggles the classes on any of the above events
        });
        toggleClassesPassword(); // and also on document ready


        /* Check if it is a mobile device */
        if (isMobile.any()) {

            /* Check if it is Internet Explorer - Trident and rv:11 belongs to IE 11 */
            if ((navigator.userAgent.match(/msie/i)) || (navigator.userAgent.match(/Trident/)
                && navigator.userAgent.match(/rv:11/))) {

                /* Drop */
                passwordIcon.on('touchend click', function (e) {
                    e.stopPropagation();
                    e.preventDefault();
                    passwordInput.attr('type', 'password');
                });

                /* Hold */
                passwordIcon.on('touchstart click', function (e) {
                    e.stopPropagation();
                    e.preventDefault();
                    passwordInput.attr('type', 'field');
                });

            } else {

                /* Drop */
                passwordIcon.on('touchend click', function (e) {
                    e.stopPropagation();
                    e.preventDefault();
                    passwordInput.prop('type', 'password');
                });

                /* Hold */
                passwordIcon.on('touchstart click', function (e) {
                    e.stopPropagation();
                    e.preventDefault();
                    passwordInput.prop('type', 'field');
                });
            }
        } else {

            /* Check if it is Internet Explorer - Trident and rv:11 belongs to IE 11 */
            if ((navigator.userAgent.match(/msie/i)) || (navigator.userAgent.match(/Trident/)
                && navigator.userAgent.match(/rv:11/))) {

                /* Drop */
                passwordIcon.mouseup(function () {
                    passwordInput.attr('type', 'password');
                });

                /* Hold */
                passwordIcon.mousedown(function () {
                    passwordInput.attr('type', 'field');
                });

            } else {

                /* Drop */
                passwordIcon.mouseup(function () {
                    passwordInput.prop('type', 'password');
                });

                /* Hold */
                passwordIcon.mousedown(function () {
                    passwordInput.prop('type', 'field');
                });
            }
        }

        /**** CONFIRM PASSWORD FIELD ****/
        /* Show eye icon */
        confirmPasswordInput.keydown(function () {
            confirmPasswordIcon.show();
            confirmPasswordIcon.css({
                'cursor': 'pointer',
                'top' : 51,
                'right': 55,
                'position': 'absolute',
                'color': '#AAAAAA'
            });
        });

        /* Hide eye icon when user deletes text with the keyboard */
        var toggleClassesConfirmPassword = function () {
            if (confirmPasswordInput.val() == '') {
                confirmPasswordIcon.hide();
            }
        };
        confirmPasswordInput.on('keyup keydown keypress change paste', function () {
            toggleClassesConfirmPassword(); // Still toggles the classes on any of the above events
        });
        toggleClassesConfirmPassword(); // and also on document ready


        /* Check if it is a mobile device */
        if (isMobile.any()) {

            /* Check if it is Internet Explorer - Trident and rv:11 belongs to IE 11 */
            if ((navigator.userAgent.match(/msie/i)) || (navigator.userAgent.match(/Trident/)
                && navigator.userAgent.match(/rv:11/))) {

                /* Drop */
                confirmPasswordIcon.on('touchend click', function (e) {
                    e.stopPropagation();
                    e.preventDefault();
                    confirmPasswordInput.attr('type', 'password');
                });

                /* Hold */
                confirmPasswordIcon.on('touchstart click', function (e) {
                    e.stopPropagation();
                    e.preventDefault();
                    confirmPasswordInput.attr('type', 'field');
                });

            } else {

                /* Drop */
                confirmPasswordIcon.on('touchend click', function (e) {
                    e.stopPropagation();
                    e.preventDefault();
                    confirmPasswordInput.prop('type', 'password');
                });

                /* Hold */
                confirmPasswordIcon.on('touchstart click', function (e) {
                    e.stopPropagation();
                    e.preventDefault();
                    confirmPasswordInput.prop('type', 'field');
                });
            }
        } else {

            /* Check if it is Internet Explorer - Trident and rv:11 belongs to IE 11 */
            if ((navigator.userAgent.match(/msie/i)) || (navigator.userAgent.match(/Trident/)
                && navigator.userAgent.match(/rv:11/))) {

                /* Drop */
                confirmPasswordIcon.mouseup(function () {
                    confirmPasswordInput.attr('type', 'password');
                });

                /* Hold */
                confirmPasswordIcon.mousedown(function () {
                    confirmPasswordInput.attr('type', 'field');
                });

            } else {

                /* Drop */
                confirmPasswordIcon.mouseup(function () {
                    confirmPasswordInput.prop('type', 'password');
                });

                /* Hold */
                confirmPasswordIcon.mousedown(function () {
                    confirmPasswordInput.prop('type', 'field');
                });
            }
        }
    };

    /**
     * It handles the max length of the fields
     */
    var handlerMaxlengthPassword = function() {

        /* Current password field */
        $('#currentPassword').maxlength({
            limitReachedClass: "label label-danger",
            threshold: 10,
            placement: 'top',
            validate: true
        });

        /* New password field */
        $('#password').maxlength({
            limitReachedClass: "label label-danger",
            threshold: 10,
            placement: 'top',
            validate: true
        });

        /* Confirm password field */
        $('#confirmPassword').maxlength({
            limitReachedClass: "label label-danger",
            threshold: 10,
            placement: 'top',
            validate: true
        });
    };

    return {
        // Main function to initiate the module
        init: function () {
            handlerPasswordProfileValidation();
            handlerIconUserProfile();
            handlerMaxlengthPassword()
        }
    };

}();

jQuery(document).ready(function() {
    DomainPasswordProfileValidation.init();
});