import os
import subprocess
import helper
import File
import Output
import json
from glob import glob
from datetime import datetime

# ITERATES THROUGH EACH JSON FILE IN JSON_MATH_TESTS DIRECTORY AND SENDS THEM TO THE SOLVER
# USING THE MATHBOT API. CREATES TEST.TXT FOR EACH PROBLEM WITH RELEVANT TEST INFORMATION.

# include custom made tests inside the overall results file. NEW: create an info file for the custom made tests as well.
	#     then in the overall results file, if it doesn't have the category field filled in (which custom made tests wouldn't)
	#     then count it separately from the generated tests. same with manually created tests: there likely won't be a info.txt
	#     file (unless the user will create it), so if there is no info.txt file, it will include it in the overall somehow
	# currently the overall results file separates by category. now combine them all to get a true overall measurement.

if __name__ == "__main__":
	start = datetime.now()

	helper.directory_init("json_math_tests")
	os.chdir("json_math_tests")					# mathbot_testing/json_math_tests

	overallResultsFile = File.OverallResultsFile()
	solverDirectories = [dir_name.strip('/') for dir_name in glob("*/")]
	for solverDir in solverDirectories:
		os.chdir(solverDir)						# mathbot_testing/json_math_tests/{solver_directory}
		testFile = glob("*.json")[0]

		os.chdir("../..")							# mathbot_testing/
		cmd = f"python test.py -v --ascii ./json_math_tests/{solverDir}/{testFile}".split(" ")
		output = subprocess.run(cmd, text=True, capture_output=True)

		os.chdir(f"json_math_tests/{solverDir}")   # mathbot_testing/json_math_tests/{solver_directory}
		with open(testFile, "r") as fileRead:
			testQuestions = [test['question'] for test in json.loads(fileRead.read())['tests']]

		resultsFile = File.ResultsFile(solverDir, Output.TestOutput(testQuestions, output))
		resultsFile.writeFile()

		os.chdir("..")								# mathbot_testing/json_math_tests
		overallResultsFile.addResultFile(resultsFile)

	overallResultsFile.writeFile()

	os.chdir("..")									# mathbot_testing/
	print(f"Testing duration: {datetime.now() - start}")
