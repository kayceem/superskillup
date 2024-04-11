from django.core.validators import FileExtensionValidator


def get_video_extension_validator():
    allowed_extensions = ['mp4', 'webm', 'mov']
    return FileExtensionValidator(allowed_extensions)


def get_document_extension_validator():
    allowed_extensions = ['pdf', 'docx', 'txt']
    return FileExtensionValidator(allowed_extensions)
