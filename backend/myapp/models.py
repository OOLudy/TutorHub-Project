
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os
import json

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

def pdf_upload_path(instance, filename):
    # 使用文档标题作为文件名，保留PDF扩展名
    ext = filename.split('.')[-1]
    return f"pdfs/{instance.title}.{ext}"

class PDFDocument(models.Model):
    title = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to=pdf_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_size = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title
    
    def filename(self):
        return os.path.basename(self.pdf_file.name)
    

## 神必reciever写法
@receiver(post_delete, sender=PDFDocument)
def delete_pdf_file(sender, instance, **kwargs):
    """
    当PDFDocument实例被删除时，同时删除对应的文件
    """
    if instance.pdf_file:
        if os.path.isfile(instance.pdf_file.path):
            os.remove(instance.pdf_file.path)


class AIConfig(models.Model):
    """AI配置模型"""
    name = models.CharField(max_length=100, default='默认配置')
    api_key = models.CharField(max_length=255, blank=True)
    base_url = models.CharField(max_length=255, default='https://api.aihubmix.com/v1')
    model_name = models.CharField(max_length=100, default='gpt-3.5-turbo')
    embedding_model = models.CharField(max_length=100, default='text-embedding-ada-002')
    temperature = models.FloatField(default=0.7)
    max_tokens = models.IntegerField(default=2000)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'AI配置'
        verbose_name_plural = 'AI配置'