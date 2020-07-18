$(document).ready(() => {

    const recipeTemplate = '' +
        '<h3 class="recipeTitle" data-id={{id}}> {{title}} </h3>' +
        '<div class="recipeContent" id={{id}} style="display: none;">' +
        '<img src={{image}} width=300>' +
        '<h4> There are <strong> {{missedIngredientCount}} </strong> additional ingredients that you will need' +
        '</div>';
    
    const $recipes = $('#recipes')
	$('form').on('submit', (event) => {

        $.ajax({
            data: {
                ingredients: $('#ingredients').val()
            },
            type: 'POST',
            url: '/getRecipe',
            dataType: 'json',

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
        $recipes.text("Loading...").show();
        event.preventDefault();
    });

    $recipes.delegate('.recipeTitle','click',function() {
        console.log("clicked", $(this));
        $('#' + $(this).attr('data-id')).toggle(1000);
    });
});