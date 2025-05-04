<template>
  <div class="app">
    <header class="header">
      <h1>DesertBloom AI</h1>
    </header>

    <div class="main-content">
      <Navigation />
      <main class="content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import Navigation from '@/components/Navigation.vue'

export default defineComponent({
  name: 'App',
  components: {
    Navigation
  }
})
</script>

<style>
:root {
  --primary-color: #2E7D32;
  --primary-light: #4CAF50;
  --primary-dark: #1B5E20;
  --secondary-color: #FFA000;
  --secondary-light: #FFB74D;
  --secondary-dark: #F57C00;
  --background-color: #F5F5F5;
  --paper-color: #FFFFFF;
  --text-color: #333333;
  --text-secondary: #666666;
  --error-color: #D32F2F;
  --warning-color: #FFA000;
  --success-color: #2E7D32;
  --info-color: #1976D2;
  --border-radius: 8px;
  --shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  --transition: 0.3s ease;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: "Roboto", "Helvetica", "Arial", sans-serif;
  line-height: 1.5;
  color: var(--text-color);
  background-color: var(--background-color);
}

.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  padding: 1rem;
  background-color: var(--paper-color);
  box-shadow: var(--shadow);
}

.header h1 {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--primary-color);
}

.main-content {
  flex: 1;
  display: grid;
  grid-template-columns: 250px 1fr;
  gap: 1rem;
  padding: 1rem;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

.content {
  background-color: var(--paper-color);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);
  padding: 1rem;
  overflow: auto;
}

@media (max-width: 768px) {
  .main-content {
    grid-template-columns: 1fr;
    padding: 0.5rem;
  }

  .header {
    padding: 0.75rem;
  }

  .content {
    padding: 0.75rem;
  }
}

/* Font Awesome */
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');
</style> 