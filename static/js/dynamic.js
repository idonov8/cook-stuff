$(document).ready(function() {

	$('form').on('submit', (event) => {
		$.ajax({
			data : {
				ingredients : $('#ingredients').val()
			},
			type : 'POST',
            url : '/getRecipe',
            dataType: 'json',
		})
		.done((data) => {
           if (data.error) {
                $('#errorAlert').text(data.error).show();
                $('#recipes').hide()
			} else {
                $('#recipes').empty();
                $.each(data.recipes, (index, element) => {
                    $('#recipes').append($('<h3>', {text: element.title}),'</h3>');
                });
                $('#errorAlert').hide()
                console.log(data)
            }	 		
		});

        $('#recipes').text("Loading...").show();
		event.preventDefault();

	});

});