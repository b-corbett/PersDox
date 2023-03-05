import helper

errorBook = {}

class TestOutput:
    def __init__(self, questions, completed_process_obj):
        self.questions = questions
        self.testCount = len(self.questions)
        self.outputs = helper.listify_std_string(completed_process_obj.stdout)
        self.errors = helper.simplify_error_list(helper.listify_std_string(completed_process_obj.stderr))
        self.returnCode = completed_process_obj.returncode
        self.resultPairs = self.getResultPairs()

    def getResultPairs(self):
        resultPairs = {'questions_w_output': {}, 'questions_w_error': {}}

        usedQuestionsIndexes = []
        if self.outputs:
            for index in range(len(self.outputs)):
                usedQuestionsIndexes.append(stdExtractedIndex := int(self.outputs[index].split(' ')[2][0]))
                resultPairs['questions_w_output'].setdefault(self.questions[stdExtractedIndex], self.outputs[index])

        remainingQuestions = [question for question in self.questions if self.questions.index(question) not in usedQuestionsIndexes]
        if self.errors:
            for index in range(len(self.errors)):
                resultPairs['questions_w_error'].setdefault(remainingQuestions[index], self.errors[index])

        return resultPairs
