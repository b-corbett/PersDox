import os
import sys
import helper
import json
import File
# import argparse

# CREATES A SOLVER TEST JSON FILE FROM INPUT GIVEN BY USER
# AND PUTS THEM ALL INTO THE JSON_MATH_TESTS DIRECTORY

# use argparse wherever possible

if __name__ == "__main__":
	args = sys.argv 		# <script_name> <solver_name> [<test_pairs>]

	solver = args[1]
	tests = json.loads(args[2])

	os.chdir("json_math_tests/manual")

	testFile = File.TestFile("manual")
	testFile.setSolver(solver)
	
	for testPair in tests:
		testFile.addTest(testPair[0], testPair[1])

	testFile.writeFile()

	os.chdir("../..")								# mathbot_testing/
