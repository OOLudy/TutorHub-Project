"""Serializers for the `myapp` Django app.

This module defines DRF ModelSerializers used to convert model instances to
JSON (or other content types) and to validate/deserialize input data.

Notes:
- Be careful exposing sensitive fields with `fields='__all__'`.
- Prefer explicit `fields` lists for public APIs to avoid accidental exposure
  when models change.
"""

from rest_framework import serializers
from .models import Task
from .models import PDFDocument
from .models import AIConfig


# ----------------------------------------------------------------------------
# TaskSerializer
# ----------------------------------------------------------------------------
class TaskSerializer(serializers.ModelSerializer):
    """Serializer for the Task model.

    Uses `fields='__all__'`, which exposes all model fields. If any fields are
    sensitive (passwords, tokens, etc.), replace `__all__` with an explicit
    list and mark sensitive fields as `write_only` or remove them entirely.
    """

    class Meta:
        model = Task
        # All model fields are included in this serializer. Change to an
        # explicit list if you need stricter control over the API surface.
        fields = "__all__"


# ----------------------------------------------------------------------------
# PDFDocumentSerializer
# ----------------------------------------------------------------------------
class PDFDocumentSerializer(serializers.ModelSerializer):
    """Serializer for the PDFDocument model.

    Fields explained:
    - id: primary key (int)
    - title: user-provided title (string)
    - pdf_file: file field; serialized typically as a URL depending on storage
    - uploaded_at: datetime when the file was uploaded (read-only)
    - file_size: integer file size in bytes (read-only)
    - filename: read-only field that typically contains the original file name

    The `filename` field is declared as ReadOnlyField here because it is
    usually derived from the uploaded file and should not be provided by the
    client.
    """

    # Expose the filename for convenience in responses. This field is read-only
    # and will be ignored if provided in input payloads.
    filename = serializers.ReadOnlyField()

    class Meta:
        model = PDFDocument
        # Explicit field list keeps the API stable even if the model later
        # gains additional fields.
        fields = [
            "id",
            "title",
            "pdf_file",
            "uploaded_at",
            "file_size",
            "filename",
        ]
        # These fields are managed by the server and must not be writable by
        # clients.
        read_only_fields = ["uploaded_at", "file_size"]


# ----------------------------------------------------------------------------
# AIConfigSerializer
# ----------------------------------------------------------------------------
class AIConfigSerializer(serializers.ModelSerializer):
    """Serializer for AIConfig model.

    This serializer currently exposes all model fields. If the model contains
    sensitive information (for example API keys or secrets), consider making
    those fields `write_only=True` or removing them from the serialized
    output to avoid leaking credentials to clients.
    """

    class Meta:
        model = AIConfig
        fields = "__all__"
