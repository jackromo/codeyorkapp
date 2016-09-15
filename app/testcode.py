"""
Testing occurs in several stages:

1. Client tells server to send it assignment test function (/gettest).
2. Server sends testing program template, which user program will be inserted into.
3. Client builds Python test program and runs it, putting output into a hidden pre.
4. Client collects results from this pre, empties it, and sends printed results + program back to server (/testdone).
5. Server parses test results and tells client if tests were passed or not. Results stored if so.
"""

from models import Assignment, AssignmentTest


# Passed to client with test parameters.
test_template = """
def _raw_input(dummy_inputs, prompt):
    for _, i in enumerate(dummy_inputs.strip().split('\\n')):
        yield i

def _input(dummy_inputs, prompt):
    for _, i in enumerate(dummy_inputs.strip().split('\\n')):
        yield i

def _user_prog(_test_inputs):
_proghere_

for inp in %s:
    _user_prog(inp)
"""


def get_test_str(assignment):
    """
    Get string of program, which will be merged with program and test its effectiveness.

    Program string will have the following characters to show where to put the user code: _proghere_
    (which should be entered indented by one tab.)

    When user code is placed here, program will override input and raw_input (not open atm), as well as
    encapsulate the user program in a function called _user_prog(inputs). input/raw_input will sample
    the inputs argument, which is a list of results. Print is not overridden, since printed results will be
    gathered later as test results.

    Args:
        assignment (Assignment): Assignment to get test for.

    Returns:
        str: Template for program test. Will be used by client for testing.

    """
    assignment_tests = AssignmentTest.query.filter(AssignmentTest.asgn_id == assignment.id)
    test_inp_ls = [asgn_test.test_inp for asgn_test in assignment_tests]
    return test_template % str(test_inp_ls)


def check_test_results(assignment, test_results):
    """
    Check whether test results show that program solves a given assignment.

    Args:
        assignment (Assignment): Assignment to be solved.
        test_results (str): Result string from running test function on client.

    Returns:
        bool: Whether tests were successful or not.
    """
    assignment_tests = AssignmentTest.query.filter(AssignmentTest.asgn_id == assignment.id)
    expected_out = '\n'.join([asgn_test.test_out for asgn_test in assignment_tests])
    return expected_out == test_results


# TODO: deprecate this
def test_code(assignment, code_str):
    """
    Test whether a program string solves a given assignment.

    Args:
        assignment (Assignment): Assignment to be solved.
        code_str (str): Code posed as a solution to assignment.

    Returns:
        bool: Whether solution is sufficient or not.
    """
    # TODO
    return True
