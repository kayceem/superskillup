from app.models import Tag


class TagAccessor:

    @staticmethod
    def get_tag_by_id(id):
        return Tag.objects.filter(id=id).first()

    @staticmethod
    def get_all_tags():
        return Tag.objects.all()
