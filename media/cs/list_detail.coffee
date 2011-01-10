# should work with coffeescript 0.7.2

l: (output) ->
    console.log(output)

make_show_hide_form: (name) ->
    # Add click events for a form that is shown by a button #add-[name]
    # and hidden by a button #cancel-add-[name]
    button = $('#add-' + name)
    form = $('#' + name + '-form')
    $('#add-' + name).click(->
        button.hide()
        form.show()
        $.scrollTo(form.offset().top - 80, 400)
    )
    $('#cancel-add-' + name).click(->
        form.hide()
        button.show()
    )

$(document).ready(->
    # ENTRIES

    # Form show/hide
    make_show_hide_form('entry')

    # Asynchronous form submission
    options = {
        dataType: 'json'
        success: (data) ->
            # Add the new entry to the DOM
            $("#entries").prepend(data.html)
            $('#entry-' + data.id + '-stars-wrapper').stars({
                inputType: "select",
                cancelShow: false,
                callback: (ui, type, value) ->
                    $('#entry-' + data.id + '-stars-form').ajaxSubmit()
            });

            # Reset the add entry link and the entry form to the way they were
            $('#entry-form').hide()
            $('#id_description').val('')
            $('#id_title').val('')
            $('#id_embed_url').val('')
            $('#add-entry').show()

            # Show the user the entry they added
            entry = $('#entry-' + data.id)
            entry.hide()
            entry.show('slow')
    }
    $("#entry-form").ajaxForm(options)



    # COMMENTS

    # Form show/hide
    make_show_hide_form('comment')

    # Asynchronous form submission
    options = {
        dataType: 'json'
        success: (data) ->
            # Add the new comment to the DOM
            $("#comments").append(data.html)

            # Show the user the comment they added
            comment = $('#comment-' + data.id)
            comment.hide()
            comment.show('slow')

            # Reset the comment form
            $('#comment-form').hide()
            $('#id_body').val('')
            $('#add-comment').show()
    }
    $("#comment-form").ajaxForm(options)
)
