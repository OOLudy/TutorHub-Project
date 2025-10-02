from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Task, PDFDocument
from .serializers import TaskSerializer, PDFDocumentSerializer

# TaskViewSet 保持不变
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

# 修改 PDFDocumentViewSet
class PDFDocumentViewSet(viewsets.ModelViewSet):
    queryset = PDFDocument.objects.all()
    serializer_class = PDFDocumentSerializer
    permission_classes = [AllowAny]  # 允许所有人访问
    
    def perform_create(self, serializer):
        pdf_file = self.request.FILES.get('pdf_file')
        file_size = pdf_file.size if pdf_file else 0
        serializer.save(file_size=file_size)
    
    # 移除 my_documents 自定义action，使用默认的list