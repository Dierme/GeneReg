/* Project specific Javascript goes here. */

$body = $("body");

// Submit request on submit
$(document).ready(function() {
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $('#create-request').on('submit', function(event){
        event.preventDefault();
        console.log("form submitted!")  // sanity check
        create_post();
    });

    function create_post() {
        console.log("create post is working!") // sanity check
        $.ajax({
            url : "/request/", // the endpoint
            type : "POST", // http method
//            data : {'search_form': $("#create-request").serializeArray()}, // data sent with the post request{
            data : $("#create-request").serializeArray(),
            beforeSend: function(xhr, settings) {
                $body.addClass("loading-pause");
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            // handle a successful response
            success : function(json) {
                if(json.success){
                    $('#tabs-box-2').html(json.html)
                    $('#tabs-box-1').removeClass("in")
                    $('#tabs-box-1').removeClass("active")
                    $('#tabs-box-2').addClass("active")
                    $('#tabs-box-2').addClass("in")
                    $( "#nav-tab1" ).removeClass( "active" );
                    $( "#nav-tab2" ).addClass( "active" );
                    console.log("success"); // another sanity check
                }
                else{
                    $('#errors').html('');
                    console.log("unsuccessful");
                    $('#errors').html(json.html)
                }
            },
            complete: function(xhr, settings) {
                $body.removeClass("loading-pause");
            },
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;<    /a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    };

    // collapse gene on click
    $('.request-content').on('click', ".list-item-sm", function(){
        var elem = $(this);
        collapse_list_element(elem);
    });

    // collapse all genes on click
    $('.request-content').on('click', "#collapse-all-genes", function(){
        var status = $(this).val();
        console.log(status);
        if(status == '0'){
            $(".list-item-sm").each(function(){
                var elem = $(this);
                collapse_list_element(elem, true);
            })
            $(this).val('1')
        }
        if(status == '1'){
            $(".list-item-sm").each(function(){
                var elem = $(this);
                collapse_list_element(elem, false);
            });
            $(this).val('0')
        }
    });
});


function collapse_list_element(element, direction = null){
        //  direction == null
        //      custom user click collapse
        //  direction == true
        //      opening list element
        //  direction == false
        //      closing list element
        console.log(direction)
        if(direction === null){
            if(!element.hasClass('active')){
                element.addClass('active')
                collapse_id = element.attr('data-target');
                $(collapse_id).collapse('show')
            }
            else{
                element.removeClass('active')
                collapse_id = element.attr('data-target');
                $(collapse_id).collapse('hide');
            }
        }
        else if(direction === true) {
            if(!element.hasClass('active')){
                element.addClass('active')
                collapse_id = element.attr('data-target');
                $(collapse_id).collapse('show')
            }
        }
        else if (direction === false) {
            element.removeClass('active')
            collapse_id = element.attr('data-target');
            $(collapse_id).collapse('hide');
        }
    }