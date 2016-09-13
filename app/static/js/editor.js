/**
 * File: editor.js
 *
 * Contains all code for editor page.
 *
 * Author: Jack Romo <sharrackor@gmail.com>
 */


/**
 * submit_code: Submit a code solution and handle the response.
 *
 * @param asgn_id - Assignment ID.
 * @param user_id - User ID.
 */
function submit_code(asgn_id, user_id) {
    $("#submit").hide();
    $("#loading").show();
    $.post('/submitcode/' + asgn_id + '/' + user_id, {
        contents: $("#code_editor").text()
    }).done(function(result) {
        if(result['solved'])
            $("#success").show();
        else
            $("#fail").show();
        $("#loading").hide();
        $("#submit").show();
    }).fail(function() {
        alert("Error: Could not contact server. Check your internet connection and try again.");
        $("#loading").hide();
        $("#submit").show();
    });
}
