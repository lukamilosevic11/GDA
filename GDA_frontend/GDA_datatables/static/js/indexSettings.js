$(document).ready(function () {
    function Error() {
        $('#parsingFailed').show();
        setTimeout(function () {
            $('#parsingFailed').hide();
        }, 2000);
        $('#progressBar').hide();
    }

    function update() {
        let updateIntervalId = setInterval(function () {
            $.ajax({
                type: 'POST',
                url: 'update_data/',
                headers: {"X-CSRFToken": $.cookie("csrftoken")},
                success: function (resp) {
                    console.log(resp.progress);
                    $('#progressBarPercentage').width(resp.progress + '%');
                    if (!resp.parsing) {
                        location.reload();
                        clearInterval(updateIntervalId);
                    }
                }
            });
        }, 500);
    }

    if (parsing) {
        update();
    }

    $('#parseButton').click(function () {
        $("#parseButton").prop('disabled', true);
        $("#seeAnnotationFileButton").addClass("disabled");
        $("#initializeSearchEngine").prop('disabled', true);
        $("#progressBar").show();
        let initializeSearchEngine = $('#initializeSearchEngine').prop('checked');
        $.ajax({
            type: 'POST',
            url: 'initialize_parsing/',
            headers: {"X-CSRFToken": $.cookie("csrftoken")},
            error: Error
        }).done(function () {
            console.log("done");
            update();
            $.ajax({
                type: "POST",
                url: 'parsing/',
                headers: {"X-CSRFToken": $.cookie("csrftoken")},
                data: {"initializeSearchEngine": initializeSearchEngine},
                error: Error
            }).done(function () {
                $("#parseButton").prop('disabled', false);
                $("#seeAnnotationFileButton").removeClass("disabled");
                $("#initializeSearchEngine").prop('disabled', false);
                $("#progressBar").hide();
                location.reload();
            });
        });
    });


// *** Tooltip settings social icons ***

    $('#phoneNumber').click(function () {
        navigator.clipboard.writeText("0038162216560");
        $('#phoneNumber').attr('data-tooltip', 'Copied phone number!');
        $('#phoneNumber').addClass("simptip-position-top").addClass("simptip-smooth").addClass("simptip-fade");
        setTimeout(function () {
            $('#phoneNumber').removeClass("simptip-position-top").removeClass("simptip-smooth").removeClass("simptip-fade");
            $('#phoneNumber').attr('data-tooltip', '');
        }, 1500);

        return false;
    });

    $('.social-tooltip').click(function () {
        $('.tm-social-link').removeClass("simptip-position-top").removeClass("simptip-smooth").removeClass("simptip-fade");
        $('.tm-social-link').attr('data-tooltip', '');
    });

    let githubElement = $('#github');
    githubElement.hover(function () {
        githubElement.attr('data-tooltip', 'Github');
        githubElement.addClass("simptip-position-top").addClass("simptip-smooth").addClass("simptip-fade");
    }, function () {
        githubElement.removeClass("simptip-position-top").removeClass("simptip-smooth").removeClass("simptip-fade");
        githubElement.attr('data-tooltip', '');
    });

    let linkedinElement = $('#linkedin');
    linkedinElement.hover(function () {
        linkedinElement.attr('data-tooltip', 'Linkedin');
        linkedinElement.addClass("simptip-position-top").addClass("simptip-smooth").addClass("simptip-fade");
    }, function () {
        linkedinElement.removeClass("simptip-position-top").removeClass("simptip-smooth").removeClass("simptip-fade");
        linkedinElement.attr('data-tooltip', '');
    });

    let phoneNumberElement = $('#phoneNumber');
    phoneNumberElement.hover(function () {
        phoneNumberElement.attr('data-tooltip', 'Copy phone number!');
        phoneNumberElement.addClass("simptip-position-top").addClass("simptip-smooth").addClass("simptip-fade");
    }, function () {
        phoneNumberElement.removeClass("simptip-position-top").removeClass("simptip-smooth").removeClass("simptip-fade");
        phoneNumberElement.attr('data-tooltip', '');
    });

    let websiteElement = $('#website');
    websiteElement.hover(function () {
        websiteElement.attr('data-tooltip', 'Personal Website');
        websiteElement.addClass("simptip-position-top").addClass("simptip-smooth").addClass("simptip-fade");
    }, function () {
        websiteElement.removeClass("simptip-position-top").removeClass("simptip-smooth").removeClass("simptip-fade");
        websiteElement.attr('data-tooltip', '');
    });
});
