/*-------------------------------------------------------------------------------------------*
 *                            CUSTOM JAVASCRIPT - CONFIRMATION                               *
 *-------------------------------------------------------------------------------------------*/

var CustomConfirmation = function () {

    /**
     * Popup to delete an instance of a entity
     */
    var handlerPopupDelete = function () {

        $('#delete-confirm-popover').confirmation({
            onConfirm: function() {
                $('.form-delete').submit();
            }
        });
    };

    return {
        // Main function to initiate the module
        init: function () {
            handlerPopupDelete();
        }
    };
}();

jQuery(document).ready(function() {
    CustomConfirmation.init();
});
