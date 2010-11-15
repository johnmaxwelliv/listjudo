# should work with coffeescript 0.7.2

l: (output) ->
    console.log(output)

$(document).ready(->
    # ENTRIES

    $('#add-entry').click(->
        # The user clicked the link to add an entry to the list, now show them the entry form.
        $('#add-entry-div').hide()
        $.scrollTo('#entry-form-div')
        $('#entry-form-div').show('fast')
    )

    # These options are related to the asynchronous submission of the entry form.
    options = {
        dataType: 'json'
        success: (data) ->
            entry_pk = data.id

            # Add the new entry to the DOM
            $("#entries").append(data.html)
            entry = $('#entry-' + entry_pk)
            $('#entry-' + entry_pk + '-stars-wrapper').stars({
                inputType: "select",
                cancelShow: false,
                callback: (ui, type, value) ->
                    $('#entry-' + entry_pk + '-stars-form').ajaxSubmit()
            });

            # Show the user the entry they added
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



    # COMMENTS

    $('#add-comment').click(->
        # The user clicked the link to add an entry to the list, now show them the entry form.
        $('#add-comment-div').hide()
        $.scrollTo('#comment-form-div')
        $('#comment-form-div').show('fast')
    )

    # These options are related to the asynchronous submission of the comment form.
    options = {
        dataType: 'json'
        success: (data) ->
            # Add the new comment to the DOM
            $("#comments").append(data.html)

            # Reset the comment form
            $('#id_body').val('')
    }
    $("#comment-form").ajaxForm(options)
)
