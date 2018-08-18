/*-------------------------------------------------------------------------------------------*
 *                                     DATATABLE JAVASCRIPT                                  *
 *-------------------------------------------------------------------------------------------*/

var DatatableUserList = function () {

    /**
     *  Table function
     */
    var initUserTable = function () {

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

            // Auto width
            "autoWidth": true,

            // Visibility of columns
            "columnDefs": [
                {
                    "targets": [5], // Expired account
                    "visible": false
                },
                {
                    "targets": [6], // Expired password
                    "visible": false
                },
            ],

            buttons: [
                { extend: 'print', className: 'btn dark btn-outline transparent hvr-bounce-to-top-print', text: _print, exportOptions: {columns: [0, 1, 2, 3, 4, 5, 6, 7, 8]} },
                { extend: 'copy', className: 'btn red-sunglo btn-outline transparent hvr-bounce-to-top-copy', text: _copy, exportOptions: {columns: [0, 1, 2, 3, 4, 5, 6, 7, 8]} },
                { extend: 'pdf', className: 'btn green-dark btn-outline transparent hvr-bounce-to-top-pdf', text: _pdf, filename: _userFile, title: _userTableTitle, exportOptions: {columns: [0, 1, 2, 3, 4, 5, 6, 7, 8]} },
                { extend: 'csv', className: 'btn blue-steel btn-outline transparent hvr-bounce-to-top-csv', text: _csv, fieldSeparator: ';', filename: _userFile, exportOptions: {columns: [0, 1, 2, 3, 4, 5, 6, 7, 8]} },
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

        // Search of users
        var searchTable = table.DataTable();
        searchTable.search(_textSearch).draw();

    };

    return {

        // Main function to initiate the script
        init: function () {

            if (!jQuery().dataTable) {
                return;
            }
            initUserTable();
        }

    };

}();

jQuery(document).ready(function() {
    DatatableUserList.init();
});