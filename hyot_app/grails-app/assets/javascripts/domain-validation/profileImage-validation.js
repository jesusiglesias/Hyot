/*-------------------------------------------------------------------------------------------*
 *                             PROFILE IMAGE VALIDATION JAVASCRIPT                           *
 *-------------------------------------------------------------------------------------------*/

var DomainProfileImageValidation = function () {

    /**
     * Profile image validation
     */
    var handlerProfileImageValidation = function() {

        var profileImageForm = $('.profileImage-form');

        profileImageForm.validate({
                errorElement: 'span', // Default input error message container
                errorClass: 'help-block help-block-error', // Default input error message class
                focusInvalid: false, // Do not focus the last invalid input
                ignore: "",  // Validate all fields including form hidden input
                rules: {
                    avatar: {
                        required: true
                    }
                },

                messages: {
                    avatar: {
                        required: _requiredField
                    }
                },

                // Render error placement for each input type
                errorPlacement: function (error, element) {
                },

                // Set error class to the control group
                highlight: function (element) {
                    $(element)
                        .closest('.form-group').removeClass("has-success").addClass('has-error');
                },

                // Set success class to the control group
                success: function (label, element) {
                    $(element).closest('.form-group').removeClass('has-error').addClass('has-success');
                },

                submitHandler: function (form) {
                    form.submit(); // Submit the form
                }
            });
    };

    return {
        // Main function to initiate the module
        init: function () {
            handlerProfileImageValidation();
        }
    };

}();

jQuery(document).ready(function() {
    DomainProfileImageValidation.init();
});