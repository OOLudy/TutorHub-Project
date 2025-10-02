<template>
  <div class="settings-page">
    <div class="container">
      <div class="page-header">
        <h1>AI设置</h1>
        <p>配置您的AI API密钥和模型参数</p>
      </div>

      <!-- 当前配置状态 -->
      <div class="status-card">
        <div class="status-header">
          <h3>当前配置状态</h3>
          <span :class="['status-badge', connectionStatus.class]">
            {{ connectionStatus.text }}
          </span>
        </div>
        <div v-if="activeConfig" class="config-info">
          <p><strong>配置名称:</strong> {{ activeConfig.name }}</p>
          <p><strong>API端点:</strong> {{ activeConfig.base_url }}</p>
          <p><strong>对话模型:</strong> {{ activeConfig.model_name }}</p>
          <p><strong>嵌入模型:</strong> {{ activeConfig.embedding_model }}</p>
        </div>
        <div v-else class="config-info">
          <p>暂无激活的配置</p>
        </div>
      </div>

      <!-- 配置列表 -->
      <div class="configs-section">
        <div class="section-header">
          <h2>AI配置列表</h2>
          <button @click="showCreateModal = true" class="btn btn-primary">
            + 添加配置
          </button>
        </div>

        <div v-if="configs.length === 0" class="empty-state">
          <p>暂无配置，请添加您的第一个AI配置</p>
        </div>

        <div v-else class="configs-grid">
          <div 
            v-for="config in configs" 
            :key="config.id" 
            class="config-card"
            :class="{ 'active': config.is_active }"
          >
            <div class="config-header">
              <h4>{{ config.name }}</h4>
              <div class="config-actions">
                <button 
                  @click="setActiveConfig(config.id)" 
                  class="btn btn-sm"
                  :class="config.is_active ? 'btn-success' : 'btn-outline'"
                >
                  {{ config.is_active ? '已激活' : '激活' }}
                </button>
                <button @click="editConfig(config)" class="btn btn-sm btn-secondary">编辑</button>
                <button @click="deleteConfig(config.id)" class="btn btn-sm btn-danger">删除</button>
              </div>
            </div>
            <div class="config-details">
              <p><strong>API端点:</strong> {{ config.base_url }}</p>
              <p><strong>对话模型:</strong> {{ config.model_name }}</p>
              <p><strong>嵌入模型:</strong> {{ config.embedding_model }}</p>
              <p><strong>温度:</strong> {{ config.temperature }}</p>
              <p><strong>最大Token:</strong> {{ config.max_tokens }}</p>
              <p><strong>API密钥:</strong> {{ maskApiKey(config.api_key) }}</p>
            </div>
            <div class="config-footer">
              <small>更新于: {{ formatDate(config.updated_at) }}</small>
            </div>
          </div>
        </div>
      </div>

      <!-- 创建/编辑配置模态框 -->
      <div v-if="showCreateModal || showEditModal" class="modal-overlay" @click="closeModal">
        <div class="modal-content large-modal" @click.stop>
          <div class="modal-header">
            <h3>{{ showEditModal ? '编辑配置' : '添加新配置' }}</h3>
            <button class="close-btn" @click="closeModal">&times;</button>
          </div>
          <div class="modal-body">
          <form @submit.prevent="submitConfig">
            <div class="form-grid">
              <div class="form-group">
                <label for="config-name">配置名称 *</label>
                <input
                  id="config-name"
                  v-model="currentConfig.name"
                  type="text"
                  placeholder="例如: OpenAI配置"
                  required
                  class="input"
                >
              </div>

              <div class="form-group">
                <label for="api-key">API密钥 *</label>
                <input
                  id="api-key"
                  v-model="currentConfig.api_key"
                  type="password"
                  placeholder="输入您的API密钥"
                  required
                  class="input"
                >
              </div>

              <div class="form-group">
                <label for="base-url">API基础URL *</label>
                <input
                  id="base-url"
                  v-model="currentConfig.base_url"
                  type="url"
                  placeholder="例如: https://api.openai.com/v1"
                  required
                  class="input"
                >
              </div>

              <div class="form-group">
                <label for="model-name">对话模型</label>
                <input
                  id="model-name"
                  v-model="currentConfig.model_name"
                  type="text"
                  placeholder="例如: gpt-3.5-turbo, gpt-4, claude-3-sonnet"
                  class="input"
                >
                <small>输入您要使用的对话模型名称</small>
              </div>

              <div class="form-group">
                <label for="embedding-model">嵌入模型</label>
                <input
                  id="embedding-model"
                  v-model="currentConfig.embedding_model"
                  type="text"
                  placeholder="例如: text-embedding-ada-002"
                  class="input"
                >
                <small>输入您要使用的嵌入模型名称</small>
              </div>

              <div class="form-group">
                <label for="temperature">温度 (0-1)</label>
                <input
                  id="temperature"
                  v-model="currentConfig.temperature"
                  type="number"
                  min="0"
                  max="1"
                  step="0.1"
                  class="input"
                >
                <small>值越高，回答越随机</small>
              </div>

              <div class="form-group">
                <label for="max-tokens">最大Token数</label>
                <input
                  id="max-tokens"
                  v-model="currentConfig.max_tokens"
                  type="number"
                  min="100"
                  max="4000"
                  class="input"
                >
                <small>控制回答的最大长度</small>
              </div>
            </div>

            <div class="form-actions">
              <button 
                type="button" 
                @click="testConnection" 
                class="btn btn-secondary"
                :disabled="testingConnection"
              >
                <span v-if="testingConnection">测试中...</span>
                <span v-else>测试连接</span>
              </button>
              <div class="action-buttons">
                <button type="button" @click="closeModal" class="btn btn-outline">取消</button>
                <button type="submit" class="btn btn-primary" :disabled="testingConnection">
                  {{ showEditModal ? '更新配置' : '创建配置' }}
                </button>
              </div>
            </div>

            <div v-if="testResult" class="test-result">
              <p :class="testResult.success ? 'success' : 'error'">
                {{ testResult.message }}
              </p>
            </div>
          </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export default {
  name: 'SettingsPage',
  data() {
    return {
      configs: [],
      activeConfig: null,
      showCreateModal: false,
      showEditModal: false,
      testingConnection: false,
      testResult: null,
      currentConfig: {
        name: '',
        api_key: '',
        base_url: 'https://api.openai.com/v1',
        model_name: 'gpt-3.5-turbo',
        embedding_model: 'text-embedding-ada-002',
        temperature: 0.7,
        max_tokens: 2000,
        is_active: false
      }
    };
  },
  computed: {
    connectionStatus() {
      if (this.activeConfig) {
        return { class: 'success', text: '已连接' };
      } else {
        return { class: 'error', text: '未配置' };
      }
    }
  },
  mounted() {
    this.fetchConfigs();
    this.fetchActiveConfig();
  },
  methods: {
    async fetchConfigs() {
      try {
        const response = await axios.get(`${API_URL}/ai-configs/`);
        this.configs = response.data;
      } catch (error) {
        console.error('获取配置列表失败:', error);
      }
    },
    async fetchActiveConfig() {
      try {
        const response = await axios.get(`${API_URL}/active-config/`);
        if (response.data.success) {
          this.activeConfig = response.data.config;
        }
      } catch (error) {
        console.error('获取激活配置失败:', error);
      }
    },
    async setActiveConfig(configId) {
      try {
        // 先取消所有激活状态
        for (const config of this.configs) {
          if (config.is_active) {
            await axios.patch(`${API_URL}/ai-configs/${config.id}/`, { is_active: false });
          }
        }
        
        // 设置新的激活配置
        await axios.patch(`${API_URL}/ai-configs/${configId}/`, { is_active: true });
        
        this.fetchConfigs();
        this.fetchActiveConfig();
        alert('配置激活成功');
      } catch (error) {
        console.error('激活配置失败:', error);
        alert('激活配置失败');
      }
    },
    async testConnection() {
      if (!this.currentConfig.api_key || !this.currentConfig.base_url) {
        alert('请填写API密钥和基础URL');
        return;
      }

      this.testingConnection = true;
      this.testResult = null;

      try {
        const response = await axios.post(`${API_URL}/test-connection/`, {
          api_key: this.currentConfig.api_key,
          base_url: this.currentConfig.base_url,
          model_name: this.currentConfig.model_name
        });

        this.testResult = {
          success: response.data.success,
          message: response.data.success ? response.data.message : response.data.error
        };
      } catch (error) {
        this.testResult = {
          success: false,
          message: '测试连接失败: ' + (error.response?.data?.error || error.message)
        };
      } finally {
        this.testingConnection = false;
      }
    },
    async submitConfig() {
      try {
        if (this.showEditModal) {
          // 更新配置
          await axios.put(`${API_URL}/ai-configs/${this.currentConfig.id}/`, this.currentConfig);
          alert('配置更新成功');
        } else {
          // 创建新配置
          await axios.post(`${API_URL}/ai-configs/`, this.currentConfig);
          alert('配置创建成功');
        }

        this.closeModal();
        this.fetchConfigs();
        this.fetchActiveConfig();
      } catch (error) {
        console.error('保存配置失败:', error);
        alert('保存配置失败');
      }
    },
    editConfig(config) {
      this.currentConfig = { ...config };
      this.showEditModal = true;
    },
    async deleteConfig(configId) {
      if (!confirm('确定要删除这个配置吗？')) {
        return;
      }

      try {
        await axios.delete(`${API_URL}/ai-configs/${configId}/`);
        this.fetchConfigs();
        this.fetchActiveConfig();
        alert('配置删除成功');
      } catch (error) {
        console.error('删除配置失败:', error);
        alert('删除配置失败');
      }
    },
    closeModal() {
      this.showCreateModal = false;
      this.showEditModal = false;
      this.testResult = null;
      this.resetCurrentConfig();
    },
    resetCurrentConfig() {
      this.currentConfig = {
        name: '',
        api_key: '',
        base_url: 'https://api.openai.com/v1',
        model_name: 'gpt-3.5-turbo',
        embedding_model: 'text-embedding-ada-002',
        temperature: 0.7,
        max_tokens: 2000,
        is_active: false
      };
    },
    maskApiKey(apiKey) {
      if (!apiKey) return '未设置';
      return apiKey.substring(0, 8) + '***' + apiKey.substring(apiKey.length - 4);
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleString('zh-CN');
    }
  }
};
</script>

