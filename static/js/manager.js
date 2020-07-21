$(document).ready(() => {
    $('.remove').on('click', function(event){
        const id = $(this).attr("id");
        $.ajax({
            type: "DELETE",
            url: ("/manager/delete/"+id),
            // data: "data",
            success: (response) => {
                $('#feedback-'+id).remove();
            },
            error: () => {
                alert('Error in removing feedback. Check your internet connection.')
            }
        });
    });
});