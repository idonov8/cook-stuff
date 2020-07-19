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
        '<h3 class="recipeTitle" data-id={{id}}> {{title}} </h3>' +
        '<div class="recipeContent" id={{id}} style="display: none;">' +
        '<img src={{image}} width=300>' +
        '<h4> There are <strong> {{missedIngredientCount}} </strong> additional ingredients that you will need' +
        '</div>';

    const $recipes = $('#recipes')
    $('form').on('submit', function(event){
        const formData = new FormData(this);
        $.ajax({
            data: formData,
            type: 'POST',
            url: '/getRecipe',
            cache: false,
            contentType: false,
            processData: false,
            // dataType: 'json',
        })
            .done((data) => {
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
            });
        
        $("body").appendChild(formData.get('image'));
        $recipes.text("Loading...").show();
        event.preventDefault();
    });
    $recipes.delegate('.recipeTitle', 'click', function () {
        console.log("clicked", $(this));
        $('#' + $(this).attr('data-id')).toggle(1000);
    });
});