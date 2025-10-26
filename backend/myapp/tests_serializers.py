from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from myapp.models import PDFDocument, Task, AIConfig
from myapp.serializers import (
    PDFDocumentSerializer,
    TaskSerializer,
    AIConfigSerializer,
)
import tempfile
import shutil


class PDFDocumentSerializerTests(TestCase):
    def setUp(self):
        # create a temporary MEDIA_ROOT so uploaded files don't pollute the repo
        self._tmp_media = tempfile.mkdtemp()
        # patch settings.MEDIA_ROOT to point to our temp dir during tests
        from django.conf import settings

        self._orig_media_root = getattr(settings, "MEDIA_ROOT", None)
        settings.MEDIA_ROOT = self._tmp_media

    def tearDown(self):
        # restore original MEDIA_ROOT and remove temp dir
        from django.conf import settings

        if getattr(self, "_orig_media_root", None) is not None:
            settings.MEDIA_ROOT = self._orig_media_root
        else:
            delattr(settings, "MEDIA_ROOT")
        shutil.rmtree(self._tmp_media)

    def test_serialization_outputs_expected_fields(self):
        # create a simple in-memory PDF file
        f = SimpleUploadedFile("doc.pdf", b"%PDF-1.4 sample content")
        pdf = PDFDocument.objects.create(title="T1", pdf_file=f)
        serializer = PDFDocumentSerializer(pdf)
        data = serializer.data
        # basic presence checks
        self.assertIn("id", data)
        self.assertIn("title", data)
        self.assertIn("pdf_file", data)
        # read-only fields should be present in output
        self.assertIn("uploaded_at", data)
        self.assertIn("file_size", data)
        # filename field is defined as ReadOnlyField on the serializer
        self.assertIn("filename", data)

    def test_read_only_fields_are_ignored_on_input(self):
        f = SimpleUploadedFile("doc2.pdf", b"content")
        payload = {
            "title": "T2",
            "pdf_file": f,
            "uploaded_at": "2000-01-01T00:00:00Z",
            "file_size": 99999,
            "filename": "malicious.pdf",
        }
        serializer = PDFDocumentSerializer(data=payload)
        self.assertTrue(serializer.is_valid(), msg=serializer.errors)
        obj = serializer.save()
        # server-managed file_size should not equal the malicious input
        self.assertNotEqual(obj.file_size, 99999)


class TaskSerializerTests(TestCase):
    def test_task_serializer_basic(self):
        t = Task.objects.create(title="task1")
        s = TaskSerializer(t)
        self.assertIn("id", s.data)
        self.assertIn("title", s.data)


class AIConfigSerializerTests(TestCase):
    def test_ai_config_fields(self):
        cfg = AIConfig.objects.create(name="c1", api_key="SECRET123", model_name="gpt-test")
        s = AIConfigSerializer(cfg)
        data = s.data
        # model_name exists on the model; serializer exposes all fields by default
        self.assertIn("model_name", data)
        # api_key will be present unless the serializer was changed to hide it
        self.assertIn("api_key", data)
