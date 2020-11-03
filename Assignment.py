from Question import Question


class Assignment:
    lst_ques: [Question]
    student_id: int

    def __init__(self, student_id, lst_ques):
        self.student_id = student_id
        self.lst_ques = lst_ques

