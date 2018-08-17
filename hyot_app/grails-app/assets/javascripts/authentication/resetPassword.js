/*-------------------------------------------------------------------------------------------*
 *                                  RESET PASSWORD JAVASCRIPT                                *
 *-------------------------------------------------------------------------------------------*/

var Login = function() {

    /** Restore password form */
    var handleForgetPassword = function () {

        // Reset password button activates when user enter the data
        var forgetForm = $(".forget-form");
        var restoreButton = $("#restore-button");
        var emailField = $("#email");
        var refreshIcon = $('.refreshIcon');

        restoreButton.attr('disabled', 'disabled');

        forgetForm.keyup(function () {
            // Disable reset button
            restoreButton.attr('disabled', 'disabled');

            // Validating fields
            var email = emailField.val().trim();

            // Validating whitespaces
            var emailWhitespace = /\s/g.test(email);

            if (!(email === "" || emailWhitespace)) {
                // Enable reset Button
                restoreButton.removeAttr('disabled');
            }
        });

        // Form validation
        forgetForm.validate({
            errorElement: 'span', // Default input error message container
            errorClass: 'help-block', // Default input error message class
            focusInvalid: true, // Do not focus the last invalid input
            ignore: "",
            rules: {
                email: {
                    required: true,
                    email: true
                }
            },

            messages: {
                email: {
                    required: "",
                    email: _forgotPassword
                }
            },

            highlight: function (element) { // Hightlight error inputs
                $(element).closest('.form-group').addClass('has-error'); // Set error class to the control group
            },

            success: function (label) {
                label.closest('.form-group').removeClass('has-error');
                label.closest('.form-group').addClass('has-success');
                label.remove();
            },

            errorPlacement: function (error, element) {
                error.insertAfter(element.closest('.form-control'));
            },

            submitHandler: function (form) {
                restoreButton.attr('disabled', true);
                restoreButton.find('span').text(_sending);
                refreshIcon.removeClass('refresh-icon-stop');
                refreshIcon.addClass('refresh-icon');

                form.submit(); // Submit the form
            }
        });

        $('.forget-form input').keypress(function (e) {

            if (e.which === 13) {
                if (forgetForm.validate().form()) {

                    restoreButton.attr('disabled', true);
                    restoreButton.find('span').text(_sending);
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
        var restoreButton = $('#restore-button');

        function handleOrientationChange(mediaquery) {
            if (mediaquery.matches) {

                backButton.addClass('btn-block');
                restoreButton.addClass('btn-block');
                restoreButton.addClass('space-button-restore-new-size');
            } else {
                backButton.removeClass('btn-block');
                restoreButton.removeClass('btn-block');
                restoreButton.removeClass('space-button-restore-new-size');
            }
        }

        handleOrientationChange(mediaquery);
        mediaquery.addListener(handleOrientationChange);
    };

    return {
        // Main function to initiate the module
        init: function() {
            handleForgetPassword();
            handleSizeButtons();
        }
    };
}();

// Init login functions when page is loaded
jQuery(document).ready(function() {
    Login.init();
});