# should work with coffeescript 0.7.2

l: (output) ->
    console.log(output)

$(document).ready(->
    $('#add-entry').click(->
        $('#add-entry-div').hide()
        $('#entry-form-div').css('opacity', 0)
        $('#entry-form-div').css('display', 'block')
        $.scrollTo('#entry-form-div')
        $('#entry-form-div').fadeIn(400, (->
            # I'm putting this callback here because the fadeIn doesn't seem to work on Google Chrome.
            $('#entry-form-div').css('opacity', 1)
        ))
        return false
    )
    options = {
        dataType: 'json'
        success: (data) ->
            entry_pk = data.entry_id

            $("#entries").append('<div style="display:none" id="entry-' + entry_pk + '">' + data.html + '</div>')
            $('#stars-wrapper-' + entry_pk).stars({
                inputType: "select",
                cancelShow: false,
                callback: (ui, type, value) ->
                    $("#stars-form-" + entry_pk).ajaxSubmit()
            });

            entry = $('#entry-' + entry_pk)
            $.scrollTo('#entry-' + entry_pk)
            entry.show('slow')

            $('#entry-form-div').hide()
            $('#id_description').val('')
            $('#id_title').val('')
            $('#add-entry-div').show()
    }
    $("#entry-form").ajaxForm(options)
)
