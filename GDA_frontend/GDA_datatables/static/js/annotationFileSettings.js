$(document).ready(function() {
    $('#phoneNumber').click(function (){
        navigator.clipboard.writeText("0038162216560");
        $('#phoneNumber').attr('data-tooltip', 'Copied phone number!');
        $('#phoneNumber').addClass("simptip-position-top").addClass("simptip-smooth").addClass("simptip-fade");
        setTimeout(function(){
            $('#phoneNumber').removeClass("simptip-position-top").removeClass("simptip-smooth").removeClass("simptip-fade");
            $('#phoneNumber').attr('data-tooltip', '');
        }, 1500);

        return false;
    });

    $('.social-tooltip').click(function (){
        $('.social-tooltip').removeClass("simptip-position-top").removeClass("simptip-smooth").removeClass("simptip-fade");
        $('.social-tooltip').attr('data-tooltip', '');
    });

    let githubElement = $('#github');
    githubElement.hover(function (){
        githubElement.attr('data-tooltip', 'Github');
        githubElement.addClass("simptip-position-top").addClass("simptip-smooth").addClass("simptip-fade");
    }, function (){
        githubElement.removeClass("simptip-position-top").removeClass("simptip-smooth").removeClass("simptip-fade");
        githubElement.attr('data-tooltip', '');
    });

    let linkedinElement = $('#linkedin');
    linkedinElement.hover(function (){
        linkedinElement.attr('data-tooltip', 'Linkedin');
        linkedinElement.addClass("simptip-position-top").addClass("simptip-smooth").addClass("simptip-fade");
    }, function (){
        linkedinElement.removeClass("simptip-position-top").removeClass("simptip-smooth").removeClass("simptip-fade");
        linkedinElement.attr('data-tooltip', '');
    });

    let phoneNumberElement = $('#phoneNumber');
    phoneNumberElement.hover(function (){
        phoneNumberElement.attr('data-tooltip', 'Copy phone number!');
        phoneNumberElement.addClass("simptip-position-top").addClass("simptip-smooth").addClass("simptip-fade");
    }, function (){
        phoneNumberElement.removeClass("simptip-position-top").removeClass("simptip-smooth").removeClass("simptip-fade");
        phoneNumberElement.attr('data-tooltip', '');
    });

    let websiteElement = $('#website');
    websiteElement.hover(function (){
        websiteElement.attr('data-tooltip', 'Personal Website');
        websiteElement.addClass("simptip-position-top").addClass("simptip-smooth").addClass("simptip-fade");
    }, function (){
        websiteElement.removeClass("simptip-position-top").removeClass("simptip-smooth").removeClass("simptip-fade");
        websiteElement.attr('data-tooltip', '');
    });

    $('#annotationTable').dataTable({
        language: DT_LANGUAGE,
        order: [[ 0, "desc" ]],
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
                data: 'jaccardIndex',
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
                    }, 'csv', 'excel', 'pdf'
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
});