<template>
  <nav class="navigation">
    <div class="logo">
      <img src="@/assets/logo.png" alt="DesertBloom AI">
      <h1>DesertBloom AI</h1>
    </div>
    
    <ul class="nav-links">
      <li>
        <router-link to="/" class="nav-link">
          <i class="fas fa-home"></i>
          <span>Dashboard</span>
        </router-link>
      </li>
      <li>
        <router-link to="/plants" class="nav-link">
          <i class="fas fa-seedling"></i>
          <span>Plants</span>
        </router-link>
      </li>
      <li>
        <router-link to="/sensors" class="nav-link">
          <i class="fas fa-microchip"></i>
          <span>Sensors</span>
        </router-link>
      </li>
      <li>
        <router-link to="/irrigation" class="nav-link">
          <i class="fas fa-tint"></i>
          <span>Irrigation</span>
        </router-link>
      </li>
      <li>
        <router-link to="/analytics" class="nav-link">
          <i class="fas fa-chart-line"></i>
          <span>Analytics</span>
        </router-link>
      </li>
      <li>
        <router-link to="/robotics" class="nav-link">
          <i class="fas fa-robot"></i>
          <span>Robotics</span>
        </router-link>
      </li>
      <li>
        <router-link to="/path-planning" class="nav-link">
          <i class="fas fa-route"></i>
          <span>Path Planning</span>
        </router-link>
      </li>
      <li>
        <router-link to="/prototype" class="nav-link">
          <i class="fas fa-pencil-ruler"></i>
          <span>Prototype</span>
        </router-link>
      </li>
    </ul>
    
    <div class="user-info">
      <div class="user-avatar">
        <i class="fas fa-user"></i>
      </div>
      <div class="user-details">
        <span class="username">DesertBloomAI</span>
        <span class="role">{{ role }}</span>
      </div>
    </div>
  </nav>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'Navigation'
})
</script>

<style scoped>
.navigation {
  background-color: var(--paper-color);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);
  padding: 1rem;
  height: 100%;
}

.logo {
  display: flex;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--background-color);
}

.logo img {
  width: 40px;
  height: 40px;
  margin-right: 0.75rem;
}

.logo h1 {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--primary-color);
}

.nav-links {
  list-style: none;
}

.nav-link {
  display: flex;
  align-items: center;
  padding: 0.75rem;
  color: var(--text-color);
  text-decoration: none;
  border-radius: var(--border-radius);
  transition: var(--transition);
}

.nav-link:hover {
  background-color: var(--background-color);
  color: var(--primary-color);
}

.nav-link.router-link-active {
  background-color: var(--primary-light);
  color: var(--paper-color);
}

.nav-link i {
  margin-right: 0.75rem;
  width: 20px;
  text-align: center;
}

@media (max-width: 768px) {
  .navigation {
    padding: 0.75rem;
  }

  .logo {
    margin-bottom: 1rem;
  }

  .logo img {
    width: 32px;
    height: 32px;
  }

  .logo h1 {
    font-size: 1rem;
  }

  .nav-link {
    padding: 0.5rem;
  }
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 15px;
  background-color: #34495e;
  border-radius: 4px;
  margin-top: auto;
}

.user-avatar {
  width: 40px;
  height: 40px;
  background-color: #3498db;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-details {
  display: flex;
  flex-direction: column;
}

.username {
  font-weight: bold;
}

.role {
  font-size: 0.8rem;
  opacity: 0.8;
}
</style> 