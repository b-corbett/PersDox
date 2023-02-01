import helper
from glob import glob
import os
from datetime import datetime
import FileFormatter as FF
import mathgenerator as mg
import json

if __name__ == '__main__':
    # with open("./json_math_tests/addition/addition.json", "r") as fileRead:
    # 	jsonTests = json.loads(fileRead.read())
    # 	tests = [test['question'] for test in jsonTests["tests"]]
    print({1, 2, 3, 4, 5, 6} - {5})

    # os.chdir("json_math_tests")
    # solverDirectories = glob("*/")
    # i = 1
    # with open("unparseable_or_unsolved.txt", "a") as fileAppend:
    #     for solverDir in solverDirectories:
    #         os.chdir(solverDir)
    #
    #         with open("test.txt", "r") as readFile:
    #             fileContent = readFile.read()
    #
    #         if "indices" in fileContent:
    #             fileAppend.write(f"{i} - {solverDir}\n")
    #             fileAppend.write("\tindices\n")
    #             i += 1
    #             fileAppend.write("\n")
    #
    #         os.chdir("..")
