<template>
  <div class="home">
    <h1>Welcome to DesertBloom AI</h1>
    <p>
      DesertBloom AI is a comprehensive platform for managing and monitoring
      autonomous robots in desert environments.
    </p>

    <div class="features">
      <div class="feature-card">
        <i class="fas fa-route"></i>
        <h2>Path Planning</h2>
        <p>
          Plan and optimize robot paths with our intuitive path planning
          interface.
        </p>
        <router-link to="/path-planning" class="feature-link">
          Get Started
        </router-link>
      </div>

      <div class="feature-card">
        <i class="fas fa-chart-line"></i>
        <h2>Monitoring</h2>
        <p>
          Monitor robot status, battery levels, and environmental conditions in
          real-time.
        </p>
        <router-link to="/monitoring" class="feature-link">
          View Dashboard
        </router-link>
      </div>

      <div class="feature-card">
        <i class="fas fa-cog"></i>
        <h2>Settings</h2>
        <p>
          Configure robot parameters, map settings, and system preferences.
        </p>
        <router-link to="/settings" class="feature-link">
          Configure
        </router-link>
      </div>
    </div>

    <div class="quick-start">
      <h2>Quick Start</h2>
      <ol>
        <li>
          <router-link to="/path-planning/example">
            Try the path planning example
          </router-link>
        </li>
        <li>
          <router-link to="/robotics">
            View available robots
          </router-link>
        </li>
        <li>
          <router-link to="/analytics">
            Check system analytics
          </router-link>
        </li>
      </ol>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'Home'
})
</script>

<style scoped>
.home {
  padding: 2rem;
}

h1 {
  font-size: 2rem;
  font-weight: 600;
  color: var(--primary-color);
  margin-bottom: 1rem;
}

p {
  font-size: 1.125rem;
  color: var(--text-secondary);
  margin-bottom: 2rem;
  max-width: 800px;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.feature-card {
  background-color: var(--paper-color);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);
  padding: 2rem;
  transition: var(--transition);
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.feature-card i {
  font-size: 2rem;
  color: var(--primary-color);
  margin-bottom: 1rem;
}

.feature-card h2 {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-color);
  margin-bottom: 0.75rem;
}

.feature-card p {
  font-size: 1rem;
  color: var(--text-secondary);
  margin-bottom: 1.5rem;
}

.feature-link {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  background-color: var(--primary-color);
  color: var(--paper-color);
  text-decoration: none;
  border-radius: var(--border-radius);
  transition: var(--transition);
}

.feature-link:hover {
  background-color: var(--primary-dark);
}

.quick-start {
  background-color: var(--paper-color);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);
  padding: 2rem;
}

.quick-start h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-color);
  margin-bottom: 1.5rem;
}

.quick-start ol {
  list-style-position: inside;
  margin-left: 1rem;
}

.quick-start li {
  margin-bottom: 1rem;
  font-size: 1.125rem;
}

.quick-start a {
  color: var(--primary-color);
  text-decoration: none;
  transition: var(--transition);
}

.quick-start a:hover {
  color: var(--primary-dark);
  text-decoration: underline;
}

@media (max-width: 768px) {
  .home {
    padding: 1rem;
  }

  h1 {
    font-size: 1.5rem;
  }

  .features {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .feature-card {
    padding: 1.5rem;
  }

  .quick-start {
    padding: 1.5rem;
  }
}
</style> 