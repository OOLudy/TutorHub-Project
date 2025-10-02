<template>
  <div class="task-page">
    <div class="container">
      <h1>任务管理系统</h1>
      
      <!-- 添加任务表单 -->
      <div class="task-form">
        <h2>添加新任务</h2>
        <input v-model="newTask.title" placeholder="任务标题" class="input">
        <textarea v-model="newTask.description" placeholder="任务描述" class="textarea"></textarea>
        <button @click="addTask" class="btn btn-primary">添加任务</button>
      </div>

      <!-- 任务列表 -->
      <div class="task-list">
        <h2>任务列表</h2>
        <div v-if="tasks.length === 0" class="empty-state">
          <p>暂无任务，请添加新任务</p>
        </div>
        <div v-else>
          <div v-for="task in tasks" :key="task.id" class="task-item">
            <div class="task-info">
              <h3 :class="{ completed: task.completed }">{{ task.title }}</h3>
              <p>{{ task.description }}</p>
              <small>创建时间: {{ formatDate(task.created_at) }}</small>
            </div>
            <div class="task-actions">
              <button @click="toggleTask(task)" class="btn btn-secondary">
                {{ task.completed ? '标记未完成' : '标记完成' }}
              </button>
              <button @click="deleteTask(task.id)" class="btn btn-danger">删除</button>
            </div>
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
  name: 'TaskPage',  // 确保这个也是多单词的
  data() {
    return {
      tasks: [],
      newTask: {
        title: '',
        description: '',
        completed: false
      }
    };
  },
  mounted() {
    this.fetchTasks();
  },
  methods: {
    async fetchTasks() {
      try {
        const response = await axios.get(`${API_URL}/tasks/`);
        this.tasks = response.data;
      } catch (error) {
        console.error('获取任务失败:', error);
      }
    },
    async addTask() {
      if (!this.newTask.title.trim()) {
        alert('请输入任务标题');
        return;
      }
      
      try {
        const response = await axios.post(`${API_URL}/tasks/`, this.newTask);
        this.tasks.push(response.data);
        this.newTask = { title: '', description: '', completed: false };
      } catch (error) {
        console.error('添加任务失败:', error);
      }
    },
    async toggleTask(task) {
      try {
        const updatedTask = { ...task, completed: !task.completed };
        const response = await axios.put(`${API_URL}/tasks/${task.id}/`, updatedTask);
        const index = this.tasks.findIndex(t => t.id === task.id);
        this.tasks.splice(index, 1, response.data);
      } catch (error) {
        console.error('更新任务失败:', error);
      }
    },
    async deleteTask(taskId) {
      if (!confirm('确定要删除这个任务吗？')) {
        return;
      }
      
      try {
        await axios.delete(`${API_URL}/tasks/${taskId}/`);
        this.tasks = this.tasks.filter(task => task.id !== taskId);
      } catch (error) {
        console.error('删除任务失败:', error);
      }
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleString();
    }
  }
};
</script>

<style scoped>
.task-page {
  min-height: calc(100vh - 60px);
  padding: 20px 0;
  background-color: #f5f7fa;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 20px;
}

.task-form {
  background: white;
  padding: 25px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  margin-bottom: 30px;
}

.task-form h2, .task-list h2 {
  color: #2c3e50;
  margin-bottom: 20px;
  border-bottom: 2px solid #eee;
  padding-bottom: 10px;
}

.input, .textarea {
  width: 100%;
  padding: 12px;
  margin: 8px 0;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  box-sizing: border-box;
}

.textarea {
  min-height: 100px;
  resize: vertical;
}

.btn {
  padding: 10px 20px;
  margin: 5px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

.btn-primary {
  background: #3498db;
  color: white;
}

.btn-primary:hover {
  background: #2980b9;
}

.btn-secondary {
  background: #95a5a6;
  color: white;
}

.btn-secondary:hover {
  background: #7f8c8d;
}

.btn-danger {
  background: #e74c3c;
  color: white;
}

.btn-danger:hover {
  background: #c0392b;
}

.task-list {
  background: white;
  padding: 25px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #7f8c8d;
}

.task-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  margin: 15px 0;
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  transition: transform 0.2s;
}

.task-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.05);
}

.task-info h3.completed {
  text-decoration: line-through;
  color: #95a5a6;
}

.task-info p {
  margin: 10px 0;
  color: #555;
}

.task-info small {
  color: #888;
}

.task-actions {
  display: flex;
  gap: 10px;
}

@media (max-width: 768px) {
  .task-item {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .task-actions {
    margin-top: 15px;
    width: 100%;
    justify-content: flex-end;
  }
}
</style>