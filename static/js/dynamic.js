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
                    '<p class="card-text">There are <strong> {{missedIngredientCount}} </strong> additional ingredients that you will need'//</p>'+
                    '<a href="#" class="btn btn-primary">Go somewhere</a>'+
                '</div>'+
            '</div>'+
        '</div>';

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
                    $.each(data.recipes, (index, element) => {
                        $recipes.append(Mustache.render(recipeTemplate, element));
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
    $recipes.delegate('.recipeTitle', 'click', function () {
        console.log("clicked", $(this));
        $('#' + $(this).attr('data-id')).toggle(1000);
    });
});