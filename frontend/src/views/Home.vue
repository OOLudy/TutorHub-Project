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
  font-family: 'Inter', 'Noto Sans SC', sans-serif;
}

/* ===== Hero Section ===== */
.hero-section {
  background: linear-gradient(135deg, #5B6BF2 0%, #748DF5 100%);
  color: #ffffff;
  text-align: center;
  padding: 100px 20px;
  position: relative;
  overflow: hidden;
}

.hero-section::after {
  content: "";
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 80% 20%, rgba(255,255,255,0.15), transparent 60%);
  pointer-events: none;
}

.hero-section h1 {
  font-size: 3rem;
  margin-bottom: 20px;
  font-weight: 700;
  text-shadow: 0 2px 6px rgba(0,0,0,0.15);
}

.hero-section p {
  font-size: 1.2rem;
  margin-bottom: 30px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
  color: #e2e6ff;
}

.cta-button {
  display: inline-block;
  background-color: #ffffff;
  color: #4752C4;
  padding: 12px 30px;
  border-radius: 30px;
  text-decoration: none;
  font-weight: bold;
  transition: transform 0.3s, box-shadow 0.3s, background-color 0.3s;
  box-shadow: 0 6px 12px rgba(0,0,0,0.15);
}

.cta-button:hover {
  background-color: #8EA7FF;
  color: #ffffff;
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(88,101,242,0.3);
}

/* ===== Features Section ===== */
.features-section {
  padding: 100px 20px 120px;
  background-color: #f5f7ff;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.features-section h2 {
  text-align: center;
  margin-bottom: 50px;
  font-size: 2.5rem;
  color: #4752C4;
  font-weight: 600;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
}

.feature-card {
  background: #ffffff;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 8px 25px rgba(88,101,242,0.1);
  text-align: center;
  transition: transform 0.3s, box-shadow 0.3s;
  border: 1px solid rgba(142, 167, 255, 0.2);
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(88,101,242,0.25);
}

.feature-card h3 {
  color: #5865F2;
  margin-bottom: 15px;
  font-size: 1.3rem;
  font-weight: 600;
}

.feature-card p {
  color: #6b7280;
  line-height: 1.6;
  font-size: 1rem;
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
