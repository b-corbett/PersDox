import json
import datetime
import helper
from glob import glob

class TestFile:
    def __init__(self, solver, tests):
        self.solver = solver
        self.tests = tests

    def content(self):
        fileContent = {
            'solver': self.solver,
            'tests': []
        }
        for test in self.tests:
            question, expected = test[0], test[1]
            newTest = {
                "question": question,
                "expected": {
                    "he-info-solver-answer": expected
                }
            }
            fileContent['tests'].append(newTest)
        return fileContent

    def writeFile(self):
        helper.directory_init(self.solver)
        with open(f"./{self.solver}/{self.solver}.json", "w") as fileWrite:
            fileWrite.write(json.dumps(self.content(), indent=2))

class ResultsFile:
    def __init__(self, solver, questions, output):
        self.solver = solver
        self.questions = questions
        self.returnCode = output.returncode
        self.output = output.stdout
        self.parsedOutput = self.output.split('\n')[0:-1]
        self.error = output.stderr
        self.parsedError = self.error.split('\n')[0:-1]

    def content(self):
        # refactor this method, refactor parsed_error, parsed_output, unique_errors, etc...
        # add in error_count property
        fileContent = {
            "solver": self.solver,
            "display_name": "",
            "category": "",
            "questions": self.questions,
            "question_w_errors": helper.pair_question_and_error(self.questions, self.error),
            "timestamp": datetime.datetime.now().strftime("%m/%d/%Y at %H:%M:%S"),
            "return_code": self.returnCode,
            "return_code_meaning": helper.get_return_code_meaning(self.returnCode),
            "parsed_output": self.parsedOutput,
            "parsed_error": list(set(self.parsedError) - {""}),
            "unique_errors": list(set(self.parsedError)),               # NOT BEING USED
            "test_count": len(self.parsedOutput),
            "pass_count": len([1 for result in self.parsedOutput if "PASS" in result]),
            "pass_rate": float(helper.get_test_rate("pass", self.parsedOutput)),
            "fail_count": len([1 for result in self.parsedOutput if "FAIL" in result]),
            "fail_rate": float(helper.get_test_rate("fail", self.parsedOutput)),
            "summary": ""
        }
        solver_info = helper.get_problem_info(self.solver)
        if solver_info:
            fileContent["display_name"] = solver_info["display_name"]
            fileContent["category"] = solver_info["category"]

        fileContent["summary"] += f"Timestamp: {fileContent['timestamp']}\n"
        fileContent["summary"] += f"Solver tested: {fileContent['display_name'] if fileContent['display_name'] else fileContent['solver']}\n"
        fileContent["summary"] += f"Category: {fileContent['category'] if fileContent['category'] else 'custom test'}\n\n"
        fileContent["summary"] += f"Return code: {fileContent['return_code']} - {fileContent['return_code_meaning']}\n\n"

        if fileContent["parsed_output"] != []:
            fileContent["summary"] += f"Standard output:\n"
            for result in fileContent["parsed_output"]:
                fileContent["summary"] += f"{result}\n"
            fileContent["summary"] += "-----------------\n"
            fileContent["summary"] += f"With a test count of {fileContent['test_count']}:\n"
            fileContent["summary"] += f"Pass rate: {helper.percent_format(fileContent['pass_rate'])} ({fileContent['pass_count']})\n"
            fileContent["summary"] += f"Fail rate: {helper.percent_format(fileContent['fail_rate'])} ({fileContent['fail_count']})"

        if fileContent["parsed_error"] != []:
            fileContent["summary"] += f"Standard error:\n"
            for question, error in fileContent["question_w_errors"].items():
                fileContent["summary"] += f"{question}\n\tORIGINAL: {error['original_error']}\n\tEXPLAINED: {error['pretty_error']}\n"
            fileContent["summary"] += "-----------------\n"

        return fileContent

    def writeFile(self):
        with open("results.txt", "w") as fileWrite:
            fileWrite.write(json.dumps(self.content(), indent=2))
            # fileWrite.write(self.content()["summary"])

class OverallResultsFile:
    def __init__(self):
        pass

    def content(self):
        pass

    def writeFile(self):
        pass
