<template>
  <div class="cyber-world">
    <!-- 背景粒子效果 -->
    <div class="particles" ref="particlesContainer"></div>
    
    <!-- 3D浮动球体 -->
    <div class="floating-spheres">
      <div class="sphere sphere-1" :style="sphere1Style"></div>
      <div class="sphere sphere-2" :style="sphere2Style"></div>
      <div class="sphere sphere-3" :style="sphere3Style"></div>
    </div>

    <!-- 主内容区域 -->
    <div class="main-content">
      <!-- 霓虹标题 -->
      <div class="neon-title">
        <h1 class="title-text" ref="titleText">CYBER</h1>
        <h1 class="title-text glitch" data-text="REALM">REALM</h1>
      </div>

      <!-- 动态卡片网格 -->
      <div class="card-grid">
        <div 
          v-for="(card, index) in cards" 
          :key="card.id"
          class="cyber-card"
          :style="getCardStyle(index)"
          @mouseenter="hoverCard(index)"
          @mouseleave="resetCard(index)"
        >
          <div class="card-glow"></div>
          <div class="card-content">
            <div class="card-icon">{{ card.icon }}</div>
            <h3 class="card-title">{{ card.title }}</h3>
            <p class="card-desc">{{ card.description }}</p>
            <div class="card-stats">
              <span v-for="stat in card.stats" :key="stat" class="stat-tag">{{ stat }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 交互式控制面板 -->
      <div class="control-panel">
        <div class="panel-section">
          <h4>能量频率</h4>
          <input 
            type="range" 
            v-model="energyFrequency" 
            min="0" 
            max="100"
            class="cyber-slider"
            @input="updateParticles"
          >
        </div>
        
        <div class="panel-section">
          <h4>色彩矩阵</h4>
          <div class="color-buttons">
            <button 
              v-for="color in colorSchemes" 
              :key="color.name"
              class="color-btn"
              :style="{ backgroundColor: color.primary }"
              @click="changeColorScheme(color)"
            ></button>
          </div>
        </div>

        <div class="panel-section">
          <h4>动态模式</h4>
          <div class="mode-buttons">
            <button 
              v-for="mode in modes" 
              :key="mode"
              class="mode-btn"
              :class="{ active: currentMode === mode }"
              @click="changeMode(mode)"
            >
              {{ mode }}
            </button>
          </div>
        </div>
      </div>

      <!-- 浮动信息面板 -->
      <div class="floating-info" :style="infoPanelStyle">
        <div class="info-content">
          <h4>系统状态</h4>
          <div class="status-grid">
            <div class="status-item">
              <span class="status-label">粒子数量</span>
              <span class="status-value">{{ particleCount }}</span>
            </div>
            <div class="status-item">
              <span class="status-label">帧率</span>
              <span class="status-value">{{ fps }} FPS</span>
            </div>
            <div class="status-item">
              <span class="status-label">能量等级</span>
              <span class="status-value">{{ energyLevel }}%</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 音频可视化 -->
      <div class="audio-viz" v-if="showAudioViz">
        <div 
          v-for="(bar, index) in audioBars" 
          :key="index"
          class="viz-bar"
          :style="getBarStyle(bar, index)"
        ></div>
      </div>

      <!-- 时间扭曲效果 -->
      <div class="time-distortion" :style="timeDistortionStyle">
        <div class="distortion-ring ring-1"></div>
        <div class="distortion-ring ring-2"></div>
        <div class="distortion-ring ring-3"></div>
      </div>
    </div>

    <!-- 底部导航 -->
    <div class="cyber-nav">
      <button 
        v-for="nav in navigation" 
        :key="nav.name"
        class="nav-btn"
        @mouseenter="animateNav(nav.name)"
      >
        <span class="nav-icon">{{ nav.icon }}</span>
        <span class="nav-text">{{ nav.name }}</span>
        <div class="nav-underline"></div>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CyberWorld',
  data() {
    return {
      // 粒子系统
      particles: [],
      particleCount: 150,
      
      // 3D球体位置
      sphere1Style: {},
      sphere2Style: {},
      sphere3Style: {},
      
      // 卡片数据
      cards: [
        {
          id: 1,
          icon: '⚡',
          title: '量子计算',
          description: '超越经典计算的极限',
          stats: ['量子比特', '叠加态', '纠缠']
        },
        {
          id: 2,
          icon: '🌌',
          title: '神经接口',
          description: '人机融合的新纪元',
          stats: ['脑机', '意识上传', '数字永生']
        },
        {
          id: 3,
          icon: '🔮',
          title: '时空扭曲',
          description: '操纵时空连续体',
          stats: ['虫洞', '时间旅行', '多维空间']
        },
        {
          id: 4,
          icon: '🤖',
          title: '强人工智能',
          description: '超越人类智能的存在',
          stats: ['机器学习', '深度学习', '意识觉醒']
        }
      ],
      
      // 交互控制
      energyFrequency: 50,
      currentMode: '混沌',
      modes: ['混沌', '秩序', '平衡', '随机'],
      
      // 色彩方案
      currentColorScheme: {
        name: '霓虹蓝',
        primary: '#00f3ff',
        secondary: '#ff00ff',
        accent: '#00ff87'
      },
      colorSchemes: [
        { name: '霓虹蓝', primary: '#00f3ff', secondary: '#ff00ff', accent: '#00ff87' },
        { name: '赛博红', primary: '#ff003c', secondary: '#ff8a00', accent: '#e100ff' },
        { name: '矩阵绿', primary: '#00ff41', secondary: '#00ffcc', accent: '#ccff00' },
        { name: '量子紫', primary: '#8a2be2', secondary: '#da70d6', accent: '#9370db' }
      ],
      
      // 音频可视化
      showAudioViz: true,
      audioBars: [],
      
      // 性能监控
      fps: 60,
      energyLevel: 75,
      
      // 导航
      navigation: [
        { name: '维度', icon: '🌀' },
        { name: '现实', icon: '🌐' },
        { name: '虚空', icon: '⚫' },
        { name: '根源', icon: '⚛️' }
      ],
      
      // 动画状态
      mouseX: 0,
      mouseY: 0,
      time: 0
    }
  },
  
  computed: {
    infoPanelStyle() {
      return {
        transform: `translate(${this.mouseX * 0.02}px, ${this.mouseY * 0.02}px) rotateX(${this.mouseY * 0.1}deg) rotateY(${this.mouseX * 0.1}deg)`
      }
    },
    
    timeDistortionStyle() {
      return {
        opacity: Math.sin(this.time * 0.001) * 0.3 + 0.4,
        transform: `scale(${1 + Math.sin(this.time * 0.002) * 0.1})`
      }
    }
  },
  
  mounted() {
    this.initParticles()
    this.initAudioViz()
    this.startAnimations()
    this.bindEvents()
  },
  
  beforeUnmount() {
    this.stopAnimations()
  },
  
  methods: {
    initParticles() {
      for (let i = 0; i < this.particleCount; i++) {
        this.particles.push({
          x: Math.random() * window.innerWidth,
          y: Math.random() * window.innerHeight,
          vx: (Math.random() - 0.5) * 2,
          vy: (Math.random() - 0.5) * 2,
          size: Math.random() * 3 + 1,
          color: this.getRandomParticleColor()
        })
      }
      this.updateParticles()
    },
    
    initAudioViz() {
      for (let i = 0; i < 64; i++) {
        this.audioBars.push({
          height: Math.random() * 100,
          phase: Math.random() * Math.PI * 2
        })
      }
    },
    
    startAnimations() {
      const animate = () => {
        this.time = performance.now()
        this.animateSpheres()
        this.animateParticles()
        this.animateAudioViz()
        this.updateFPS()
        requestAnimationFrame(animate)
      }
      animate()
    },
    
    stopAnimations() {
      // 清理动画帧
    },
    
    bindEvents() {
      document.addEventListener('mousemove', this.handleMouseMove)
      window.addEventListener('resize', this.handleResize)
    },
    
    handleMouseMove(event) {
      this.mouseX = event.clientX
      this.mouseY = event.clientY
    },
    
    handleResize() {
      // 处理窗口大小变化
    },
    
    animateSpheres() {
      const time = this.time * 0.001
      
      this.sphere1Style = {
        transform: `translateX(${Math.sin(time) * 100}px) translateY(${Math.cos(time * 0.7) * 80}px) rotateX(${time * 30}deg)`
      }
      
      this.sphere2Style = {
        transform: `translateX(${Math.cos(time * 0.5) * 120}px) translateY(${Math.sin(time * 0.9) * 60}px) rotateY(${time * 40}deg)`
      }
      
      this.sphere3Style = {
        transform: `translateX(${Math.sin(time * 0.8) * 80}px) translateY(${Math.cos(time * 1.2) * 100}px) rotateZ(${time * 50}deg)`
      }
    },
    
    animateParticles() {
      const container = this.$refs.particlesContainer
      if (!container) return
      
      let html = ''
      const speed = this.energyFrequency * 0.01
      
      this.particles.forEach(particle => {
        // 更新位置
        particle.x += particle.vx * speed
        particle.y += particle.vy * speed
        
        // 边界检查
        if (particle.x < 0 || particle.x > window.innerWidth) particle.vx *= -1
        if (particle.y < 0 || particle.y > window.innerHeight) particle.vy *= -1
        
        // 鼠标交互
        const dx = this.mouseX - particle.x
        const dy = this.mouseY - particle.y
        const distance = Math.sqrt(dx * dx + dy * dy)
        
        if (distance < 100) {
          const force = (100 - distance) * 0.0005
          particle.vx -= dx * force
          particle.vy -= dy * force
        }
        
        html += `<div class="particle" style="
          left: ${particle.x}px;
          top: ${particle.y}px;
          width: ${particle.size}px;
          height: ${particle.size}px;
          background: ${particle.color};
          opacity: ${0.5 + Math.sin(this.time * 0.001 + particle.x * 0.01) * 0.3};
        "></div>`
      })
      
      container.innerHTML = html
    },
    
    animateAudioViz() {
      const time = this.time * 0.001
      
      this.audioBars.forEach((bar, index) => {
        bar.height = 20 + Math.sin(time * 2 + bar.phase + index * 0.1) * 30 + 
                     Math.sin(time * 3 + index * 0.05) * 20
      })
    },
    
    updateFPS() {
      // 简化的FPS计算
      this.fps = Math.round(1000 / 16)
    },
    
    getCardStyle(index) {
      const time = this.time * 0.001
      const offset = index * 0.5
      
      return {
        transform: `translateY(${Math.sin(time + offset) * 10}px) rotateY(${Math.sin(time * 0.5 + offset) * 5}deg)`,
        '--glow-color': this.currentColorScheme.primary,
        '--card-delay': `${index * 0.1}s`
      }
    },
    
    getBarStyle(bar, index) {
      return {
        height: `${bar.height}%`,
        background: `linear-gradient(to top, ${this.currentColorScheme.primary}, ${this.currentColorScheme.secondary})`,
        animationDelay: `${index * 0.02}s`
      }
    },
    
    hoverCard(index) {
      this.cards[index].hovered = true
    },
    
    resetCard(index) {
      this.cards[index].hovered = false
    },
    
    animateNav(navName) {
      console.log(`Animating navigation: ${navName}`)
    },
    
    updateParticles() {
      this.particleCount = 100 + this.energyFrequency
    },
    
    changeColorScheme(scheme) {
      this.currentColorScheme = scheme
      document.documentElement.style.setProperty('--primary-color', scheme.primary)
      document.documentElement.style.setProperty('--secondary-color', scheme.secondary)
      document.documentElement.style.setProperty('--accent-color', scheme.accent)
    },
    
    changeMode(mode) {
      this.currentMode = mode
    },
    
    getRandomParticleColor() {
      const colors = [
        this.currentColorScheme.primary,
        this.currentColorScheme.secondary,
        this.currentColorScheme.accent,
        '#ffffff'
      ]
      return colors[Math.floor(Math.random() * colors.length)]
    }
  }
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

:root {
  --primary-color: #00f3ff;
  --secondary-color: #ff00ff;
  --accent-color: #00ff87;
  --bg-color: #0a0a0a;
}

.cyber-world {
  min-height: 100vh;
  background: 
    radial-gradient(circle at 20% 80%, rgba(0, 243, 255, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(255, 0, 255, 0.1) 0%, transparent 50%),
    linear-gradient(45deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
  color: white;
  font-family: 'Orbitron', 'Arial', sans-serif;
  overflow: hidden;
  position: relative;
}

/* 粒子背景 */
.particles {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

.particle {
  position: absolute;
  border-radius: 50%;
  pointer-events: none;
  transition: all 0.3s ease;
}

/* 浮动球体 */
.floating-spheres {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 2;
}

.sphere {
  position: absolute;
  width: 200px;
  height: 200px;
  border-radius: 50%;
  filter: blur(40px);
  opacity: 0.3;
  transition: all 2s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.sphere-1 {
  background: radial-gradient(circle, var(--primary-color) 0%, transparent 70%);
  top: 20%;
  left: 10%;
}

.sphere-2 {
  background: radial-gradient(circle, var(--secondary-color) 0%, transparent 70%);
  top: 60%;
  left: 80%;
}

.sphere-3 {
  background: radial-gradient(circle, var(--accent-color) 0%, transparent 70%);
  top: 80%;
  left: 20%;
}

/* 主内容 */
.main-content {
  position: relative;
  z-index: 3;
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

/* 霓虹标题 */
.neon-title {
  text-align: center;
  margin-bottom: 4rem;
  perspective: 1000px;
}

.title-text {
  font-size: 6rem;
  font-weight: 900;
  text-transform: uppercase;
  margin: 0;
  background: linear-gradient(45deg, var(--primary-color), var(--secondary-color), var(--accent-color));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 
    0 0 10px currentColor,
    0 0 20px currentColor,
    0 0 40px currentColor;
  animation: float 6s ease-in-out infinite;
}

.glitch {
  position: relative;
}

.glitch::before,
.glitch::after {
  content: attr(data-text);
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.glitch::before {
  animation: glitch-1 0.5s infinite linear alternate-reverse;
  color: var(--primary-color);
  z-index: -1;
}

.glitch::after {
  animation: glitch-2 0.5s infinite linear alternate-reverse;
  color: var(--secondary-color);
  z-index: -2;
}

/* 卡片网格 */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.cyber-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 2rem;
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(10px);
  transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  animation: cardEntrance 0.6s ease-out;
  animation-fill-mode: both;
  animation-delay: var(--card-delay, 0s);
}

.cyber-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  transition: left 0.5s ease;
}

.cyber-card:hover::before {
  left: 100%;
}

.cyber-card:hover {
  transform: translateY(-10px) scale(1.02);
  border-color: var(--primary-color);
  box-shadow: 
    0 0 30px rgba(0, 243, 255, 0.3),
    inset 0 0 30px rgba(0, 243, 255, 0.1);
}

.card-glow {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at center, var(--glow-color) 0%, transparent 70%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.cyber-card:hover .card-glow {
  opacity: 0.1;
}

.card-content {
  position: relative;
  z-index: 2;
}

.card-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  filter: drop-shadow(0 0 10px currentColor);
}

.card-title {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.card-desc {
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 1.5rem;
  line-height: 1.6;
}

.card-stats {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.stat-tag {
  background: rgba(255, 255, 255, 0.1);
  padding: 0.3rem 0.8rem;
  border-radius: 15px;
  font-size: 0.8rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
}

.stat-tag:hover {
  background: var(--primary-color);
  color: black;
  transform: scale(1.1);
}

/* 控制面板 */
.control-panel {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 20px;
  padding: 2rem;
  margin-bottom: 3rem;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.panel-section h4 {
  margin-bottom: 1rem;
  color: var(--primary-color);
}

.cyber-slider {
  width: 100%;
  height: 4px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
  outline: none;
  -webkit-appearance: none;
}

.cyber-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: var(--primary-color);
  cursor: pointer;
  box-shadow: 0 0 10px var(--primary-color);
}

.color-buttons {
  display: flex;
  gap: 0.5rem;
}

.color-btn {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.3);
  cursor: pointer;
  transition: all 0.3s ease;
}

.color-btn:hover {
  transform: scale(1.2);
  box-shadow: 0 0 15px currentColor;
}

.mode-buttons {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.mode-btn {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.mode-btn.active,
.mode-btn:hover {
  background: var(--primary-color);
  color: black;
  transform: scale(1.05);
}

/* 浮动信息面板 */
.floating-info {
  position: fixed;
  top: 2rem;
  right: 2rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  padding: 1.5rem;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
  z-index: 10;
}

.status-grid {
  display: grid;
  gap: 0.5rem;
}

.status-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.status-label {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
}

.status-value {
  color: var(--primary-color);
  font-weight: bold;
}

/* 音频可视化 */
.audio-viz {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 100px;
  display: flex;
  align-items: end;
  justify-content: center;
  gap: 2px;
  padding: 1rem;
  z-index: 2;
}

.viz-bar {
  width: 8px;
  background: linear-gradient(to top, var(--primary-color), var(--secondary-color));
  border-radius: 4px 4px 0 0;
  animation: audioPulse 1.5s ease-in-out infinite;
  transform-origin: bottom;
}

/* 时间扭曲效果 */
.time-distortion {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  pointer-events: none;
  z-index: 1;
}

.distortion-ring {
  position: absolute;
  border: 2px solid var(--primary-color);
  border-radius: 50%;
  animation: distort 4s linear infinite;
}

.ring-1 {
  width: 200px;
  height: 200px;
  animation-delay: 0s;
}

.ring-2 {
  width: 400px;
  height: 400px;
  animation-delay: -1.33s;
}

.ring-3 {
  width: 600px;
  height: 600px;
  animation-delay: -2.66s;
}

/* 底部导航 */
.cyber-nav {
  position: fixed;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 2rem;
  background: rgba(255, 255, 255, 0.05);
  padding: 1rem 2rem;
  border-radius: 50px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  z-index: 10;
}

.nav-btn {
  background: none;
  border: none;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 25px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.nav-btn:hover {
  color: var(--primary-color);
  transform: translateY(-2px);
}

.nav-underline {
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 2px;
  background: var(--primary-color);
  transition: all 0.3s ease;
  transform: translateX(-50%);
}

.nav-btn:hover .nav-underline {
  width: 80%;
}

/* 动画定义 */
@keyframes float {
  0%, 100% { transform: translateY(0px) rotateX(0deg); }
  50% { transform: translateY(-20px) rotateX(5deg); }
}

@keyframes glitch-1 {
  0% { transform: translate(0); }
  20% { transform: translate(-2px, 2px); }
  40% { transform: translate(-2px, -2px); }
  60% { transform: translate(2px, 2px); }
  80% { transform: translate(2px, -2px); }
  100% { transform: translate(0); }
}

@keyframes glitch-2 {
  0% { transform: translate(0); }
  20% { transform: translate(2px, 2px); }
  40% { transform: translate(2px, -2px); }
  60% { transform: translate(-2px, 2px); }
  80% { transform: translate(-2px, -2px); }
  100% { transform: translate(0); }
}

@keyframes cardEntrance {
  from {
    opacity: 0;
    transform: translateY(50px) scale(0.9);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes audioPulse {
  0%, 100% { transform: scaleY(1); }
  50% { transform: scaleY(1.5); }
}

@keyframes distort {
  0% { transform: translate(-50%, -50%) scale(1) rotate(0deg); opacity: 1; }
  50% { transform: translate(-50%, -50%) scale(1.1) rotate(180deg); opacity: 0.5; }
  100% { transform: translate(-50%, -50%) scale(1) rotate(360deg); opacity: 1; }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .title-text {
    font-size: 3rem;
  }
  
  .card-grid {
    grid-template-columns: 1fr;
  }
  
  .control-panel {
    grid-template-columns: 1fr;
  }
  
  .cyber-nav {
    flex-wrap: wrap;
    justify-content: center;
  }
}

/* 滚动条样式 */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
}

::-webkit-scrollbar-thumb {
  background: var(--primary-color);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: var(--secondary-color);
}
</style>