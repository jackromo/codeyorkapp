/**
 * File: editor.js
 *
 * Contains all code for editor page.
 *
 * Author: Jack Romo <sharrackor@gmail.com>
 */


/**
 * get_test: Get the testing template from the server.
 * 
 * @param asgn_id - ID of assignment.
 * @param user_id - ID of user.
 */
function get_test(asgn_id, user_id) {
    var editor = ace.edit("code_editor");
    $("#submit").hide();
    $("#success").hide();
    $("#fail").hide();
    $("#loading").show();
    $.ajax(
        '/gettest/' + asgn_id,
        {
            method: 'POST',
            success: get_tester(asgn_id, user_id),
            error: error_submit_code
        }
    );
}


/**
 * get_tester - Get a callback which will run tests and submit them to the server.
 * 
 * @param asgn_id - ID of assignment.
 * @param user_id - ID of user.
 * @returns {Function} - Callback function, used by get_test.
 */
function get_tester(asgn_id, user_id) {
    return function(data) {
        $.ajax(
            '/testdone/' + asgn_id + '/' + user_id,
            {
                method: 'POST',
                data: test_prog(data['test_template']),
                contentType: 'application/json',
                dataType: 'json',
                success: success_submit_code,
                error: error_submit_code
            }
        );
    };
}


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


// Skulpt code


/**
 * get_skulpt_out_func: Get a function which sends result of skulpt interpreter to output pre.
 *
 * @param out_id - ID of element, which acts as text output of interpreter.
 */
function get_skulpt_out_func(out_id) {
    return function(text) {
        $("#" + out_id).append(text);
    };
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
 * 
 * @param in_prog - String of Python code to run. If null, look in Ace editor.
 * @param out_pre_id - ID of pre to use as stdout and stderr.
 * @param canvas_pre_id - ID of pre to user for graphics. If null, then no canvas.
 */
function skulpt_run(in_prog, out_pre_id, canvas_pre_id) {
    var prog;
    if(in_prog != null)
        prog = in_prog;
    else
        prog = ace.edit("code_editor").getValue();
    var out_pre = $("#" + out_pre_id);
    out_pre.html('');
    Sk.pre = out_pre_id;
    Sk.configure({output:get_skulpt_out_func(out_pre_id), read:skulpt_read});
    if(canvas_pre_id != null)
        (Sk.TurtleGraphics || (Sk.TurtleGraphics = {})).target = canvas_pre_id;
    var myPromise = Sk.misceval.asyncToPromise(function() {
        return Sk.importMainWithBody("<stdin>", false, prog, true);
    });
    myPromise.then(function(mod) {
        console.log('User code run successfully.');
    }, function(err) {
        out_pre.html(err.toString());
    });
}


// Testing code


/**
 * test_prog: Test code currently in editor pre.
 *
 * @param test_template - Test program template received from server, to have user code filled in.
 * @returns {*} - Stringified JSON of test results string and original program.
 */
function test_prog(test_template) {
    var orig_prog = ace.edit("code_editor").getValue();
    var out_pre = $("#test_out");
    // replace inbuilt functions with user defined versions
    var prog = orig_prog.replace(/input\(/g, '_input(_test_inputs, ')
                        .replace(/raw_input\(/g, '_raw_input(_test_inputs, ');
    var indented_prog = ('\t' + prog).replace(/\n/g, '\n\t');
    var test_prog = test_template.replace(/_proghere_/, indented_prog);
    skulpt_run(test_prog, out_pre.attr('id'), null);
    var test_result = out_pre.html().slice(0, -1);  // will have a \n on the end
    out_pre.html('');
    return JSON.stringify({
        test_result: test_result,
        program: orig_prog
    });
}
