from app import models
from app.tag.accessor import TagAccessor


class Tag:

    @staticmethod
    def get_tag_by_id(id):
        return TagAccessor.get_tag_by_id(id)

    @staticmethod
    def get_all_tags():
        return TagAccessor.get_all_tags()

    @staticmethod
    def delete_tag(tag):
        return tag.hard_delete()
