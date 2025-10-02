from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, PDFDocumentViewSet  # 确保导入正确的类名

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'pdfs', PDFDocumentViewSet)  # 使用正确的类名

urlpatterns = [
    path('api/', include(router.urls)),
]