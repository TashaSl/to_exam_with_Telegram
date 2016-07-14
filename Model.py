import re

class Model():
    def __init__(self):
        self.arr_questions = self.__read_file('questions.txt')
        answers = ' '.join(self.__read_file('answers.txt'))
        self.arr_answers = self.__make_arr_answers(answers)

    def __read_file(self, name_file):
        arr = []
        f = open(name_file, 'r', encoding='utf-8')
        arr = f.readlines()
        f.close()
        for i, element in enumerate(arr):
            element = element.replace('\n', '')
            arr[i] = re.sub('^[0-9]*[.][ ]', '', element)
        return arr

    def __make_arr_answers(self, answers):
        arr = []
        for question in self.arr_questions[::-1]:
            match = answers.find(question)
            if match == -1:
                arr.insert(0, '')
                continue
            arr.insert(0, answers[match:])
            answers = answers[:match]
        return arr


    def find(self, i):
        if i < 0 or i > 87:
            return 'Не найден такой вопрос'
        return self.arr_answers[i]

    def find_questions(self, search_string):
        arr_matches = []
        arr_search = search_string.split()
        for question in self.arr_questions:
            n = 0
            for element in arr_search:
                if question.find(element) != -1:
                    n += 1
            arr_matches.append(n)
        if max(arr_matches) == 0:
            return -1
        return_arr = []
        for i, element in enumerate(arr_matches):
            if element == max(arr_matches):
                return_arr.append('/' + str(i + 1) + ' ' + self.arr_questions[i])
        return return_arr

    def get_all_questions(self):
        s = ''
        for i, question in enumerate(self.arr_questions):
            s = s + '"' + str(i + 1) + ' ' + question + '"\n'
        return s