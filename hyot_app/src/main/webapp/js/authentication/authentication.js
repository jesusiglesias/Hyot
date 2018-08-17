/*-------------------------------------------------------------------------------------------*
 *                                  AUTHENTICATION JAVASCRIPT                                *
 *-------------------------------------------------------------------------------------------*/

var Login = function() {

    /**
     * Login form.
     */
    var handleLogin = function() {

        // Login button activates when user enter the data
        var loginForm = $(".login-form");
        var loginButton =  $("#login-button");
        var usernameField = $("#username");
        var passwordField = $("#password");

        loginButton.attr('disabled', 'disabled');

        loginForm.keyup(function () {
            // Disable login button
            loginButton.attr('disabled', 'disabled');

            // Validating fields
            var username = usernameField.val().trim();
            var password = passwordField.val().trim();

            // Validating whitespaces
            var usernameWhitespace = /\s/g.test(username);
            var passwordWhitespace = /\s/g.test(password);

            if (!(username == "" || password == "" || usernameWhitespace || passwordWhitespace)) {
                    // Enable login Button
                    loginButton.removeAttr('disabled');
            }
        });
    };

    /**
     * It handles the overlay in log in action.
     */
    var handlerOverlay = function() {

        var loginButton =  $("#login-button");

        loginButton.click(function() {
            $.LoadingOverlay("show", {
                color       : "rgba(255, 255, 255, 0.2)",
                image       : "",
                fontawesome : "fa fa-spinner fa-spin"
            });
        });
    };

    return {
        // Main function to initiate the module
        init: function() {
            handleLogin();
            handlerOverlay();
        }
    };
}();

// Init login functions when page is loaded
jQuery(document).ready(function() {
    Login.init();
});