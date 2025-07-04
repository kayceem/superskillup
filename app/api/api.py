SUCCESS = 1

# Invalid input
INVALID_INPUT = 100
TOO_MANY_REQUEST = 101

# User
INVALID_LOGIN_TOKEN = 300
UNAUTHORIZED = 301
USER_NOT_FOUND = 302
INVALID_PASSWORD = 303
ADMIN_USER_NOT_FOUND = 304
EMAIL_ALREADY_EXISTS = 308
USER_NOT_VERIFIED = 305
USER_VERIFIED = 201
OTP_ALREADY_SENT = 202
# OTP
OTP_VERIFICATION_FAILED = 600
# Search
INVALID_SEARCH_QUERY = 605
# Course
COURSE_NOT_FOUND = 700
# Topic
TOPIC_NOT_FOUND = 705
# Sub Topic
SUB_TOPIC_NOT_FOUND = 715

# Question
QUESTION_NOT_FOUND = 400
QUESTION_ANSWER_NOT_FOUND = 401

# User Enrollment
USER_ENROLLMENT_NOT_FOUND = 402
USER_ENROLLED_COURSE_NOT_FOUND = 410
USER_ENROLLED_TOPIC_NOT_FOUND = 411
USER_ENROLLED_SUB_TOPIC_NOT_FOUND = 412
USER_ENROLLED_QUESTION_NOT_FOUND = 413
USER_ENROLLED_MANAGER_NOT_FOUND = 414

# Assignment
ASSIGNMENT_NOT_FOUND = 415
USER_ASSIGNMENT_NOT_FOUND = 416
USER_ASSIGNMENT_SUBMISSION_NOT_FOUND = 417

# Gpt Review
GPT_REVIEW_NOT_FOUND = 420

# Tag
TAG_NOT_FOUND = 430

# Manager Feedback
MANAGER_FEEDBACK_NOT_FOUND = 403

# Delete
DELETE_ERROR = 720

error_messages = {
    INVALID_INPUT: 'Invalid input',
    TOO_MANY_REQUEST: 'Too many requests',
    INVALID_LOGIN_TOKEN: 'Invalid token for login',
    UNAUTHORIZED: "Unauthorized",
    USER_NOT_FOUND: "User not found",
    INVALID_PASSWORD: "Invalid password",
    ADMIN_USER_NOT_FOUND: "Admin user not found",
    OTP_VERIFICATION_FAILED: "OTP verification failed",
    EMAIL_ALREADY_EXISTS: "User already exists with this email",
    USER_NOT_VERIFIED: "User is not verified",
    USER_VERIFIED: "User is already verified",
    OTP_ALREADY_SENT: "OTP was already sent. Please check your mail",
    QUESTION_NOT_FOUND: "Question doesn't exists",
    QUESTION_ANSWER_NOT_FOUND: "User answer not found",
    COURSE_NOT_FOUND: "Course not found",
    TOPIC_NOT_FOUND: "Topic not found",
    SUB_TOPIC_NOT_FOUND: "Sub topic not found",
    USER_ENROLLMENT_NOT_FOUND: "Enrollment not found",
    USER_ENROLLED_COURSE_NOT_FOUND: "Enrolled courses not found",
    USER_ENROLLED_TOPIC_NOT_FOUND: "Enrolled topics not found",
    USER_ENROLLED_SUB_TOPIC_NOT_FOUND: "Enrolled sub topics not found",
    USER_ENROLLED_QUESTION_NOT_FOUND: "Enrolled questions not found",
    USER_ENROLLED_MANAGER_NOT_FOUND: "Managers not found",
    ASSIGNMENT_NOT_FOUND: "Assignment not found",
    USER_ASSIGNMENT_NOT_FOUND: "User assignment not found",
    USER_ASSIGNMENT_SUBMISSION_NOT_FOUND: "User assignment submission not found",
    GPT_REVIEW_NOT_FOUND: "Gpt review not found",
    TAG_NOT_FOUND: "Tag not found",
    MANAGER_FEEDBACK_NOT_FOUND: "Manager Feedback not found",
    INVALID_SEARCH_QUERY: "Invalid search query",
}
