# should work with coffeescript 0.7.2

l: (output) ->
    console.log(output)

$(document).ready(->
    $('#add-entry').click(->
        $('#add-entry-div').hide()
        $('#entry-form-div').show('slow')
    )
    options = {
        dataType: 'json'
        success: (data) ->
            entry_id = data.entry_id
            $('#entry-form-div').hide()
            $("#entries").append('<div style="display:none" id="entry-' + entry_id + '">' + data.html + '</div>')
            $('#stars-wrapper-' + entry_id).stars({
                inputType: "select",
                cancelShow: false,
                callback: (ui, type, value) ->
                    $("#stars-form-" + entry_id).ajaxSubmit();
            });
            $('#entry-' + entry_id).show('slow')
            $('#add-entry-div').show()
            l(data.form_html)
            #('#entry-form-div').html(data.form_html)
            l($('#entry-form-div').html())
            l('done')
    }
    $("#entry-form").ajaxForm(options)
)
