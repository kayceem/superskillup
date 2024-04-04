from app.question.accessor import QuestionAccessor


class Question:

    @staticmethod
    def get_questions_by_course(course_id):
        return QuestionAccessor.get_questions_by_course(course_id)

    @staticmethod
    def get_questions_by_course_sub_topic(course_id, sub_topic_id):
        return QuestionAccessor.get_questions_by_course_sub_topic(course_id, sub_topic_id)

    @staticmethod
    def get_questions_by_sub_topic(sub_topic_id):
        return QuestionAccessor.get_questions_by_sub_topic(sub_topic_id)

    @staticmethod
    def get_question_by_id(id):
        return QuestionAccessor.get_question_by_id(id)

    @staticmethod
    def delete_question(question):
        return question.delete()
