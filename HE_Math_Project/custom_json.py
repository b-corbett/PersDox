import os
import json
import sys
import helper
import argparse
from FileFormatter import TestFile


# CREATES A SOLVER TEST JSON FILE FROM INPUT GIVEN BY USER
# AND PUTS THEM ALL INTO THE JSON_MATH_TESTS DIRECTORY

# use argparse wherever possible

if __name__ == "__main__":
	args = sys.argv 		# [<script_name> <solver_name>]
	solver = args[1] if len(args) == 2 else input("Solver name: ").strip().replace(" ", "_")

	helper.directory_init("json_math_tests")
	os.chdir("json_math_tests")						# mathbot_testing/json_math_tests

	tests = []
	question = ""
	while (question != ";"):
		question = input("Question: ")
		if question.strip() == ";":
			break

		expected = input("Expected solution: ")
		tests.append([question, expected])

	testFile = TestFile(solver, tests)
	testFile.writeFile()

	os.chdir("..")								# mathbot_testing
