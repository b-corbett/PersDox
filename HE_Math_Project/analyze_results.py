import helper
import os
import json
from glob import glob

if __name__ == '__main__':
    helper.directory_init("json_math_tests")
    os.chdir("json_math_tests")                        # mathbot_testing/json_math_tests

    overallResults = { "categories": {} }
    solverDirectories = glob("*/")

    for solverDir in solverDirectories:
        os.chdir(solverDir)                             # mathbot_testing/json_math_tests/{solver_directory}

        try:
            with open(f"{solverDir.replace('/', '')}.json", "r") as fileRead:
                testFile = json.loads(fileRead.read())
            with open("results.txt", "r") as fileRead:
                resultsFile = json.loads(fileRead.read())
        except:
        	pass

        if resultsFile["category"] != "":
            if resultsFile["category"] not in overallResults["categories"].keys():
                overallResults["categories"][resultsFile["category"]] = {
                	"test_count": 0, "pass_rate": 0, "passed": 0, "failed": 0 }
            overallResults["categories"][resultsFile["category"]]["test_count"] += resultsFile["test_count"]
            overallResults["categories"][resultsFile["category"]]["passed"] += resultsFile["pass_count"]
            overallResults["categories"][resultsFile["category"]]["failed"] += resultsFile["fail_count"]
            # overall Resuls [categories][resultsfile["category"]]["errors"] += get error count

        os.chdir("..")                                  # mathbot_testing/json_math_tests

    for category in overallResults["categories"].values():
        try:
            category["pass_rate"] = "{:.1%}".format(category["passed"] / category["test_count"])
        except:
            category["pass_rate"] = "{:.1%}".format(0)

    with open("overall_test_results.txt", "w") as fileWrite:
        fileWrite.write(json.dumps(overallResults, indent=2))


	# include custom made tests inside the overall results file. NEW: create an info file for the custom made tests as well.
	#     then in the overall results file, if it doesn't have the category field filled in (which custom made tests wouldn't)
	#     then count it separately from the generated tests. same with manually created tests: there likely won't be a info.txt
	#     file (unless the user will create it), so if there is no info.txt file, it will include it in the overall somehow
	# currently the overall results file separates by category. now combine them all to get a true overall measurement.
