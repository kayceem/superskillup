import uuid
from app.api.api import SUCCESS

def get_char_uuid(length: int = None) -> str:
    id = uuid.uuid4().hex
    return id[:length]


def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None


def is_status_failed(status: int) -> bool:
    return status != SUCCESS

