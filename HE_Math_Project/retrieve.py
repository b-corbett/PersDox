import sys
import logging
from concurrent.futures import ThreadPoolExecutor, wait
from json import loads, load
from json.decoder import JSONDecodeError
from subprocess import run, SubprocessError
from requests import post


def _extract_questions(file_handle):
    questions = []
    expecteds = []
    try:
        jsn = load(file_handle)
    # --- make sure json is valid and contains what we need ---
    except JSONDecodeError as e:
        _log(logging.WARNING, e)
    if not jsn["tests"] and jsn["tests"]["question"] and jsn["tests"]["expected"]:
        _log(logging.WARNING, "One or more expected fields missing from input json.")
    # --- done ---
    for test in jsn["tests"]:
        q = test["question"]
        e = test["expected"]
        questions.append(q)
        expecteds.append(e) # TODO maybe arrange these

    return (questions, expecteds)


def _log(level, msg):
    logging.log(level, msg)
    if level >= logging.ERROR: # the threshold for errors deemed unrecoverable.
        exit(2)


def _extract_tag(html_solution):
    """
    run extract-tag on the received html_solution, and return its json output.
    """
    class_to_find = "he-info"
    if class_to_find not in html_solution:
        _log(logging.WARNING, "the string '%s' was not found in the html_solution returned by the mathbot API." % class_to_find)
    try:
        process = run(["info-tag/extract-tag.php", "-c", class_to_find], text=True, input=html_solution, capture_output=True, timeout=5)
        process.check_returncode()
        return loads(process.stdout)
    except SubprocessError as e:
        _log(logging.ERROR, "php subprocess returned with nonzero exit code. Check that php is accessible on the PATH, and that php-dom and php-mbstring are also installed.\n")


def _post_all(url, questions):
    with ThreadPoolExecutor() as executor:
        try:
            futures = \
                [executor.submit(post, url, data={"q":question}) for question in questions]

            done, not_done = wait(futures)
            if not_done:
                _log(logging.CRITICAL, "one or more POST requests failed.")
        except:
            _log(logging.ERROR, "Invalid url suppled: %s\n\n%s" % (url))
        # sort back to the order that they were given to us
        return [future.result() for future in futures]


def test_json(url, f):
    questions, expecteds = _extract_questions(f)
    responses = _post_all(url, questions)
    test_results = []
    for i, (response, expected) in enumerate(zip(responses, expecteds)):
        html_solution = ""
        try: # oh how I wish for optional chaining.
            he_math_answer = response.json()["data"]["solved"]["answer"]
            if he_math_answer["error"]: # server error, warn but continue trying to process the other questions.
                _log(logging.WARNING, he_math_answer["error"])
                
            else:
                html_solution = he_math_answer["result"]["html_solution"]
        except TypeError as e:
            _log(logging.WARNING, "One or more expected fields missing from API response: %s\n" % e)
        except KeyError as e:
            _log(logging.WARNING, "One or more expected fields missing from API response: %s\n" % e)

        # --- at this point, we should have some sort of a valid response from the server ---

        # run the php function
        jsn = _extract_tag(html_solution)
        for item in jsn:
            id = item.get("id")
            value = item.get("value")
            if id and value:
                test_results.append((i, id, expected.get(id), value))
        # add more things to compare here.

    return test_results
