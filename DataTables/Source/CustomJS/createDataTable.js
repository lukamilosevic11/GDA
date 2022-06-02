/*
 * GDA Copyright (c) 2022.
 * University of Belgrade, Faculty of Mathematics
 * Luka Milosevic
 * lukamilosevic11@gmail.com
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 */

$(document).ready(function () {
    $('#annotation').DataTable({
        responsive: true,
        dom: 'Bfrtip'
        // lengthMenu: [
        //     [10, 25, 50, 100, -1],
        //     ['10 rows', '25 rows', '50 rows', '100 rows', 'Show all']
        // ],
        // buttons: [
        //     'pageLength',
        //     'copy',
        //     'csv',
        //     'excel',
        //     'pdf',
        //     {
        //         extend: 'print',
        //         text: 'Print selected',
        //
        //     },
        //     'selectAll',
        //     'selectNone'
        //
        // ],
        // language: {
            // buttons: {
                // selectAll: "Select all items",
                // selectNone: "Select none"
            // }
        // },
        // select: true,
        // scrollX: true
    });
});

