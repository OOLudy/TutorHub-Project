<template>
  <div class="start-page">
    <div class="container">
      <div class="page-header">
        <h1>Upload PDF Document</h1>
        <p>Upload your PDF document and we'll handle the subsequent analysis</p>
      </div>

      <!-- 上传区域 -->
      <div class="upload-section">
        <div 
          class="upload-area"
          :class="{ 'drag-over': isDragOver, 'has-file': selectedFile }"
          @drop="onDrop"
          @dragover="onDragOver"
          @dragleave="onDragLeave"
          @click="triggerFileInput"
        >
          <div class="upload-content">
            <div class="upload-icon">
              📄
            </div>
            <h3 v-if="!selectedFile">Click or drag a PDF file here to select</h3>
            <div v-else class="file-info">
              <h3>{{ selectedFile.name }}</h3>
              <p>Size: {{ formatFileSize(selectedFile.size) }}</p>
            </div>
            <p class="upload-hint">PDF only, max 10MB</p>
          </div>
          <input
            ref="fileInput"
            type="file"
            accept=".pdf"
            @change="onFileSelect"
            style="display: none"
          >
        </div>

        <!-- 文件标题输入 -->
        <div v-if="selectedFile" class="title-input">
          <label for="document-title">Document Title</label>
          <input
            id="document-title"
            v-model="documentTitle"
            type="text"
            placeholder="Enter document title"
            class="input"
          >
        </div>

        <!-- 操作按钮 -->
        <div class="action-buttons">
          <button 
            v-if="selectedFile" 
            @click="clearSelection" 
            class="btn btn-secondary"
            :disabled="isUploading"
          >
            Re-select
          </button>
          <button 
            v-if="selectedFile" 
            @click="uploadPDF" 
            class="btn btn-primary"
            :disabled="!documentTitle || isUploading"
          >
            <span v-if="isUploading">Uploading...</span>
            <span v-else>Upload Document</span>
          </button>
        </div>
      </div>

      <!-- 上传历史 -->
      <div v-if="documents.length > 0" class="documents-section">
        <h2>Uploaded Documents</h2>
        <div class="documents-grid">
          <div 
            v-for="doc in documents" 
            :key="doc.id" 
            class="document-card"
          >
            <div class="document-icon">📄</div>
            <div class="document-info">
              <h4>{{ doc.title }}</h4>
              <p class="document-meta">
                Size: {{ formatFileSize(doc.file_size) }} • 
                Uploaded: {{ formatDate(doc.uploaded_at) }}
              </p>
            </div>
            <div class="document-actions">
              <button @click="viewDocument(doc)" class="btn btn-sm btn-secondary">View</button>
              <router-link :to="'/process'" class="btn btn-sm btn-process">Process</router-link>
              <!--你不准删除！
              <button @click="deleteDocument(doc.id)" class="btn btn-sm btn-danger">删除</button>
              -->
            </div>
          </div>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-else class="empty-state">
        <p>No uploaded documents yet</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export default {
  name: 'StartPage',
  data() {
    return {
      selectedFile: null,
      documentTitle: '',
      isDragOver: false,
      isUploading: false,
      documents: []
    };
  },
  mounted() {
    this.fetchDocuments();
  },
  methods: {
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
    onFileSelect(event) {
      const file = event.target.files[0];
      if (file) {
        this.handleFileSelection(file);
      }
    },
    onDrop(event) {
      event.preventDefault();
      this.isDragOver = false;
      
      const files = event.dataTransfer.files;
      if (files.length > 0) {
        this.handleFileSelection(files[0]);
      }
    },
    onDragOver(event) {
      event.preventDefault();
      this.isDragOver = true;
    },
    onDragLeave() {
      this.isDragOver = false;
    },
    handleFileSelection(file) {
      // 验证文件类型
      if (file.type !== 'application/pdf') {
        alert('Please select a PDF file');
        return;
      }
      
      // 验证文件大小 (10MB)
      if (file.size > 10 * 1024 * 1024) {
        alert('File size must not exceed 10MB');
        return;
      }
      
      this.selectedFile = file;
      // 自动生成标题（去除扩展名）
      this.documentTitle = file.name.replace(/\.pdf$/i, '');
    },
    clearSelection() {
      this.selectedFile = null;
      this.documentTitle = '';
      this.$refs.fileInput.value = '';
    },
    async uploadPDF() {
      if (!this.selectedFile || !this.documentTitle) {
        alert('Please select a file and enter a title');
        return;
      }

      this.isUploading = true;

      try {
        const formData = new FormData();
        formData.append('title', this.documentTitle);
        formData.append('pdf_file', this.selectedFile);

        const response = await axios.post(`${API_URL}/pdfs/`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });

        // 上传成功
        this.documents.unshift(response.data);
        this.clearSelection();
  alert('Document uploaded successfully!');

      } catch (error) {
        console.error('Upload failed:', error);
        alert('Upload failed, please try again');
      } finally {
        this.isUploading = false;
      }
    },
    async fetchDocuments() {
      try {
        const response = await axios.get(`${API_URL}/pdfs/`);
        this.documents = response.data;
      } catch (error) {
        console.error('Failed to fetch documents:', error);
      }
    },
    async deleteDocument(documentId) {
      if (!confirm('Are you sure you want to delete this document?')) {
        return;
      }

      try {
        await axios.delete(`${API_URL}/pdfs/${documentId}/`);
        this.documents = this.documents.filter(doc => doc.id !== documentId);
        alert('Document deleted successfully');
      } catch (error) {
        console.error('Delete failed:', error);
        alert('Delete failed, please try again');
      }
    },
    viewDocument(doc) {
      // Open PDF in a new window
      window.open(doc.pdf_file, '_blank');
    },
    formatFileSize(bytes) {
      if (bytes === 0) return '0 Bytes';
      const k = 1024;
      const sizes = ['Bytes', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString('en-US');
    }
  }
};
</script>

