/*-------------------------------------------------------------------------------------------*
 *                            CUSTOM JAVASCRIPT - STRENGTH PASSWORD                          *
 *-------------------------------------------------------------------------------------------*/

var CustomPassword = function () {

    /**
     * Handler password strength
     */
    var handlePasswordStrengthChecker = function() {

        var initialized = false;
        var inputPassword = $("#password");

        inputPassword.keydown(function () {
            if (initialized === false) {

                // Set base options
                inputPassword.pwstrength({
                    raisePower: 1.4,
                    minChar: 8,
                    scores: [17, 26, 40, 50, 60],
                    ui: {
                        verdicts: [_weak, _normal, _medium, _strong, _veryStrong],
                        container: "#container-password",
                        viewports: {
                            progress: ".pwstrength-viewport-progress",
                            verdict: ".pwstrength-viewport-verdict"
                        }
                    },
                    rules: {
                        activated: {
                            wordTwoCharacterClasses: true,
                            wordRepetitions: true
                        }
                    }
                });

                // Add your own rule to calculate the password strength
                inputPassword.pwstrength("addRule", "demoRule", function (options, word, score) {
                    return word.match("^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=\\S+\$).{8,}\$") && score;
                }, 10, true);

                // Set as initialized
                initialized = true;
            }
        });
    };

    return {
        // Main function to initiate the module
        init: function () {
            handlePasswordStrengthChecker();
        }
    };
}();

jQuery(document).ready(function() {
    CustomPassword.init();
});
