/**
 * File: editor.js
 *
 * Contains all code for editor page.
 *
 * Author: Jack Romo <sharrackor@gmail.com>
 */


function success_submit_code(data) {
    if(data['solved'])
        $("#success").show();
    else
        $("#fail").show();
    $("#loading").hide();
    $("#submit").show();
}


function error_submit_code() {
    alert("Error: Could not contact server. Check your internet connection and try again.");
    $("#loading").hide();
    $("#submit").show();
}


/**
 * submit_code: Submit a code solution and handle the response.
 *
 * @param asgn_id - Assignment ID.
 * @param user_id - User ID.
 */
function submit_code(asgn_id, user_id) {
    var editor = ace.edit("code_editor");
    $("#submit").hide();
    $("#loading").show();
    $.ajax(
        '/submitcode/' + asgn_id + '/' + user_id,
        {
            method: 'POST',
            data: JSON.stringify({contents: editor.getValue()}),
            contentType: 'application/json',
            dataType: 'json',
            success: success_submit_code,
            error: error_submit_code
        }
    );
}
