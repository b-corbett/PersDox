import json
import helper
import os
from glob import glob
from datetime import datetime

# make classes for errors, passes, tests, etc... OOP!!

# getters and setters ?

class TestFile:
    def __init__(self, method):
        self.solver = ""
        self.tests = []
        self.method = method
        self.timestamp = datetime.now().strftime(f"%m-%d-%Y %H:%M:%S")

    def setSolver(self, solver_name):
        self.solver = solver_name
        self.tests = []

    def setContent(self, solver, tests):
        self.solver = solver
        self.tests = tests

    def addTest(self, question, expected):
        self.tests.append({
            "question": question,
            "expected": { "he-info-solver-answer": expected }
        })

    def content(self):
        return {
            'solver': self.solver,
            'tests': self.tests
        }

    def writeFile(self):
        if self.method == "generated":
            helper.directory_init(f"{self.timestamp}")
            os.chdir(f"{self.timestamp}")
            helper.directory_init(f"{self.solver}")
            os.chdir("..")
            with open(f"./{self.timestamp}/{self.solver}/{self.solver}.json", "w") as fileWrite:
                fileWrite.write(json.dumps(self.content(), indent=2))
        elif self.method == "manual":
            helper.directory_init(f"{self.solver} {self.timestamp}")
            os.chdir(f"{self.solver} {self.timestamp}")
            with open(f"./{self.solver}.json", "w") as fileWrite:
                fileWrite.write(json.dumps(self.content(), indent=2))

class ResultsFile:
    def __init__(self, solver, test_output_obj):
        self.solver = solver
        self.testOutput = test_output_obj

        self.timestamp = datetime.now()

        solver_info = helper.get_solver_info(self.solver)
        self.displayName = solver_info["display_name"] if solver_info else self.solver
        self.category = solver_info["category"] if solver_info else "custom_test"

        outputs = self.testOutput.resultPairs['questions_w_output'].values()
        errors = self.testOutput.resultPairs['questions_w_error'].values()
        test_count = len(outputs) + len(errors)
        self.testCount = test_count
        self.passCount = sum([1 for op in outputs if "PASS" in op])
        self.passRate = float(helper.get_test_rate("pass", outputs, test_count))
        self.failCount = sum([1 for op in outputs if "FAIL" in op])
        self.failRate = float(helper.get_test_rate("fail", outputs, test_count))
        self.errorCount = len(errors)
        self.errorRate = float(helper.get_test_rate("warning", errors, test_count))

    def content(self):
        return {
            "timestamp": self.timestamp.strftime("%m/%d/%Y at %H:%M:%S"),
            "solver": self.solver,
            "display_name": self.displayName,
            "category": self.category,
            "return_code": self.testOutput.returnCode,
            "return_code_meaning": helper.get_return_code_meaning(self.testOutput.returnCode),
            "questions_w_output": self.testOutput.resultPairs['questions_w_output'],
            "questions_w_error": self.testOutput.resultPairs['questions_w_error'],
            "test_count": self.testCount,
            "pass_count": self.passCount,
            "pass_rate": self.passRate,
            "fail_count": self.failCount,
            "fail_rate": self.failRate,
            "error_count": self.errorCount,
            "error_rate": self.errorRate
        }

    def writeFile(self):
        with open("results.txt", "w") as fileWrite:
            fileWrite.write(json.dumps(self.content(), indent=2))

# add timestamp, etc..
class OverallResultsFile:
    def __init__(self):
        self.resultFiles = []
        self.fileContent = { "categories": {} }

    def addResultFile(self, result_file_obj):
        self.resultFiles.append(result_file_obj)

    def content(self):
        for resultFile in self.resultFiles:
            self.fileContent["categories"].setdefault(resultFile.category, {
                "solvers": {}, "test_count": 0,
                "pass_count": 0, "pass_rate": 0,
                "fail_count": 0, "fail_rate": 0,
                "error_count": 0, "error_rate": 0})
            self.fileContent["categories"][resultFile.category]["test_count"] += resultFile.testCount
            self.fileContent["categories"][resultFile.category]["pass_count"] += resultFile.passCount
            self.fileContent["categories"][resultFile.category]["fail_count"] += resultFile.failCount
            self.fileContent["categories"][resultFile.category]["error_count"] += resultFile.errorCount

            self.fileContent["categories"][resultFile.category]["solvers"].setdefault(
                resultFile.solver, resultFile.testOutput.resultPairs)

        for category in self.fileContent["categories"].values():
            category["pass_rate"] = (category["pass_count"] / category["test_count"]) if (category["test_count"] != 0) else 0
            category["fail_rate"] = (category["fail_count"] / category["test_count"]) if (category["test_count"] != 0) else 0
            category["error_rate"] = (category["error_count"] / category["test_count"]) if (category["test_count"] != 0) else 0

        return self.fileContent

    def writeFile(self):
        with open("overall_results.txt", "w") as fileWrite:
            fileWrite.write(json.dumps(self.content(), indent=2))
