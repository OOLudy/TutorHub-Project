"""Serializers for the `myapp` Django app.

This module defines DRF ModelSerializers used to convert model instances to
JSON (or other content types) and to validate/deserialize input data.

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
    """

    class Meta:
        model = Task
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

    The `filename` field is declared as ReadOnlyField here
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
    """

    class Meta:
        model = AIConfig
        fields = "__all__"
