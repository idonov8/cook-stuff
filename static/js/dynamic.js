$(document).ready(() => {
    function readURL(input) {
        if (input.files && input.files[0]) {
          var reader = new FileReader();
          
          reader.onload = function(e) {
            $('#preview').attr('src', e.target.result).show();
          }
          
          reader.readAsDataURL(input.files[0]); // convert to base64 string
        }
      }
      
      $("#image").change(function() {
        readURL(this);
      });

    const recipeTemplate = '' +
        '<div class="col-sm-4">'+
            '<div class="card" style="width: 18rem;">'+
            '<img src={{image}} class="card-img-top" alt="...">'+
                '<div class="card-body">'+
                    '<h5 class="card-title">{{title}}</h5>'+
                    '<p class="card-text">There are <strong> {{missedIngredientCount}} </strong> additional ingredients that you will need</p>'+
                    '<div class="recipe-content" style="display: none;" id="{{id}}">'+
                    '</div>'+
                '</div>'+
            '</div>'+
        '</div>';

    const ingredientTemplate = ''+
    '<p class="card-text">- {{original}} </p>';

    const $recipes = $('#recipes')
    $('#ingredientsForm').on('submit', function(event){
        event.preventDefault();
        const formData = new FormData(this);
        $.ajax({
            data: formData,
            type: 'POST',
            url: '/getRecipe',
            cache: false,
            contentType: false,
            processData: false,
            success: (data) => {
                if (data.error) {
                    $('#errorAlert').text(data.error).show();
                    $recipes.hide()
                } else {
                    $recipes.empty();
                    $('#detectedIngredients').empty();
                    $('#detectedIngredients').append("<h3>Detected Ingredients:</h3> <p>"+data.ingredients+"</p> <br>")
                    $.each(data.recipes, (index, recipe) => {
                        $recipes.append(Mustache.render(recipeTemplate, recipe));
                        $("#"+recipe.id).append('<h5 class=card-subtitle>Missed Ingredients:</h5>');
                        $.each(recipe.missedIngredients, (index, ingredient) => {
                            $("#"+recipe.id).append(Mustache.render(ingredientTemplate, ingredient))
                        })
                        $("#"+recipe.id).append('<h5 class=card-subtitle>Used Ingredients:</h5>');
                        $.each(recipe.usedIngredients, (index, ingredient) => {
                            $("#"+recipe.id).append(Mustache.render(ingredientTemplate, ingredient))
                        })
                    });
                    $recipes.slideDown();
                    $('#errorAlert').hide()
                    console.log(data)
                }
            }
        });
        $recipes.html('<div class="d-flex align-items-center">'+
                         '<strong>Loading...</strong>'+
       ' <div class="spinner-border ml-auto" role="status" aria-hidden="true"></div>'+
      '</div>').show();
    });

    $('#feedback').on('submit', function(event){
        event.preventDefault();
        const formData = new FormData(this);
        $.ajax({
            data: formData,
            type: 'POST',
            url: '/sendFeedback',
            cache: false,
            contentType: false,
            processData: false,
            success: (data) => {
                console.log("got data");
                if (data.error) {
                    $('#feedbackErrorAlert').text(data.error).show();
                } else {
                    $(this).trigger('reset');;
                    $('#modal').modal('hide');
                }
            },
            error: () => {
                alert("feedback wasn't sent")

            }
        });
    });
    $recipes.delegate('.card', 'click', function (event) {
        $(this).find('.recipe-content:first').toggle(300);
    });
});