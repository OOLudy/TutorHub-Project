from rest_framework import serializers
from .models import Task
from .models import PDFDocument
from .models import AIConfig

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class PDFDocumentSerializer(serializers.ModelSerializer):
    filename = serializers.ReadOnlyField()
    
    class Meta:
        model = PDFDocument
        fields = ['id', 'title', 'pdf_file', 'uploaded_at', 'file_size', 'filename']
        read_only_fields = ['uploaded_at', 'file_size']

class AIConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIConfig
        fields = '__all__'