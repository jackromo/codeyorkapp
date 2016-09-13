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


// Skulpt code


/**
 * skulpt_out: Send result of skulpt interpreter to output pre.
 *
 * @param text - text output of interpreter.
 */
function skulpt_out(text) {
    $("#editor_out").append(text);
}


/**
 * skulpt_read: Input callable used by Skulpt to load modules.
 *
 * @param x - Requested module.
 * @returns {*} - Module requested.
 */
function skulpt_read(x) {
    if (Sk.builtinFiles === undefined || Sk.builtinFiles["files"][x] === undefined)
        throw "File not found: '" + x + "'";
    return Sk.builtinFiles["files"][x];
}


/**
 * skulpt_run: Run user-entered Python code. Called on 'Run' button press.
 */
function skulpt_run() {
   var prog = ace.edit("code_editor").getValue();
   var mypre = $("#editor_out");
   mypre.html('');
   Sk.pre = "editor_out";
   Sk.configure({output:skulpt_out, read:skulpt_read});
   (Sk.TurtleGraphics || (Sk.TurtleGraphics = {})).target = 'editor_canvas';
   var myPromise = Sk.misceval.asyncToPromise(function() {
       return Sk.importMainWithBody("<stdin>", false, prog, true);
   });
   myPromise.then(function(mod) {
       console.log('success');
   }, function(err) {
       console.log(err.toString());
   });
}
