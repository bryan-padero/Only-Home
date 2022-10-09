$(document).ready(function(){
    var token =  $('input[name="csrf_token"]').attr('value');
    function load_data(property_type='')
    {
        $.ajax({
            url:"/process",
            type:"POST",
            data:{
                property_type: property_type
            },
            headers: {
                'X-CSRF-Token': token,
            },
            success:function(data)
            {
                $('#properties').fadeOut(1).fadeIn(1500);
                $('#properties').html(data);
            }
        })
    }
    $('#property_type').change(function(){
        var property_type = $('#property_type').val();
        load_data(property_type);
    });
});

