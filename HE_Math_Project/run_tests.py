import os
import subprocess as sp
import json
import helper
from glob import glob
from datetime import datetime
from FileFormatter import ResultsFile

# ITERATES THROUGH EACH JSON FILE IN JSON_MATH_TESTS DIRECTORY AND SENDS THEM TO THE SOLVER
# USING THE MATHBOT API. CREATES TEST.TXT FOR EACH PROBLEM WITH RELEVANT TEST INFORMATION.

# in a test.txt file in json_math_tests/ put stats/success rates of types/number of problems,
# problems that failed,
#		success rates by solved/unsolved,
#		success rates by category
# and other metrics

#		vvv 1/22 vvv
# UPDATE THE README.md

#       vvv 1/28 vvv
# Do some research on the solvers that result in both WARNINGs, why are they doing that? (ex. bcd_to_decimal, percentage_error)

if __name__ == "__main__":
	start = datetime.now()

	helper.directory_init("json_math_tests")
	os.chdir("json_math_tests")					# mathbot_testing/json_math_tests

	solverDirectories = glob("*/")

	for solverDir in solverDirectories:
		os.chdir(solverDir)						# mathbot_testing/json_math_tests/{solver_directory}

		testFilePath = glob("*.json")[0]

		os.chdir("../..")						#  mathbot_testing

		cmd = f"python test.py -v --ascii ./json_math_tests/{solverDir}{testFilePath}".split(" ")
		output = sp.run(cmd, text=True, capture_output=True)

		os.chdir(f"json_math_tests/{solverDir}")    # mathbot_testing/json_math_tests/{solver_directory}

		with open(testFilePath, "r") as fileRead:
			testFile = json.loads(fileRead.read())
			questions = [test['question'] for test in testFile["tests"]]
		resultsFile = ResultsFile(solverDir.replace('/', ''), questions, output)
		resultsFile.writeFile()

		os.chdir("..")								# mathbot_testing

	os.chdir("..")
	print(f"Time to run all tests: {datetime.now() - start}")
