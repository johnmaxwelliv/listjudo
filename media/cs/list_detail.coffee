# should work with coffeescript 0.7.2

l: (output) ->
    console.log(output)

$(document).ready(->
    $("#entries").append('<p>foo</p>')
    $('#add-entry').click(->
        # The user clicked the link to add an entry to the list, now show them the entry form.
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

    # These options are related to the asynchronous submission of the entry form.
    options = {
        dataType: 'json'
        success: (data) ->
            entry_pk = data.entry_id

            # Add the new entry to the DOM
            $("#entries").append('<div style="display:none" id="entry-' + entry_pk + '">' + data.html + '</div>')
            $('#stars-wrapper-' + entry_pk).stars({
                inputType: "select",
                cancelShow: false,
                callback: (ui, type, value) ->
                    $("#stars-form-" + entry_pk).ajaxSubmit()
            });

            # Show the user the entry they added
            entry = $('#entry-' + entry_pk)
            entry.show('slow')
            $.scrollTo('#entry-' + entry_pk)

            # Reset the add entry link and the entry form to the way they were.
            $('#entry-form-div').hide()
            $('#id_description').val('')
            $('#id_title').val('')
            $('#id_embed_url').val('')
            $('#add-entry-div').show()
    }
    $("#entry-form").ajaxForm(options)

    new_comment_number: 1

    # These options are related to the asynchronous submission of the comment form.
    options = {
        dataType: 'json'
        success: (data) ->
            # Add the new comment to the DOM
            $("#comments").append('<div style="display:none" id="new-comment-' + new_comment_number + '">' + data.html + '</div>')

            # Show the user the comment they added
            comment = $('#new-comment-' + new_comment_number)
            $.scrollTo('#new-comment-' + new_comment_number)
            comment.show('slow')

            # Reset the comment form
            $('#id_body').val('')

            new_comment_number += 1
    }
    $("#comment-form").ajaxForm(options)
)
