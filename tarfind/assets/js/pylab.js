	$('#name-form').on('submit', function(event){
	    event.preventDefault();
	    $('#results').html('');
	    create_name();
	});

	$('.names-table').on('click', ".delete-name", function(){
	    var id = $(this).val();
		delete_name(id);
	});

	$('#get_random_names').click(function(){
		get_random_names()		
	})


function create_name() {
    $.ajax({
        url : "create/", // the endpoint
        type : "POST", // http method
        data : $("#name-form").serializeArray(), // data sent with the post request

        // handle a successful response
        success : function(json) {
        	if(json.success == true){
        		$('.names-table').html(json.new_names_html)
        	}
        	else{
        		console.log(json.errors);
        		append_errors(json.errors, '#results')
        	}
            $('#name-text').val(''); // remove the value from the input
            console.log(json); // log the returned json to the console
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg.error+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });	
};

function delete_name(id){
	var csrftoken = $("[name=csrfmiddlewaretoken]").val();
	console.log(csrftoken)
	$.ajax({
        url : "delete/", // the endpoint
        type : "POST", // http method
        data : {'csrfmiddlewaretoken':csrftoken, 'id':id}, // data sent with the post request
        // handle a successful response
        success : function(json) {
        	if(json.success == true){
        		$('.names-table').html(json.new_names_html)
        	}
        	else{
        		console.log(json.errors);
        		append_errors(json.errors, '#results')
        	}
            
            console.log(json); // log the returned json to the console
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg.error+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });	
}

function get_random_names(){
	var csrftoken = $("[name=csrfmiddlewaretoken]").val();
	console.log(csrftoken)
	$.ajax({
        url : "random/", // the endpoint
        type : "POST", // http method
        data : {'csrfmiddlewaretoken':csrftoken}, // data sent with the post request
        // handle a successful response
        success : function(json) {
        	if(json.success == true){
        		$('#name_rand').html(json.chosen_names_html)
        	}
        	else{
        		console.log(json.errors);
        		append_errors(json.errors, '#name_rand')
        	}
            
            console.log(json); // log the returned json to the console
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg.error+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });	
}


function append_errors(errors, appendable_id){
	for (var key in errors) {
		for (i=1; i<=errors[key].length; i++){
			$(appendable_id).append('<h5>'+i+'. '+errors[key][i-1]+'</h5>')
		}
	}
}