import os
from glob import glob
import mathgenerator as mg
import json

def get_passed_tests(result_parsed_output):
	passCount = 0
	for po in result_parsed_output:
		if "PASS" in po:
			passCount += 1
	return passCount

def get_failed_tests(result_parsed_output):
	failCount = 0
	for po in result_parsed_output:
		if "FAIL" in po:
			failCount += 1
	return failCount

def pair_question_and_error(questions, errors):
	errorsInfo = {}
	parsedErrors = errors.split("WARNING:root:the string 'he-info' was not found in the html_solution returned by the mathbot API.")
	for index in range(len(parsedErrors)-1):
		if parsedErrors[index].replace('\n', '') == "":
			errorsInfo[questions[index]] = {}
			errorsInfo[questions[index]]["original_error"] = "WARNING:root:the string 'he-info' was not found in the html_solution returned by the mathbot API."
			errorsInfo[questions[index]]["pretty_error"] = "A response was returned, but the HTML output was not tagged correctly."
			errorsInfo[questions[index]]["id"] = 0
		elif parsedErrors[index].replace('\n', '') == "WARNING:root:One or more expected fields missing from API response: list indices must be integers or slices, not str":
			errorsInfo[questions[index]] = {}
			errorsInfo[questions[index]]["original_error"] = "WARNING:root:One or more expected fields missing from API response: list indices must be integers or slices, not str"
			errorsInfo[questions[index]]["pretty_error"] = "Either there exists no solver, or the format of this question was unparseable by Mathbot."
			errorsInfo[questions[index]]["id"] = 1
		elif parsedErrors[index].replace('\n', '') == "WARNING:root:One or more expected fields missing from API response: 'html_solution'":
			errorsInfo[questions[index]] = {}
			errorsInfo[questions[index]]["original_error"] = "WARNING:root:One or more expected fields missing from API response: 'html_solution'"
			errorsInfo[questions[index]]["pretty_error"] = "The API response was missing an expected field: 'html_solution'"
			errorsInfo[questions[index]]["id"] = 2
		elif parsedErrors[index].replace('\n', '') == "WARNING:root:{'code': 6941, 'message': 'Solver did not provide an answer'}":
			errorsInfo[questions[index]] = {}
			errorsInfo[questions[index]]["original_error"] = "WARNING:root:{'code': 6941, 'message': 'Solver did not provide an answer'}"
			errorsInfo[questions[index]]["pretty_error"] = "The API did not provide an answer"
			errorsInfo[questions[index]]["id"] = 3
	return errorsInfo

def get_question_transformations(question, expected):
	transformedQuestions = []
	if '$' in question:
		noDollarSignQuestion = question.replace('$', '').strip()
		transformedQuestions.append([noDollarSignQuestion, expected])
		if '=' == noDollarSignQuestion[-1]:
			transformedQuestions.append([noDollarSignQuestion[:-1], expected])
	elif '=' == question[-1]:
		noTrailingEqualQuestion = question.strip('=').strip()
		transformedQuestions.append([noTrailingEqualQuestion, expected])
		if '$' in noTrailingEqualQuestion:
			transformedQuestions.append([noTrailingEqualQuestion.replace('$', ''), expected])

def get_problem_info(problem_name):
	for generated_problem in mg.getGenList():
		if generated_problem[3] == problem_name:
			return {
				"display_name": generated_problem[1],
				"name": generated_problem[3],
				"category": generated_problem[4]
			}

def does_file_exist(check_file_name, parent_path = "."):
# NOT BEING USED
	return bool(len(glob(f"{parent_path}/{check_file_name}")))
def directory_init(directory_name):
# used in FileFormatter/[JSONFile, InfoFile]
	try: os.mkdir(directory_name)
	except: pass
def file_init(file_name):
# NOT BEING USED
	try: open(file_name, "x")
	except: pass
def file_destroy(file_name):
# NOT BEING USED
	try: os.remove(file_name)
	except: pass

def percent_format(formatee):
	return "{:.1%}".format(formatee)

def get_test_rate(calculate_status, test_std_output):
# used in FileFormatter/TestResultsFile
	matchCount = 0
	for result in test_std_output:
		if calculate_status.upper() in result:
			matchCount += 1
	try:
		return "{:.11}".format(matchCount / len(test_std_output))
	except:
		return 0

def get_return_code_meaning(return_code):
# used in FileFormatter/TestResultsFile
	if return_code == 0:
		return "Success, all tests passed with no errors"
	elif return_code == 1:
		return "One or more tests failed"
	return ("Something went wrong when retrieving a well-structured response from the server. "
			"More info in error message down below.")