<style scoped>
.settings-page {
  min-height: calc(100vh - 60px);
  padding: 40px 0;
  background-color: #f5f7fa;
}

.container {
  max-width: 1200px;
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

.status-card {
  background: white;
  padding: 25px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.08);
  margin-bottom: 30px;
}

.status-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.status-header h3 {
  margin: 0;
  color: #2c3e50;
}

.status-badge {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 600;
}

.status-badge.success {
  background: #d4edda;
  color: #155724;
}

.status-badge.error {
  background: #f8d7da;
  color: #721c24;
}

.config-info p {
  margin: 5px 0;
  color: #555;
}

.configs-section {
  background: white;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.08);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.section-header h2 {
  color: #2c3e50;
  margin: 0;
}

.configs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.config-card {
  border: 2px solid #e9ecef;
  border-radius: 10px;
  padding: 20px;
  background: #f8f9fa;
  transition: all 0.3s;
}

.config-card.active {
  border-color: #28a745;
  background: #f0fff4;
}

.config-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
}

.config-header h4 {
  margin: 0;
  color: #2c3e50;
  flex: 1;
}

.config-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.config-details {
  margin-bottom: 15px;
}

.config-details p {
  margin: 5px 0;
  font-size: 0.9rem;
  color: #555;
}

.config-footer {
  border-top: 1px solid #e9ecef;
  padding-top: 10px;
}

