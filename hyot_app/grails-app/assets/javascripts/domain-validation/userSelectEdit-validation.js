/*-------------------------------------------------------------------------------------------*
 *                                 USER VALIDATION JAVASCRIPT                                *
 *-------------------------------------------------------------------------------------------*/

var DomainUserValidation = function () {

    /**
     * User validation
     */
    var handlerUserValidation = function() {

        var userForm = $('.user-form');

        jQuery.validator.addMethod("notEqualToUsername", function(value, element, param) {
            return this.optional(element) || value.toLowerCase() != $(param).val().toLowerCase();
        }, _equalPasswordUsername);

        userForm.validate({
                errorElement: 'span', // Default input error message container
                errorClass: 'help-block help-block-error', // Default input error message class
                focusInvalid: false, // Do not focus the last invalid input
                ignore: "",  // Validate all fields including form hidden input
                rules: {
                    username: {
                        required: true,
                        maxlength: 30
                    },
                    email: {
                        required: true,
                        email: true,
                        maxlength: 60
                    },
                    password: {
                        required: true,
                        minlength: 8,
                        maxlength: 32,
                        notEqualToUsername:'#username'
                    },
                    confirmPassword: {
                        required: true,
                        minlength: 8,
                        maxlength: 32,
                        equalTo: "#password"
                    },
                    name: {
                        required: true,
                        maxlength: 25
                    },
                    surname: {
                        required: true,
                        maxlength: 40
                    }
                },

                messages: {
                    username: {
                        required: _requiredField,
                        maxlength: _maxlengthField
                    },
                    email: {
                        required: _requiredField,
                        email: _emailField,
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
                    },
                    name: {
                        required: _requiredField,
                        maxlength: _maxlengthField
                    },
                    surname: {
                        required: _requiredField,
                        maxlength: _maxlengthField
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
     * It checks the username availability
     */
    var handleUsernameAvailabilityChecker = function () {

        var username = $('#username');
        var usernameBlock = $('.username-block');

        $("#username-checker").click(function (e) {

            // Empty username
            if (username.val() === "") {
                username.closest('.form-group').removeClass('has-success').addClass('has-error');

                usernameBlock.html(_checkerUsernameBlockInfo);
                usernameBlock.addClass('availibility-error');
                return;
            }

            var btn = $(this);

            btn.attr('disabled', true);

            username.attr("readonly", true).
            attr("disabled", true).
            addClass("spinner");

            $.post(_checkUsernameAvailibilityAndBlockchain, {

                // Username value
                username: username.val()

            }, function (res) {
                btn.attr('disabled', false);

                username.attr("readonly", false).
                attr("disabled", false).
                removeClass("spinner");

                if (res.status == 'OK') {
                    username.closest('.form-group').removeClass('has-error').addClass('has-success');

                    usernameBlock.html(res.message);
                    usernameBlock.removeClass('availibility-error');
                    usernameBlock.addClass('availibility-success');

                } else {
                    username.closest('.form-group').removeClass('has-success').addClass('has-error');

                    usernameBlock.html(res.message);
                    usernameBlock.addClass('availibility-error');
                }
            }, 'json');

        });
    };

    /**
     * It checks the email availability
     */
    var handleEmailAvailabilityChecker = function () {

        var email = $('#email');
        var emailBlock = $('.email-block');

        $("#email-checker").click(function (e) {

            // Empty email
            if (email.val() === "") {
                email.closest('.form-group').removeClass('has-success').addClass('has-error');

                emailBlock.html(_checkerEmailBlockInfo);
                emailBlock.addClass('availibility-error');
                return;
            }

            var btn = $(this);

            btn.attr('disabled', true);

            email.attr("readonly", true).
            attr("disabled", true).
            addClass("spinner");

            $.post(_checkEmailAvailibility, {

                // Email value
                email: email.val()

            }, function (res) {
                btn.attr('disabled', false);

                email.attr("readonly", false).
                attr("disabled", false).
                removeClass("spinner");

                if (res.status == 'OK') {
                    email.closest('.form-group').removeClass('has-error').addClass('has-success');

                    emailBlock.html(res.message);
                    emailBlock.removeClass('availibility-error');
                    emailBlock.addClass('availibility-success');

                } else {
                    email.closest('.form-group').removeClass('has-success').addClass('has-error');

                    emailBlock.html(res.message);
                    emailBlock.addClass('availibility-error');
                }
            }, 'json');

        });
    };

    /**
     * It handles the max length of the fields
     */
    var handlerMaxlength = function() {

        /* Username field */
        $('#username').maxlength({
            limitReachedClass: "label label-danger",
            threshold: 10,
            placement: 'top',
            validate: true
        });

        /* Email field */
        $('#email').maxlength({
            limitReachedClass: "label label-danger",
            threshold: 20,
            placement: 'top',
            validate: true
        });

        /* Password field */
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

        /* Name field */
        $('#name').maxlength({
            limitReachedClass: "label label-danger",
            threshold: 8,
            placement: 'top',
            validate: true
        });

        /* Surname field */
        $('#surname').maxlength({
            limitReachedClass: "label label-danger",
            threshold: 15,
            placement: 'top',
            validate: true
        });
    };

    return {
        // Main function to initiate the module
        init: function () {
            handlerUserValidation();
            handleUsernameAvailabilityChecker();
            handleEmailAvailabilityChecker();
            handlerMaxlength();
        }
    };

}();

jQuery(document).ready(function() {
    DomainUserValidation.init();
});