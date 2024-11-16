from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.template.defaultfilters import filesizeformat

@deconstructible
class FileValidator:
    """
    Validator for files, checking:
    - max_size: maximum file size
    - content_types: list of allowed content types
    """

    def __init__(self, max_size=None, content_types=()):
        self.max_size = max_size
        self.content_types = content_types

    def __call__(self, data):
        # Validate file size
        if self.max_size is not None and data.size > self.max_size:
            raise ValidationError(
                f'File size must not exceed {filesizeformat(self.max_size)}. '
                f'Current file size is {filesizeformat(data.size)}.'
            )

        # Validate content type using UploadedFile's content_type attribute
        if self.content_types:
            content_type = data.content_type  # Access content_type directly
            if content_type not in self.content_types:
                raise ValidationError(
                    f'File type ({content_type}) is not supported. '
                    f'Allowed types are: {", ".join(self.content_types)}'
                )

    def __eq__(self, other):
        return (
            isinstance(other, FileValidator)
            and self.max_size == other.max_size
            and self.content_types == other.content_types
        )