.config-footer small {
  color: #7f8c8d;
}

/* 模态框样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.large-modal {
  max-width: 700px;
  width: 95%;
  max-height: 90vh;
}

.modal-content {
  background: white;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
}

.modal-header {
  padding: 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  color: #2c3e50;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #7f8c8d;
}

.modal-body {
  padding: 20px;
  overflow-y: auto;
  flex: 1;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 8px;
  font-weight: 600;
  color: #2c3e50;
}

.form-group small {
  margin-top: 5px;
  color: #7f8c8d;
  font-size: 0.8rem;
}

.form-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 25px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.action-buttons {
  display: flex;
  gap: 10px;
}

.test-result {
  margin-top: 15px;
  padding: 10px;
  border-radius: 5px;
}

.test-result .success {
  color: #155724;
  background: #d4edda;
  padding: 10px;
  border-radius: 5px;
}

.test-result .error {
  color: #721c24;
  background: #f8d7da;
  padding: 10px;
  border-radius: 5px;
}

/* 按钮样式 */
.btn {
  padding: 10px 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s;
  text-decoration: none;
  display: inline-block;
  text-align: center;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-sm {
  padding: 6px 12px;
  font-size: 0.8rem;
}

.btn-primary {
  background: #3498db;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #2980b9;
}

.btn-secondary {
  background: #95a5a6;
  color: white;
}

.btn-secondary:hover:not(:disabled) {
  background: #7f8c8d;
}

.btn-success {
  background: #28a745;
  color: white;
}

.btn-danger {
  background: #e74c3c;
  color: white;
}

.btn-danger:hover:not(:disabled) {
  background: #c0392b;
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

.input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  transition: border-color 0.3s;
}

.input:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #7f8c8d;
}

@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .configs-grid {
    grid-template-columns: 1fr;
  }
  
  .config-header {
    flex-direction: column;
    gap: 10px;
  }
  
  .config-actions {
    width: 100%;
    justify-content: flex-start;
  }
  
  .form-actions {
    flex-direction: column;
    gap: 15px;
    align-items: stretch;
  }
  
  .action-buttons {
    justify-content: flex-end;
  }
}
</style>