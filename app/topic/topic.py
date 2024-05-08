from app.topic.accessor import TopicAccessor


class Topic:

    def __init__(self, topic):
        self.topic = topic

    @staticmethod
    def get_topic_by_id(topic_id):
        return TopicAccessor.get_topic_by_id(id=topic_id)

    @staticmethod
    def get_topics_by_course(course_id):
        return TopicAccessor.get_topics_by_course(course_id=course_id)

    @staticmethod
    def get_next_topic(topic):
        return TopicAccessor.get_next_topic(topic)

    @staticmethod
    def delete_topic(topic):
        return topic.delete()
