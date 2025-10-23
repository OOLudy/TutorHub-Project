<template>
  <nav class="navbar">
    <div class="nav-container">
      <div class="nav-logo">
        <router-link to="/">TestHelper-Project</router-link>
      </div>
      <ul class="nav-menu">
        <li class="nav-item">
          <router-link to="/" class="nav-link">Home</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/start" class="nav-link">Start</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/process" class="nav-link">AI Processing</router-link>
        </li>

        <li class="nav-item">
          <router-link to="/task" class="nav-link">NOT IN USE</router-link>
        </li>

        <li class="nav-item">
        <router-link to="/settings" class="nav-link">Settings</router-link>
        </li>
        
        <li class="nav-item">
          <router-link to="/checkapi" class="nav-link">API VIEW</router-link> 
        </li>
        <!--这个可以打开API用法，看看好吗-->

        <!-- Add more navigation items as needed -->

      </ul>
      <div class="nav-toggle" @click="toggleMenu">
        <span class="bar"></span>
        <span class="bar"></span>
        <span class="bar"></span>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'NavBar',
  methods: {
    toggleMenu() {
      const navMenu = document.querySelector('.nav-menu')
      navMenu.classList.toggle('active')
    }
  }
}
</script>


<style scoped>
.navbar {
  background: linear-gradient(90deg, #4F5BD5, #5865F2);
  padding: 0 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.nav-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  height: 60px;
}

.nav-logo a {
  color: #fff;
  text-decoration: none;
  font-size: 1.5rem;
  font-weight: bold;
  letter-spacing: 0.5px;
}

.nav-menu {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
}

.nav-item {
  margin-left: 20px;
}

.nav-link {
  color: #fff;
  text-decoration: none;
  padding: 10px 15px;
  border-radius: 6px;
  transition: background-color 0.3s, box-shadow 0.3s;
  font-weight: 500;
}

.nav-link:hover, .nav-link.router-link-active {
  background-color: rgba(255,255,255,0.15);
  box-shadow: 0 3px 8px rgba(0,0,0,0.1);
}

.nav-toggle {
  display: none;
  flex-direction: column;
  cursor: pointer;
}

.bar {
  width: 25px;
  height: 3px;
  background-color: #fff;
  margin: 3px 0;
  transition: 0.3s;
}

@media screen and (max-width: 768px) {
  .nav-menu {
    position: fixed;
    left: -100%;
    top: 60px;
    flex-direction: column;
    background-color: #5865F2;
    width: 100%;
    text-align: center;
    transition: 0.3s;
    box-shadow: 0 10px 27px rgba(0,0,0,0.1);
  }

  .nav-menu.active {
    left: 0;
  }

  .nav-item {
    margin: 15px 0;
  }

  .nav-toggle {
    display: flex;
  }
}
</style>
