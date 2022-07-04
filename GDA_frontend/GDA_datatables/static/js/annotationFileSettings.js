$(document).ready(function () {
    $('.ui.dropdown').dropdown();


    // function ProcessTooltip(element, name) {
    //     element.hover(function () {
    //         element.attr('data-tooltip', name);
    //         element.addClass("simptip-position-top").addClass("simptip-smooth").addClass("simptip-fade");
    //     }, function () {
    //         element.removeClass("simptip-position-top").removeClass("simptip-smooth").removeClass("simptip-fade");
    //         element.attr('data-tooltip', '');
    //     });
    // }
    //
    // $('#phoneNumber').click(function () {
    //     navigator.clipboard.writeText("0038162216560").then();
    //     let phoneNumberElement = $('#phoneNumber');
    //     phoneNumberElement.attr('data-tooltip', 'Copied phone number!');
    //     phoneNumberElement.addClass("simptip-position-top").addClass("simptip-smooth").addClass("simptip-fade");
    //     setTimeout(function () {
    //         phoneNumberElement.removeClass("simptip-position-top").removeClass("simptip-smooth").removeClass("simptip-fade");
    //         phoneNumberElement.attr('data-tooltip', '');
    //     }, 1500);
    //
    //     return false;
    // });
    //
    // $('.social-tooltip').click(function () {
    //     let socialElement = $('.social-tooltip');
    //     socialElement.removeClass("simptip-position-top").removeClass("simptip-smooth").removeClass("simptip-fade");
    //     socialElement.attr('data-tooltip', '');
    // });
    //
    // ProcessTooltip($("#github"), "Github");
    // ProcessTooltip($("#linkedin"), "Linkedin");
    // ProcessTooltip($("#phoneNumber"),"Copy phone number!")
    // ProcessTooltip($("#website"),"Personal Website")

    // Initialization of datatable


    let table = $('#annotationTable').DataTable({
        language: DT_LANGUAGE,
        order: [[0, "desc"]],
        lengthMenu: [[25, 50, 100], [25, 50, 100]],
        columnDefs: [
            {
                orderable: true,
                searchable: true,
                className: "center",
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
        dom: 'Blfrtip',
        buttons:
            [{
                extend: 'collection',
                text: 'Extract data',
                buttons: [
                    {
                        extend: 'copy',
                        text: 'Copy',
                        key: {
                            key: 'c',
                            altKey: true
                        }
                    }, 'colvis', 'csv', 'excel', 'pdf'
                ]
            },
                {
                    extend: 'print',
                    text: 'Print selected',
                }, 'selectAll', 'selectNone'],
        searching: true,
        processing: true,
        serverSide: true,
        stateSave: true,
        responsive: true,
        select: true,
        ajax: ANNOTATION_LIST_JSON_URL
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
        table.draw();
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
    console.log(currentSize);
    if (currentSize !== null) {
        ResizeTable(currentSize);

    } else {
        localStorage.setItem('table-size', 'small');
    }


    // *** Tooltip settings social icons ***

    // $('#phoneNumber').click(function () {
    //     navigator.clipboard.writeText("0038162216560");
    //     $('#phoneNumber').attr('data-tooltip', 'Copied phone number!');
    //     $('#phoneNumber').addClass("simptip-position-top").addClass("simptip-smooth").addClass("simptip-fade");
    //     setTimeout(function () {
    //         $('#phoneNumber').removeClass("simptip-position-top").removeClass("simptip-smooth").removeClass("simptip-fade");
    //         $('#phoneNumber').attr('data-tooltip', '');
    //     }, 1500);
    //
    //     return false;
    // });
    //
    // $('.social-tooltip').click(function () {
    //     $('.tm-social-link').removeClass("simptip-position-top").removeClass("simptip-smooth").removeClass("simptip-fade");
    //     $('.tm-social-link').attr('data-tooltip', '');
    // });
    //
    // let githubElement = $('#github');
    // githubElement.hover(function () {
    //     githubElement.attr('data-tooltip', 'Github');
    //     githubElement.addClass("simptip-position-top").addClass("simptip-smooth").addClass("simptip-fade");
    // }, function () {
    //     githubElement.removeClass("simptip-position-top").removeClass("simptip-smooth").removeClass("simptip-fade");
    //     githubElement.attr('data-tooltip', '');
    // });
    //
    // let linkedinElement = $('#linkedin');
    // linkedinElement.hover(function () {
    //     linkedinElement.attr('data-tooltip', 'Linkedin');
    //     linkedinElement.addClass("simptip-position-top").addClass("simptip-smooth").addClass("simptip-fade");
    // }, function () {
    //     linkedinElement.removeClass("simptip-position-top").removeClass("simptip-smooth").removeClass("simptip-fade");
    //     linkedinElement.attr('data-tooltip', '');
    // });
    //
    // let phoneNumberElement = $('#phoneNumber');
    // phoneNumberElement.hover(function () {
    //     phoneNumberElement.attr('data-tooltip', 'Copy phone number!');
    //     phoneNumberElement.addClass("simptip-position-top").addClass("simptip-smooth").addClass("simptip-fade");
    // }, function () {
    //     phoneNumberElement.removeClass("simptip-position-top").removeClass("simptip-smooth").removeClass("simptip-fade");
    //     phoneNumberElement.attr('data-tooltip', '');
    // });
    //
    // let websiteElement = $('#website');
    // websiteElement.hover(function () {
    //     websiteElement.attr('data-tooltip', 'Personal Website');
    //     websiteElement.addClass("simptip-position-top").addClass("simptip-smooth").addClass("simptip-fade");
    // }, function () {
    //     websiteElement.removeClass("simptip-position-top").removeClass("simptip-smooth").removeClass("simptip-fade");
    //     websiteElement.attr('data-tooltip', '');
    // });
});