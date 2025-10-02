from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, PDFDocumentViewSet, process_document, AIConfigViewSet, test_api_connection, get_active_config


router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'pdfs', PDFDocumentViewSet)  # 使用正确的类名
router.register(r'ai-configs', AIConfigViewSet) # 新增AI配置路由

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/process/', process_document, name='process_document'),  
     path('api/test-connection/', test_api_connection, name='test_connection'),  
    path('api/active-config/', get_active_config, name='active_config'),  
]