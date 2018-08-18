/*-------------------------------------------------------------------------------------------*
 *                                     DATATABLE JAVASCRIPT                                  *
 *-------------------------------------------------------------------------------------------*/

var DatatableAdminList = function () {

    /**
     *  Table function
     */
    var initAdminTable = function () {

        var table = $('#entity-table');

        var oTable = table.dataTable({

            // Internationalisation
            "language": {
                "aria": {
                    "sortAscending": _sortAscending,
                    "sortDescending": _sortDescending
                },
                "emptyTable": _emptyTable,
                "info": _info,
                "infoEmpty": _infoEmpty,
                "infoFiltered": _infoFiltered,
                "lengthMenu": _lengthMenu,
                "search": _search,
                "zeroRecords": _zeroRecords,
                "processing": _processing,
                "infoThousands": _infoThousands,
                "loadingRecords": _loadingRecords,
                "paginate": {
                    "first": _first,
                    "last": _last,
                    "next": _next,
                    "previous": _previous
                }
            },

            // Row selectable
            select: false,

            // Disable fixed width and enable fluid table
            "autoWidth": true,

            // Visibility of columns
            "columnDefs": [
                {
                    "targets": [5], // Account expired
                    "visible": false
                },
                {
                    "targets": [6], // Password expired
                    "visible": false
                }
            ],

            buttons: [
                { extend: 'print', className: 'btn dark btn-outline transparent hvr-bounce-to-top-print', text: _print, exportOptions: {columns: [1, 2, 3, 4, 5, 6]} },
                { extend: 'copy', className: 'btn red-sunglo btn-outline transparent hvr-bounce-to-top-copy', text: _copy, exportOptions: {columns: [1, 2, 3, 4, 5, 6]} },
                { extend: 'pdf', className: 'btn green-dark btn-outline transparent hvr-bounce-to-top-pdf', text: _pdf, filename: _adminFile, title: _adminTableTitle, exportOptions: {columns: [1, 2, 3, 4, 5, 6]} },
                { extend: 'csv', className: 'btn blue-steel btn-outline transparent hvr-bounce-to-top-csv', text: _csv, fieldSeparator: ';', filename: _adminFile, exportOptions: {columns: [1, 2, 3, 4, 5, 6]} },
                { extend: 'colvis', className: 'btn yellow-casablanca btn-outline transparent hvr-bounce-to-top-colvis', text: _columns },
                { extend: 'colvisRestore', className: 'btn yellow btn-outline transparent hvr-bounce-to-top-colvisRestore', text: _restore }
            ],

            // Pagination type
            "pagingType": "bootstrap_full_number",

            // Setup responsive extension
            responsive: true,

            // Disable column ordering
            //"ordering": false,

            // Disable pagination
            //"paging": false,

            // Save the state of search form
            //"bStateSave" : true,

            colReorder: {
                reorderCallback: function () {
                }
            },

            "order": [
                [1, 'asc']
            ],
            
            "lengthMenu": [
                [5, 10, 20, 50, 100, -1],
                [5, 10, 20, 50, 100, _all] // Change per page values here
            ],

            // Set the initial value
            "pageLength": 20,

            // Horizontal scrollable datatable
            "dom": "<'row' <'col-md-12'B>><'row'<'col-sm-6 col-xs-12'l><'col-sm-6 col-xs-12'f>r><'table-scrollable't><'row'<'col-sm-5 col-xs-12'i><'col-sm-7 col-xs-12'p>>"
        });
    };

    return {

        // Main function to initiate the script
        init: function () {

            if (!jQuery().dataTable) {
                return;
            }
            initAdminTable();
        }

    };

}();

jQuery(document).ready(function() {
    DatatableAdminList.init();
});