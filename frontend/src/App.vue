<template>
  <div id="app">
    <div class="container">
      <h1>任务管理系统</h1>
      
      <!-- 添加任务表单 -->
      <div class="task-form">
        <input v-model="newTask.title" placeholder="任务标题" class="input">
        <textarea v-model="newTask.description" placeholder="任务描述" class="textarea"></textarea>
        <button @click="addTask" class="btn btn-primary">添加任务</button>
      </div>

      <!-- 任务列表 -->
      <div class="task-list">
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
</template>

<script>
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export default {
  name: 'App',
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
      if (!this.newTask.title.trim()) return;
      
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

<style>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.task-form {
  margin-bottom: 30px;
  padding: 20px;
  background: #f5f5f5;
  border-radius: 8px;
}

.input, .textarea {
  width: 100%;
  padding: 10px;
  margin: 5px 0;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.btn {
  padding: 10px 15px;
  margin: 5px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-danger {
  background: #dc3545;
  color: white;
}

.task-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  margin: 10px 0;
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.task-info h3.completed {
  text-decoration: line-through;
  color: #888;
}

.task-actions {
  display: flex;
  gap: 10px;
}
</style>