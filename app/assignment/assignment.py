from app.assignment.accessor import AssignmentAccessor


class Assignment:

    def __init__(self, assignment):
        self.assignment = assignment

    @staticmethod
    def get_assignment_by_id(id):
        return AssignmentAccessor.get_assignment_by_id(id)

    @staticmethod
    def get_assignments_by_course(course_id):
        return AssignmentAccessor.get_assignments_by_course(course_id)

    @staticmethod
    def delete_assignment(assignment):
        return assignment.delete()
