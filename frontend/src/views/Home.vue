<template>
  <div class="home">
    <div class="hero-section">
      <h1>欢迎使用TutorHub-Project</h1>
      <p>тμтoяχαv ряоjест demo</p>
      <router-link to="/start" class="cta-button">开始上传文件</router-link>
    </div>
    
    <div class="features-section">
      <div class="container">
        <h2>功能特性</h2>
        <div class="features-grid">
          <div class="feature-card">
            <h3>文件管理</h3>
            <p>轻松上传、分析、下载所需的文件</p>
          </div>
          <div class="feature-card">
            <h3>AI辅助</h3>
            <p>使用AI快速生成分析报告</p>
          </div>
          <div class="feature-card">
            <h3>自定义输出</h3>
            <p>用户可根据需要自行更改模型和策略</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomePage'
}
</script>

<style scoped>
.home {
  min-height: calc(100vh - 60px);
}

.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-align: center;
  padding: 100px 20px;
}

.hero-section h1 {
  font-size: 3rem;
  margin-bottom: 20px;
}

.hero-section p {
  font-size: 1.2rem;
  margin-bottom: 30px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.cta-button {
  display: inline-block;
  background-color: #fff;
  color: #667eea;
  padding: 12px 30px;
  border-radius: 30px;
  text-decoration: none;
  font-weight: bold;
  transition: transform 0.3s, box-shadow 0.3s;
}

.cta-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}

.features-section {
  padding: 80px 20px;
  background-color: #f8f9fa;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.features-section h2 {
  text-align: center;
  margin-bottom: 50px;
  font-size: 2.5rem;
  color: #2c3e50;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
}

.feature-card {
  background: white;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.05);
  text-align: center;
  transition: transform 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-card h3 {
  color: #2c3e50;
  margin-bottom: 15px;
}

.feature-card p {
  color: #7f8c8d;
  line-height: 1.6;
}

@media (max-width: 768px) {
  .hero-section h1 {
    font-size: 2rem;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
  }
}
</style>