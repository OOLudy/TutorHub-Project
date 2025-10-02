from rest_framework import viewsets,status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Task, PDFDocument, AIConfig
from .serializers import TaskSerializer, PDFDocumentSerializer, AIConfigSerializer

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

## API视图给AI模块的
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Task, PDFDocument, AIConfig
from .serializers import TaskSerializer, PDFDocumentSerializer, AIConfigSerializer
import os
from django.conf import settings

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [AllowAny]

class PDFDocumentViewSet(viewsets.ModelViewSet):
    queryset = PDFDocument.objects.all()
    serializer_class = PDFDocumentSerializer
    permission_classes = [AllowAny]
    
    def perform_create(self, serializer):
        pdf_file = self.request.FILES.get('pdf_file')
        file_size = pdf_file.size if pdf_file else 0
        serializer.save(file_size=file_size)

class AIConfigViewSet(viewsets.ModelViewSet):
    queryset = AIConfig.objects.all()
    serializer_class = AIConfigSerializer
    permission_classes = [AllowAny]

@api_view(['POST'])
@permission_classes([AllowAny])
def process_document(request):
    """处理文档API"""
    document_id = request.data.get('document_id')
    task_type = request.data.get('task_type')  # summary, analysis, questions
    
    if not document_id or not task_type:
        return Response({'error': '缺少参数'}, status=400)
    
    try:
        document = PDFDocument.objects.get(id=document_id)
        
        # 构建PDF文件路径
        pdf_path = os.path.join(settings.MEDIA_ROOT, document.pdf_file.name)
        
        if not os.path.exists(pdf_path):
            return Response({'error': 'PDF文件不存在'}, status=404)
        
        # 创建新的处理器实例（确保使用最新配置）
        from .ai_service import get_processor
        processor = get_processor()
        
        # 处理文档
        result = processor.process_document(str(document_id), pdf_path, task_type)
        
        return Response({
            'success': True,
            'result': result,
            'task_type': task_type,
            'document_title': document.title
        })
        
    except PDFDocument.DoesNotExist:
        return Response({'error': '文档不存在'}, status=404)
    except Exception as e:
        return Response({'error': f'处理失败: {str(e)}'}, status=500)

@api_view(['POST'])
@permission_classes([AllowAny])
def test_api_connection(request):
    """测试API连接"""
    from .ai_service import DocumentProcessor
    
    api_key = request.data.get('api_key')
    base_url = request.data.get('base_url')
    model_name = request.data.get('model_name', 'gpt-3.5-turbo')
    
    if not api_key:
        return Response({'success': False, 'error': 'API密钥不能为空'})
    
    try:
        # 创建临时处理器测试连接
        processor = DocumentProcessor()
        
        # 手动设置配置进行测试
        test_config = {
            'api_key': api_key,
            'base_url': base_url,
            'model_name': model_name,
            'embedding_model': 'text-embedding-ada-002',
            'temperature': 0.7,
            'max_tokens': 2000,
            'simulation_mode': False
        }
        
        # 临时替换_get_active_config方法
        original_method = processor._get_active_config
        processor._get_active_config = lambda: test_config
        
        # 测试调用
        test_prompt = "请回复'连接成功'，不要添加其他内容。"
        result = processor.call_llm_api(test_prompt)
        
        # 恢复原始方法
        processor._get_active_config = original_method
        
        if "连接成功" in result:
            return Response({'success': True, 'message': 'API连接测试成功'})
        elif "API错误" in result:
            return Response({'success': False, 'error': result})
        else:
            return Response({'success': False, 'error': f'API返回异常: {result}'})
            
    except Exception as e:
        return Response({'success': False, 'error': f'连接测试失败: {str(e)}'})

@api_view(['GET'])
@permission_classes([AllowAny])
def get_active_config(request):
    """获取当前激活的配置"""
    try:
        active_config = AIConfig.objects.filter(is_active=True).first()
        if active_config:
            serializer = AIConfigSerializer(active_config)
            return Response({'success': True, 'config': serializer.data})
        else:
            return Response({'success': False, 'error': '没有激活的配置'})
    except Exception as e:
        return Response({'success': False, 'error': str(e)})