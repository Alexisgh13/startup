$('#form_add_category').hide();

$('.add_button').click(function() {
    if ($(this + 'i').hasClass('fa-plus')) {
        $('#form_add_category').fadeIn();
        $('.add_button i').removeClass('fa-plus');
        $('.add_button i').addClass('fa-minus');
    }else{
        $('#form_add_category').fadeOut();
        $('.add_button i').removeClass('fa-minus');
        $('.add_button i').addClass('fa-plus');
    }
});
