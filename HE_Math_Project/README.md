# mathbot_testing

```sh
git clone https://vcs.he.net/brian.corbett/mathbot_testing.git --recursive
```

## Usage

### Create python environment

```sh
bash make-venv.bash venv
source venv/bin/activate
export PYTHONPATH=${PYTHONPATH}:$(pwd)
```

### Structure of **json_math_tests/**

The testing script **run_tests.py** will loop through each test in the **json_math_tests/** directory. Initially, after cloning, **json_math_tests/** should be empty. Before explaining how to populate the directory with tests, I will explain the intended structure of the directory. At a minimum, it should have:

* A folder for each solver to be tested, with the same name as the solver
* A well-formed JSON test file in each respective folder, with the same name as the solver

```sh
.
└── json_math_tests/
    ├── addition/
    │   └── addition.json
    └── subtraction/
        └── subtraction.json
```

### Creating tests

There are 3 methods to populating **json_math_tests/** with tests:

* #### Manually create and place a JSON test file
Each JSON test file must follow the format exemplified by this file: [prove_identity.json](prove_identity.json)
Then place each JSON test file into it's own folder by the same name: **prove_identity/prove_identity.json**
**_Take notice: the JSON file, the 'solver' field in the JSON file, and the folder the JSON file is placed in should all have the same name._**

* #### Run script **custom_json.py**
This script takes a solver name as its only argument:
```sh
python custom_json.py addition
```
Or you can pass no argument, and the script will prompt you to specify a solver name.

Then it will prompt you for a question to pass to mathbot, and an expected result. It will keep prompting for and saving each question/expected pair until a semicolon (;) is given to the question prompt:
```sh
Question: 5+5
Expected: 10
Question: ;         # the semi-colon tells the script to exit the loop and create the files
```
At this point, it will create a JSON test file and a corresponding folder to place it in, then place that folder inside of **json_math_tests/**.

* #### Run script **mathgenerator_jsons.py**
This script takes no arguments (a potential argument would be how many tests to create for each problem, currently hard-coded to two):
```sh
python mathgenerator_jsons.py
```
It utilizes a python module that generates a number of questions and expected results (currently two) for many different math problems. For each generated problem, it creates a JSON test file and a corresponding **info.txt** file that captures information about the problems and the tests. This is for the overall test results file that will be created when the tests are actually run. It places the JSON test file and the **info.txt** file into it's corresponding folder and places that folder into **json_math_tests/**.

### Run tests
To loop through the contents of **json_math_tests/** and test each problem, run the script **run_tests.py**:
```sh
python run_tests.py
```
Once this script is finished, each folder in **json_math_tests/** will have a **test.txt** file that contains the results of the tests for that particular problem. In addition, **json_math_tests/** will have an **overall_test_results.txt** file that contains metrics for all the tests as a whole.
Currently, the measured metrics are _test count, pass / fail count,_ and _pass rate_. These are separated by category at the moment.


details that test.py, retrieve.py, and info-tag/ are from Rob's repo https://vcs.he.net/robert.loth/mathbot_api_test
will need to clone / copypaste from there to update files
