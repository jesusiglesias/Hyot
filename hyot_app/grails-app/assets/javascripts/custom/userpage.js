/*-------------------------------------------------------------------------------------------*
 *                               CUSTOM JAVASCRIPT - USER PAGE                               *
 *-------------------------------------------------------------------------------------------*/

var CustomUserPageScript = function () {

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
     * It reload the content from AJAX call
     */
    var handlerAJAXCallDashboard = function () {

        // Call AJAX to upload the number of measurements of the user
        $('.reloadMymeasurement').click(function () {

            var counterMymeasurement = $('.counterMymeasurement');
            var widgetMymeasurement = $('.widget-mymeasurement');

            $.ajax({
                url: reloadMymeasurementURL,
                beforeSend: function () {

                    widgetMymeasurement.LoadingOverlay("show", {
                        image: "",
                        fontawesome: "fa fa-spinner fa-spin"
                    });
                },
                success: function (data) {
                    counterMymeasurement.attr('data-value', data);
                    counterMymeasurement.text(data);

                    counterMymeasurement.counterUp({});
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
                        widgetMymeasurement.LoadingOverlay("hide");
                    }, 500);
                }
            });
        });

        // Call AJAX to upload the number of alerts of the user in the Blockchain
        $('.reloadMyalert').click(function () {

            var counterMyalert = $('.counterMyalert');
            var widgetMyalert = $('.widget-myalert');

            $.ajax({
                url: reloadMyalertURL,
                beforeSend: function () {

                    widgetMyalert.LoadingOverlay("show", {
                        image: "",
                        fontawesome: "fa fa-spinner fa-spin"
                    });
                },
                success: function (data) {
                    counterMyalert.attr('data-value', data);
                    counterMyalert.text(data);

                    counterMyalert.counterUp({});
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
                        widgetMyalert.LoadingOverlay("hide");
                    }, 500);
                }
            });
        });
    };

return {
    // Main function to initiate the module
    init: function () {
        handlerTooltip();
        handlerAJAXCallDashboard();
    }
};
}();

jQuery(document).ready(function () {
    CustomUserPageScript.init();
});
