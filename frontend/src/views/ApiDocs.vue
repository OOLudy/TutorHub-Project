<template>
  <div class="start-page">
    <div class="container">
      <div class="page-header">
        <h1>API 文档</h1>
        <p>下面列出了后端 `myapp` 提供的所有 API（只读视图）。</p>
      </div>

      <div class="upload-section">
        <div class="api-list">
          <div class="api-item" v-for="api in apis" :key="api.path">
            <div class="api-header">
              <h3 class="api-path">{{ api.path }}</h3>
              <div class="method-tags">
                <span v-for="m in api.methods" :key="m" class="method-tag">{{ m }}</span>
              </div>
            </div>
            <p class="api-desc">{{ api.description }}</p>

            <div class="api-details">
              <div class="detail-row"><strong>Backed by:</strong> {{ api.backed_by }}</div>
              <div class="detail-row"><strong>Permissions:</strong> {{ api.permissions }}</div>
              <div v-if="api.request" class="detail-row"><strong>Request:</strong> {{ api.request }}</div>
              <div v-if="api.response" class="detail-row"><strong>Response:</strong> {{ api.response }}</div>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: 'ApiDocs',
  data() {
    return {
      apis: [
        {
          path: '/api/tasks/',
          methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
          description: '任务的 CRUD 接口（ModelViewSet - TaskViewSet）',
          backed_by: 'TaskViewSet (ModelViewSet)',
          permissions: 'AllowAny',
          request: '使用 TaskSerializer 定义的字段',
          response: 'TaskSerializer 返回的对象或对象列表'
        },
        {
          path: '/api/pdfs/',
          methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
          description: 'PDF 文档管理（上传、列出、检索、删除）。POST 需要 multipart/form-data 的 pdf_file。',
          backed_by: 'PDFDocumentViewSet (ModelViewSet)',
          permissions: 'AllowAny',
          request: "POST: form-data (title, pdf_file)。其他字段按 serializer", 
          response: 'PDFDocumentSerializer 返回的对象或对象列表'
        },
        {
          path: '/api/ai-configs/',
          methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
          description: 'AI 配置的管理（可创建、激活、修改、删除）。',
          backed_by: 'AIConfigViewSet (ModelViewSet)',
          permissions: 'AllowAny',
          request: '使用 AIConfigSerializer 定义的字段',
          response: 'AIConfigSerializer 返回的对象或对象列表'
        },
        {
          path: '/api/process/',
          methods: ['POST'],
          description: '处理 PDF 文档（调用 AI 处理器），需要 document_id 和 task_type。',
          backed_by: 'process_document (function)',
          permissions: 'AllowAny',
          request: '{ document_id: int, task_type: string }',
          response: "{ success: True, result: <processor result>, task_type, document_title } 或 错误信息"
        },
        {
          path: '/api/test-connection/',
          methods: ['POST'],
          description: '测试 AI API 连接，传入 api_key 等配置以临时验证。',
          backed_by: 'test_api_connection (function)',
          permissions: 'AllowAny',
          request: "{ api_key: string, base_url?: string, model_name?: string }",
          response: "{ success: True/False, message/error: string }"
        },
        {
          path: '/api/active-config/',
          methods: ['GET'],
          description: '获取当前激活的 AI 配置（is_active=True 的第一项）。',
          backed_by: 'get_active_config (function)',
          permissions: 'AllowAny',
          request: '无',
          response: "{ success: True, config: <AIConfig data> } 或 { success: False, error: '没有激活的配置' }"
        }
      ]
    };
  }
};
</script>

<style scoped>
/* 复用 RealStart.vue 的风格 */
.start-page { min-height: calc(100vh - 60px); padding: 40px 0; background-color: #f5f7fa; }
.container { max-width: 900px; margin: 0 auto; padding: 0 20px; }
.page-header { text-align: center; margin-bottom: 24px; }
.page-header h1 { color: #2c3e50; margin-bottom: 6px; font-size: 2rem; }
.page-header p { color: #7f8c8d; font-size: 1rem; }
.upload-section { background: white; padding: 24px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); }
.api-list { display: flex; flex-direction: column; gap: 12px; }
.api-item { border: 1px solid #eee; padding: 14px; border-radius: 10px; background: #fcfdff; }
.api-header { display:flex; align-items:center; justify-content:space-between; gap:12px; }
.api-path { color: #2c3e50; margin:0; font-size:1.05rem; }
.method-tags { display:flex; gap:8px; }
.method-tag { background:#eaf2ff; color:#2c3e50; padding:4px 8px; border-radius:6px; font-weight:600; font-size:0.85rem; }
.api-desc { color:#586069; margin:8px 0; }
.api-details { display:flex; flex-direction:column; gap:4px; color:#34495e; font-size:0.95rem; }
.detail-row { display:flex; gap:8px; }
@media (max-width: 768px) { .container { padding: 0 12px; } .api-header { flex-direction:column; align-items:flex-start; gap:6px; } }
</style>
