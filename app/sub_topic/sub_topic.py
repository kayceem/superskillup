from app.sub_topic.accessor import SubTopicAccessor


class SubTopic:

    def __init__(self, sub_topic):
        self.sub_topic = sub_topic

    @staticmethod
    def get_sub_topic_by_id(sub_topic_id):
        return SubTopicAccessor.get_sub_topic_by_id(id=sub_topic_id)

    @staticmethod
    def get_sub_topics_by_topic(topic_id):
        return SubTopicAccessor.get_sub_topics_by_topic(topic_id=topic_id)

    @staticmethod
    def delete_sub_topic(sub_topic):
        return sub_topic.delete()
