import os
import mathgenerator as mg
import json
from glob import glob









def simplify_error_list(error_list):
	commonError = "WARNING:root:the string 'he-info' was not found in the html_solution returned by the mathbot API."
	doRemoveCommonError = False
	for error in error_list[:]:
		if not doRemoveCommonError and (error != commonError):
			doRemoveCommonError = True
		elif doRemoveCommonError and (error == commonError):
			error_list.remove(error)
			doRemoveCommonError = False
	return error_list

def listify_std_string(output_string):
	outputList = output_string.split('\n')
	[outputList.pop(outputList.index(v)) for v in outputList[:] if v == ""]
	return outputList[:-1] if ((outputList != []) and ("ERROR" in outputList[-1])) else outputList

def get_solver_info(solver_name):
	solver_info = [{"display_name": gen_prob[1], "category": gen_prob[4]}
		for gen_prob in mg.getGenList() if gen_prob[3] == solver_name]
	return solver_info[0] if solver_info else None

def directory_init(directory_name):
	try:
		os.mkdir(directory_name)
	except:
		pass

def get_test_rate(target_result, check_std_output, test_count):
	if test_count != 0:
		resultMatchCount = sum([1 for result in check_std_output if (target_result.upper() in result)])
		return resultMatchCount / test_count
	else:
		return 0

def get_return_code_meaning(return_code):
# used in FileFormatter/TestResultsFile
	if return_code == 0:
		return "Success, all tests passed with no errors"
	elif return_code == 1:
		return "One or more tests failed"
	return ("Something went wrong when retrieving a well-structured response from the server. "
			"More info in error message down below.")













# not used yet
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