<style scoped>
/* 样式保持不变，只添加处理按钮样式 */
.btn-process {
  background: #9b59b6;
  color: white;
  text-decoration: none;
  display: inline-block;
  text-align: center;
}

.btn-process:hover {
  background: #8e44ad;
  color: white;
}

/* 其他样式与之前相同 */
.start-page {
  min-height: calc(100vh - 60px);
  padding: 40px 0;
  background-color: #f5f7fa;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 20px;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
}

.page-header h1 {
  color: #2c3e50;
  margin-bottom: 10px;
  font-size: 2.5rem;
}

.page-header p {
  color: #7f8c8d;
  font-size: 1.1rem;
}

.upload-section {
  background: white;
  padding: 40px;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  margin-bottom: 40px;
}

.upload-area {
  border: 3px dashed #ddd;
  border-radius: 10px;
  padding: 60px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background: #fafbfc;
}

.upload-area:hover {
  border-color: #3498db;
  background: #f8fafc;
}

.upload-area.drag-over {
  border-color: #3498db;
  background: #ebf5fb;
}

.upload-area.has-file {
  border-color: #27ae60;
  background: #eafaf1;
}

.upload-content {
  pointer-events: none;
}

.upload-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.upload-area h3 {
  color: #2c3e50;
  margin-bottom: 10px;
}

.upload-hint {
  color: #7f8c8d;
  margin-top: 10px;
}

.file-info h3 {
  color: #27ae60;
}

.file-info p {
  color: #7f8c8d;
  margin-top: 5px;
}

.title-input {
  margin-top: 30px;
}

.title-input label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #2c3e50;
}

.action-buttons {
  margin-top: 30px;
  display: flex;
  gap: 15px;
  justify-content: center;
}

.documents-section {
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}

.documents-section h2 {
  color: #2c3e50;
  margin-bottom: 20px;
  border-bottom: 2px solid #eee;
  padding-bottom: 10px;
}

.documents-grid {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.document-card {
  display: flex;
  align-items: center;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 10px;
  border: 1px solid #e9ecef;
  transition: transform 0.2s;
}

.document-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.05);
}

.document-icon {
  font-size: 2rem;
  margin-right: 20px;
}

.document-info {
  flex: 1;
}

.document-info h4 {
  color: #2c3e50;
  margin-bottom: 5px;
}

.document-meta {
  color: #7f8c8d;
  font-size: 0.9rem;
}

.document-actions {
  display: flex;
  gap: 10px;
}

.btn-sm {
  padding: 6px 12px;
  font-size: 0.875rem;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #7f8c8d;
}

.input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 16px;
  transition: border-color 0.3s;
}

.input:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.3s;
  text-decoration: none;
  display: inline-block;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background: #3498db;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #2980b9;
  transform: translateY(-1px);
}

.btn-secondary {
  background: #95a5a6;
  color: white;
}

.btn-secondary:hover:not(:disabled) {
  background: #7f8c8d;
}

.btn-danger {
  background: #e74c3c;
  color: white;
}

.btn-danger:hover:not(:disabled) {
  background: #c0392b;
}

@media (max-width: 768px) {
  .upload-section,
  .documents-section {
    padding: 20px;
  }
  
  .upload-area {
    padding: 40px 20px;
  }
  
  .document-card {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .document-actions {
    width: 100%;
    justify-content: flex-end;
  }
  
  .action-buttons {
    flex-direction: column;
  }
}
</style>