/*-------------------------------------------------------------------------------------------*
 *                               CUSTOM JAVASCRIPT - DASHBOARD                               *
 *-------------------------------------------------------------------------------------------*/

var CustomDashboardScript = function () {

    /**
     * It handles the tooltips
     */
    var handlerTooltip = function () {

        // Global tooltips
        $('.tooltips').tooltip();

        // Portlet tooltips
        $('.portlet > .portlet-title .fullscreen').tooltip({
            container: 'body',
            title: fullscreenTooltip
        });

        $('.portlet > .portlet-title > .tools > .remove').tooltip({
            container: 'body',
            title: removeTooltip
        });
        $('.portlet > .portlet-title > .tools > .collapse, .portlet > .portlet-title > .tools > .expand').tooltip({
            container: 'body',
            title: collapseTooltip
        });

        // Reload tooltips
        $('.iconReload').tooltip({
            container: 'body',
            title: reloadTooltip
        });

        // Reload tooltips
        $('.reloadGraph').tooltip({
            container: 'body',
            title: reloadTooltip
        });
    };

    /**
     * It reload the content from AJAX call in dashboards
     */
    var handlerAJAXCallDashboard = function () {

        // Call AJAX to upload the number of users
        $('.reloadNormalUser').click(function () {

            var counterUsers = $('.counterNormalUser');
            var widgetUsers = $('.widget-normaluser');

            $.ajax({
                url: reloadNormalUserURL,
                beforeSend: function () {

                    widgetUsers.LoadingOverlay("show", {
                        image: "",
                        fontawesome: "fa fa-spinner fa-spin"
                    });
                },
                success: function (data) {
                    counterUsers.attr('data-value', data);
                    counterUsers.text(data);

                    counterUsers.counterUp({});
                },
                error: function () {
                    toastr["error"](reloadAjaxError);

                    toastr.options = {
                        "closeButton": true,
                        "debug": false,
                        "newestOnTop": false,
                        "progressBar": true,
                        "positionClass": "toast-top-right",
                        "preventDuplicates": false,
                        "onclick": null,
                        "showDuration": "300",
                        "hideDuration": "1000",
                        "timeOut": "5000",
                        "extendedTimeOut": "1000",
                        "showEasing": "swing",
                        "hideEasing": "linear",
                        "showMethod": "fadeIn",
                        "hideMethod": "fadeOut"
                    }
                },
                complete: function () {
                    setTimeout(function () {
                        widgetUsers.LoadingOverlay("hide");
                    }, 500);
                }
            });
        });

        // Call AJAX to upload the number of admin users
        $('.reloadAdmin').click(function () {

            var counterAdmin = $('.counterAdmin');
            var widgetAdmin = $('.widget-admin');

            $.ajax({
                url: reloadAdminURL,
                beforeSend: function () {

                    widgetAdmin.LoadingOverlay("show", {
                        image: "",
                        fontawesome: "fa fa-spinner fa-spin"
                    });
                },
                success: function (data) {
                    counterAdmin.attr('data-value', data);
                    counterAdmin.text(data);

                    counterAdmin.counterUp({});
                },
                error: function () {
                    toastr["error"](reloadAjaxError);

                    toastr.options = {
                        "closeButton": true,
                        "debug": false,
                        "newestOnTop": false,
                        "progressBar": true,
                        "positionClass": "toast-top-right",
                        "preventDuplicates": false,
                        "onclick": null,
                        "showDuration": "300",
                        "hideDuration": "1000",
                        "timeOut": "5000",
                        "extendedTimeOut": "1000",
                        "showEasing": "swing",
                        "hideEasing": "linear",
                        "showMethod": "fadeIn",
                        "hideMethod": "fadeOut"
                    }
                },
                complete: function () {
                    setTimeout(function () {
                        widgetAdmin.LoadingOverlay("hide");
                    }, 500);
                }
            });
        });

        // Call AJAX to upload the last 10 registered users
        $('.reloadLastUsers').click(function () {

            var portletUsers = $('.portlet-users');

            // Overlay active
            portletUsers.LoadingOverlay("show", {
                image: "",
                fontawesome: "fa fa-spinner fa-spin"
            });

            // AJAX call
            $(".content-lastUsers").load("controlPanel/reloadLastUsers", function() {

                // Stop overlay
                setTimeout(function () {
                    portletUsers.LoadingOverlay("hide");
                }, 500);
            });
        });

        // Call AJAX to upload the number of alerts in the Blockchain
        $('.reloadAlert').click(function () {

            var counterAlert = $('.counterAlert');
            var widgetAlert = $('.widget-alert');

            $.ajax({
                url: reloadAlertURL,
                beforeSend: function () {

                    widgetAlert.LoadingOverlay("show", {
                        image: "",
                        fontawesome: "fa fa-spinner fa-spin"
                    });
                },
                success: function (data) {
                    counterAlert.attr('data-value', data);
                    counterAlert.text(data);

                    counterAlert.counterUp({});
                },
                error: function () {
                    toastr["error"](reloadAjaxError);

                    toastr.options = {
                        "closeButton": true,
                        "debug": false,
                        "newestOnTop": false,
                        "progressBar": true,
                        "positionClass": "toast-top-right",
                        "preventDuplicates": false,
                        "onclick": null,
                        "showDuration": "300",
                        "hideDuration": "1000",
                        "timeOut": "5000",
                        "extendedTimeOut": "1000",
                        "showEasing": "swing",
                        "hideEasing": "linear",
                        "showMethod": "fadeIn",
                        "hideMethod": "fadeOut"
                    }
                },
                complete: function () {
                    setTimeout(function () {
                        widgetAlert.LoadingOverlay("hide");
                    }, 500);
                }
            });
        });

        // Call AJAX to upload the number of users in the Blockchain
        $('.reloadUserBC').click(function () {

            var counterUserBC = $('.counterUserBC');
            var widgetUserBC = $('.widget-userBC');

            $.ajax({
                url: reloadUserBCURL,
                beforeSend: function () {

                    widgetUserBC.LoadingOverlay("show", {
                        image: "",
                        fontawesome: "fa fa-spinner fa-spin"
                    });
                },
                success: function (data) {
                    counterUserBC.attr('data-value', data);
                    counterUserBC.text(data);

                    counterUserBC.counterUp({});
                },
                error: function () {
                    toastr["error"](reloadAjaxError);

                    toastr.options = {
                        "closeButton": true,
                        "debug": false,
                        "newestOnTop": false,
                        "progressBar": true,
                        "positionClass": "toast-top-right",
                        "preventDuplicates": false,
                        "onclick": null,
                        "showDuration": "300",
                        "hideDuration": "1000",
                        "timeOut": "5000",
                        "extendedTimeOut": "1000",
                        "showEasing": "swing",
                        "hideEasing": "linear",
                        "showMethod": "fadeIn",
                        "hideMethod": "fadeOut"
                    }
                },
                complete: function () {
                    setTimeout(function () {
                        widgetUserBC.LoadingOverlay("hide");
                    }, 500);
                }
            });
        });
    };

    /**
     * It handles the select
     */
    var handlerBootstrapSelect = function () {

        $('.bs-select').selectpicker({
            iconBase: 'fa',
            tickIcon: 'fa-check'
        });
    };

return {
    // Main function to initiate the module
    init: function () {
        handlerTooltip();
        handlerAJAXCallDashboard();
        handlerBootstrapSelect();
    }
};
}();

jQuery(document).ready(function () {
    CustomDashboardScript.init();
});
