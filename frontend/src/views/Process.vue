<template>
  <div class="process-page">
    <div class="container">
      <div class="page-header">
        <h1>AI Document Processing</h1>
        <p>Select a document and use AI to analyze, summarize, or generate questions</p>
      </div>

      <!-- 文档选择区域 -->
      <div class="document-selection">
        <h2>Select a Document to Process</h2>
        <div v-if="documents.length === 0" class="empty-state">
          <p>No available documents</p>
          <router-link to="/start" class="btn btn-primary">Upload Document</router-link>
        </div>
        <div v-else class="documents-grid">
          <div 
            v-for="doc in documents" 
            :key="doc.id" 
            class="document-card"
            :class="{ 'selected': selectedDocument?.id === doc.id }"
            @click="selectDocument(doc)"
          >
            <div class="document-icon">📄</div>
            <div class="document-info">
              <h4>{{ doc.title }}</h4>
              <p class="document-meta">
                Size: {{ formatFileSize(doc.file_size) }} • 
                Uploaded: {{ formatDate(doc.uploaded_at) }}
              </p>
            </div>
            <div class="select-indicator">
              <div v-if="selectedDocument?.id === doc.id" class="selected-dot"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- 处理选项 -->
      <div v-if="selectedDocument" class="process-options-section">
        <h2>Select processing type</h2>
        <div class="process-options">
          <div class="process-option" @click="processDocument('summary')">
            <div class="option-icon">📋</div>
            <div class="option-content">
              <h4>Summarize</h4>
              <p>Generate a structured summary and key points of the document</p>
            </div>
          </div>
          <div class="process-option" @click="processDocument('analysis')">
            <div class="option-icon">🔍</div>
            <div class="option-content">
              <h4>Detailed Analysis</h4>
              <p>Perform an in-depth analysis and interpretation of the document</p>
            </div>
          </div>
          <div class="process-option" @click="processDocument('questions')">
            <div class="option-icon">📝</div>
            <div class="option-content">
              <h4>Generate Questions</h4>
              <p>Create test questions of various types based on the document content</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 处理结果 -->
      <div v-if="resultData.result" class="result-section">
        <h2>Processing Result</h2>
        <div class="result-header">
          <h3>{{ resultData.document_title }} - {{ getTaskTypeName(resultData.task_type) }}</h3>
          <div class="result-actions">
            <button @click="copyResult" class="btn btn-secondary">Copy Result</button>
            <button @click="downloadResult" class="btn btn-primary">Download Result</button>
            <button @click="clearResult" class="btn btn-outline">Clear Result</button>
          </div>
        </div>
        <div class="result-content">
          <div class="markdown-content" v-html="renderMarkdown(resultData.result)"></div>
        </div>
      </div>

      <!-- 处理中指示器 -->
      <div v-if="isProcessing" class="processing-overlay">
        <div class="processing-indicator">
          <div class="spinner"></div>
          <h3>Processing document</h3>
          <p>Please wait, this may take a while...</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export default {
  name: 'ProcessPage',
  data() {
    return {
      documents: [],
      selectedDocument: null,
      isProcessing: false,
      resultData: {
        document_title: '',
        task_type: '',
        result: ''
      }
    };
  },
  mounted() {
    this.fetchDocuments();
  },
  methods: {
    async fetchDocuments() {
      try {
        const response = await axios.get(`${API_URL}/pdfs/`);
        this.documents = response.data;
      } catch (error) {
        console.error('Failed to fetch documents:', error);
      }
    },
    selectDocument(document) {
      this.selectedDocument = document;
      // 清除之前的结果
      this.clearResult();
    },
    async processDocument(taskType) {
      if (!this.selectedDocument) {
        alert('Please select a document first');
        return;
      }

      this.isProcessing = true;
      
      this.resultData = {
        document_title: this.selectedDocument.title,
        task_type: taskType,
        result: ''
      };
      
      try {
        const response = await axios.post(`${API_URL}/process/`, {
          document_id: this.selectedDocument.id,
          task_type: taskType
        });
        
        if (response.data.success) {
          this.resultData = response.data;
        } else {
          this.resultData.result = 'Processing failed: ' + (response.data.error || 'Unknown error');
        }
      } catch (error) {
        console.error('Failed to process document:', error);
        this.resultData.result = 'Processing failed: ' + (error.response?.data?.error || 'Network error');
      } finally {
        this.isProcessing = false;
      }
    },
    clearResult() {
      this.resultData = {
        document_title: '',
        task_type: '',
        result: ''
      };
    },
    getTaskTypeName(type) {
      const names = {
        'summary': 'Summarize',
        'analysis': 'Detailed Analysis',
        'questions': 'Generate Questions'
      };
      return names[type] || type;
    },
    copyResult() {
      navigator.clipboard.writeText(this.resultData.result).then(() => {
        alert('Result copied to clipboard');
      });
    },
    downloadResult() {
      const blob = new Blob([this.resultData.result], { type: 'text/markdown' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${this.resultData.document_title}_${this.getTaskTypeName(this.resultData.task_type)}.md`;
      a.click();
      URL.revokeObjectURL(url);
    },
    renderMarkdown(text) {
      // 简单的Markdown渲染
      return text
        .replace(/\n/g, '<br>')
        .replace(/## (.*?)(<br>|$)/g, '<h2>$1</h2>')
        .replace(/# (.*?)(<br>|$)/g, '<h1>$1</h1>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/\d\. (.*?)(<br>|$)/g, '<li>$1</li>')
        .replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
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
.process-page {
  min-height: calc(100vh - 60px);
  padding: 40px 0;
  background-color: #f5f7fa;
}

.container {
  max-width: 1000px;
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

.document-selection {
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  margin-bottom: 30px;
}

.document-selection h2 {
  color: #2c3e50;
  margin-bottom: 20px;
  border-bottom: 2px solid #eee;
  padding-bottom: 10px;
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #7f8c8d;
}

.empty-state .btn {
  margin-top: 15px;
}

.documents-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 15px;
}

.document-card {
  display: flex;
  align-items: center;
  padding: 20px;
  background: #f8f9fa;
  border: 2px solid #e9ecef;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
}

.document-card:hover {
  border-color: #3498db;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.document-card.selected {
  border-color: #3498db;
  background: #ebf5fb;
}

.document-icon {
  font-size: 2rem;
  margin-right: 15px;
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

.select-indicator {
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.selected-dot {
  width: 12px;
  height: 12px;
  background: #3498db;
  border-radius: 50%;
}

.process-options-section {
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  margin-bottom: 30px;
}

.process-options-section h2 {
  color: #2c3e50;
  margin-bottom: 20px;
  border-bottom: 2px solid #eee;
  padding-bottom: 10px;
}

.process-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.process-option {
  display: flex;
  align-items: center;
  padding: 25px;
  border: 2px solid #e9ecef;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s;
  background: #f8f9fa;
}

.process-option:hover {
  border-color: #3498db;
  background: #ebf5fb;
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.1);
}

.option-icon {
  font-size: 2.5rem;
  margin-right: 20px;
}

.option-content h4 {
  margin: 0 0 8px 0;
  color: #2c3e50;
  font-size: 1.2rem;
}

.option-content p {
  margin: 0;
  color: #7f8c8d;
  line-height: 1.5;
}

.result-section {
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}

.result-section h2 {
  color: #2c3e50;
  margin-bottom: 20px;
  border-bottom: 2px solid #eee;
  padding-bottom: 10px;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.result-header h3 {
  margin: 0;
  color: #2c3e50;
}

.result-actions {
  display: flex;
  gap: 10px;
}

.result-content {
  line-height: 1.6;
}

.markdown-content {
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.markdown-content h1 {
  color: #2c3e50;
  border-bottom: 2px solid #3498db;
  padding-bottom: 10px;
  margin-top: 0;
}

.markdown-content h2 {
  color: #34495e;
  margin-top: 25px;
  padding-bottom: 8px;
  border-bottom: 1px solid #ddd;
}

.markdown-content ul {
  padding-left: 20px;
  margin: 15px 0;
}

.markdown-content li {
  margin-bottom: 8px;
  line-height: 1.5;
}

.markdown-content strong {
  color: #2c3e50;
}

.markdown-content em {
  color: #7f8c8d;
}

.processing-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.processing-indicator {
  background: white;
  padding: 40px;
  border-radius: 15px;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 2s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.processing-indicator h3 {
  color: #2c3e50;
  margin-bottom: 10px;
}

.processing-indicator p {
  color: #7f8c8d;
  margin: 0;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
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

.btn-outline {
  background: transparent;
  color: #7f8c8d;
  border: 1px solid #ddd;
}

.btn-outline:hover:not(:disabled) {
  background: #f8f9fa;
  color: #2c3e50;
}

@media (max-width: 768px) {
  .container {
    padding: 0 15px;
  }
  
  .documents-grid {
    grid-template-columns: 1fr;
  }
  
  .process-options {
    grid-template-columns: 1fr;
  }
  
  .result-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .result-actions {
    width: 100%;
    justify-content: flex-start;
  }
  
  .document-selection,
  .process-options-section,
  .result-section {
    padding: 20px;
  }
}
</style>