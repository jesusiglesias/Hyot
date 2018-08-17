/*-------------------------------------------------------------------------------------------*
 *                                    NEW PASSWORD JAVASCRIPT                                *
 *-------------------------------------------------------------------------------------------*/

var Login = function() {

    /**
     * New password form.
     */
    var handleNewPassword = function () {

        // Reset password button activates when user enter the data
        var forgetForm = $(".forget-form");
        var newPasswordButton = $("#newPassword-button");
        var passwordField = $("#password");
        var passwordConfirmField = $("#passwordConfirm");
        var formConfirmPassword = $('.form-confirmPassword');
        var refreshIcon = $('.refreshIcon');

        newPasswordButton.attr('disabled', 'disabled');

        forgetForm.keyup(function () {
            // Disable new password button
            newPasswordButton.attr('disabled', 'disabled');

            // Validating fields
            var password = passwordField.val().trim();
            var passwordConfirm = passwordConfirmField.val().trim();

            // Validating whitespaces
            var passwordWhitespace = /\s/g.test(password);
            var passwordConfirmWhitespace = /\s/g.test(passwordConfirm);

            if (!(password === "" || passwordConfirm === "" || passwordWhitespace || passwordConfirmWhitespace)) {
                // Enable new password Button
                newPasswordButton.removeAttr('disabled');
            }
        });

        // Form validation
        forgetForm.validate({
            focusInvalid: true, // Do not focus the last invalid input
            ignore: "",
            rules: {
                passwordConfirm: {
                    required: true,
                    minlength: 8,
                    maxlength: 32,
                    equalTo: "#password"
                }
            },

            messages: {
                passwordConfirm: {
                    required: _requiredField,
                    minlength: _minlengthField,
                    maxlength: _maxlengthField,
                    equalTo: _equalPassword
                }
            },

            highlight: function (element) { // Hightlight error inputs
                $(element).closest('.form-group').removeClass('has-error').addClass('has-error'); // Set error class to the control group
            },

            success: function () {
                formConfirmPassword.removeClass('has-error');
                formConfirmPassword.addClass('has-success');

                var icon = $('.i-checkPassword');
                icon.removeClass("fa-warning").addClass("fa-key");
            },

            errorPlacement: function (error) {

                var icon = $('.i-checkPassword');
                icon.removeClass('fa-key').addClass("fa-warning");
                icon.attr("data-original-title", error.text()).tooltip({'container': 'body'});
            },

            submitHandler: function (form) {
                newPasswordButton.attr('disabled', true);
                newPasswordButton.find('span').text(_confirming);
                refreshIcon.removeClass('refresh-icon-stop');
                refreshIcon.addClass('refresh-icon');

                form.submit(); // Submit the form
            }
        });

        $('.forget-form input').keypress(function (e) {

            if (e.which === 13) {
                if (forgetForm.validate().form()) {

                    newPasswordButton.attr('disabled', true);
                    newPasswordButton.find('span').text(_confirming);
                    refreshIcon.removeClass('refresh-icon-stop');
                    refreshIcon.addClass('refresh-icon');
                    
                    forgetForm.submit();
                }
                return false;
            }
        });
    };

    /**
     * It adds classes to buttons depends on size screen
     */
    var handleSizeButtons = function () {

        var mediaquery = window.matchMedia("(max-width: 480px)");

        var backButton = $('.back-button');
        var newPasswordButton = $('#newPassword-button');

        function handleOrientationChange(mediaquery) {
            if (mediaquery.matches) {

                backButton.addClass('btn-block');
                newPasswordButton.addClass('btn-block');
                newPasswordButton.addClass('space-button-restore-new-size');
            } else {
                backButton.removeClass('btn-block');
                newPasswordButton.removeClass('btn-block');
                newPasswordButton.removeClass('space-button-restore-new-size');
            }
        }

        handleOrientationChange(mediaquery);
        mediaquery.addListener(handleOrientationChange);
    };

    /**
     * It handles the max length of the fields
     */
    var handlerMaxlength = function() {

        /* Password field */
        $('#password').maxlength({
            limitReachedClass: "label label-danger",
            threshold: 10,
            placement: 'top',
            validate: true
        });

        /* Confirm password field */
        $('#passwordConfirm').maxlength({
            limitReachedClass: "label label-danger",
            threshold: 10,
            placement: 'top',
            validate: true
        });
    };

    return {
        // Main function to initiate the module
        init: function() {
            handleNewPassword();
            handleSizeButtons();
            handlerMaxlength();
        }
    };
}();

// Init login functions when page is loaded
jQuery(document).ready(function() {
    Login.init();
});