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
# Course
COURSE_NOT_FOUND = 700
# Topic
TOPIC_NOT_FOUND = 705
# Sub Topic
SUB_TOPIC_NOT_FOUND = 715

# Question
QUESTION_NOT_FOUND = 400
USER_ANSWER_NOT_FOUND = 401

# User Assignment
USER_ASSIGNMENT_NOT_FOUND = 402
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
    USER_ANSWER_NOT_FOUND: "User answer not found",
    COURSE_NOT_FOUND: "Course not found",
    TOPIC_NOT_FOUND: "Topic not found",
    SUB_TOPIC_NOT_FOUND: "Sub topic not found",
    USER_ASSIGNMENT_NOT_FOUND: "Assignment not found",
}
