$(document).ready(function () {
    $('.ui.dropdown').dropdown();

    function ProcessTooltip(element, name) {
        element.hover(function () {
            element.attr('data-tooltip', name);
            element.addClass("simptip-position-top").addClass("simptip-smooth").addClass("simptip-fade");
        }, function () {
            element.removeClass("simptip-position-top").removeClass("simptip-smooth").removeClass("simptip-fade");
            element.attr('data-tooltip', '');
        });
    }

    $('#phoneNumber').click(function () {
        navigator.clipboard.writeText("0038162216560").then();
        let phoneNumberElement = $('#phoneNumber');
        phoneNumberElement.attr('data-tooltip', 'Copied phone number!');
        phoneNumberElement.addClass("simptip-position-top").addClass("simptip-smooth").addClass("simptip-fade");

        return false;
    });

    $('.social-tooltip').click(function () {
        let socialElement = $('.social-tooltip');
        socialElement.removeClass("simptip-position-top").removeClass("simptip-smooth").removeClass("simptip-fade");
        socialElement.attr('data-tooltip', '');
    });

    ProcessTooltip($("#github"), "Github");
    ProcessTooltip($("#linkedin"), "Linkedin");
    ProcessTooltip($("#phoneNumber"), "Copy phone number!")
    ProcessTooltip($("#website"), "Personal Website")

    $.fn.DataTable.ext.pager.numbers_length = 5; //paging numbers

    // Initialization of datatable
    let table = $('#annotationTable').DataTable({
        language: DT_LANGUAGE,
        order: [[0, "desc"]],
        lengthMenu: [[10, 25, 50, 100], [10, 25, 50, 100]],
        columnDefs: [
            {
                orderable: true,
                searchable: true,
                targets: [0, 1, 2, 3, 4, 5, 6, 7]
            },
            {
                data: 'symbol',
                targets: [0]
            },
            {
                data: 'entrezID',
                targets: [1]
            },
            {
                data: 'uniprotID',
                targets: [2]
            },
            {
                data: 'ensemblID',
                targets: [3]
            },
            {
                data: 'doid',
                targets: [4]
            },
            {
                data: 'source',
                targets: [5]
            },
            {
                data: 'diseaseName',
                targets: [6]
            },
            {
                data: 'doidSource',
                targets: [7]
            }
        ],
        dom: '<"ui grid pb-3" <"eight wide column" B> <"four wide column ml-0 pl-0 pt-0 mt-0" r>  <"four wide column">' +
            '<"four wide column ml-0 pl-0" l> <"eight wide column"> <"four wide column " f>>t' +
            '<"ui grid stackable pt-3" <"sixteen wide column" i>>' +
            '<"container pt-1 text-center bottomGrid" <"inline-block-child" p> <"inline-block-child pageNumber">>',
        buttons:
            [
                'colvis',
                {
                    extend: 'collection',
                    text: 'Extract data',
                    buttons: [
                        {
                            extend: 'csvHtml5',
                            filename: 'GDA_annotation_file'
                        },
                        {
                            extend: 'excelHtml5',
                            filename: 'GDA_annotation_file',
                            title: 'GDA Annotation File'
                        },
                        {
                            extend: 'pdfHtml5',
                            filename: 'GDA_annotation_file',
                            title: 'GDA Annotation File'
                        },
                        {
                            extend: 'print',
                            title: 'GDA Annotation File'
                        }
                    ]
                },
                {
                    extend: 'copyHtml5',
                    text: 'Copy',
                    key: {
                        key: 'c',
                        altKey: true
                    }
                },
                'selectAll',
                'selectNone'
            ],
        searching: true,
        processing: true,
        serverSide: true,
        stateSave: true,
        responsive: true,
        select: true,
        ajax: ANNOTATION_LIST_JSON_URL
    });

    $(".pageNumber").append(
        '<div class="ui icon input small" style="width: 130px; margin-left: 10px;">' +
        '   <input id="pageNumber" type="number" min="1" placeholder="Page number">' +
        '   <i class="list ol large icon"></i>' +
        '</div>'
    );


    let pageNumber = $('#pageNumber');

    function ChangePage(refreshEmpty = false) {
        let p = pageNumber.val();
        if (p) {
            p = parseInt(p);
            let numberOfPages = table.page.info().pages;
            if (p && p >= 0 && p <= numberOfPages) {
                table.page(p - 1).draw('page');
            }
        } else if (refreshEmpty) {
            let pageNum = table.page();
            table.draw();
            table.page(pageNum).draw('page');
        }
    }

    pageNumber.on('change keydown paste input propertychange click keyup blur', function () {
        ChangePage();
    });

    let inputElements = $(".input-search");
    inputElements.on("keyup", "input", function () {
        table.column($(this)[0].id).search(this.value).draw();
    });
    inputElements.click(function (event) {
        event.stopPropagation();
    });

    document.querySelectorAll('.input-search').forEach(item => {
        item.addEventListener('search', event => {
            table.column(event.target.id).search(event.target.value).draw();
        });
    });

    table.columns().every(function () {
        let inputElem = $('#' + this.index());

        let state = this.state.loaded();
        if (state) {
            let val = state.columns[this.index()];
            inputElem.val(val.search.search);
        }
    });

    function ResizeTable(size) {
        let tableSizing = $("#annotationTable");
        let small = $('#size-small');
        let normal = $('#size-normal');
        let large = $('#size-large');
        let text = $('#table-size-text');

        if (size === "small") {
            localStorage.setItem("table-size", "small");
            tableSizing.removeClass("large");
            small.addClass("active selected");
            normal.removeClass("active selected");
            large.removeClass("active selected");
            text.text("Small");
            tableSizing.addClass("small");
        } else if (size === "") {
            localStorage.setItem("table-size", "");
            tableSizing.removeClass("large");
            tableSizing.removeClass("small");
            small.removeClass("active selected");
            normal.addClass("active selected");
            text.text("Normal");
            large.removeClass("active selected");
        } else if (size === "large") {
            localStorage.setItem("table-size", "large");
            tableSizing.removeClass("small");
            small.removeClass("active selected");
            normal.removeClass("active selected");
            large.addClass("active selected");
            text.text("Large");
            tableSizing.addClass("large");
        }
        ChangePage(true);
    }

    $('.table-size').click(function (element) {
        if ($('#size-small')[0].className.includes("selected")) {
            ResizeTable("small");
        } else if ($('#size-normal')[0].className.includes("selected")) {
            ResizeTable("");
        } else if ($('#size-large')[0].className.includes("selected")) {
            ResizeTable("large");
        }
    });

    let currentSize = localStorage.getItem('table-size');
    if (currentSize !== null) {
        ResizeTable(currentSize);

    } else {
        localStorage.setItem('table-size', 'small');
    }
});