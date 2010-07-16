# should work with coffeescript 0.7.2

$(document).ready(->
    options = {
        dataType: 'json'
        success: (data) ->
            entry_id = data.entry_id
            $("#entries").append('<div>' + data.html + '</div>')
            $('#stars-wrapper-' + entry_id).stars({
                inputType: "select",
                cancelShow: false,
                callback: (ui, type, value) ->
                    $("#stars-form-" + entry_id).ajaxSubmit();
            });
    }
    $("#entry-form").ajaxForm(options)
)
