
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os
import uuid

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

def pdf_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f"pdfs/{filename}"

class PDFDocument(models.Model):
    title = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to=pdf_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_size = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title
    
    def filename(self):
        return os.path.basename(self.pdf_file.name)
    
@receiver(post_delete, sender=PDFDocument)
def delete_pdf_file(sender, instance, **kwargs):
    """
    当PDFDocument实例被删除时，同时删除对应的文件
    """
    if instance.pdf_file:
        if os.path.isfile(instance.pdf_file.path):
            os.remove(instance.pdf_file.path)