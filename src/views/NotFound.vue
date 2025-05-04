<template>
  <div class="not-found">
    <h1>404</h1>
    <h2>Page Not Found</h2>
    <p>
      The page you are looking for might have been removed, had its name changed, or is temporarily unavailable.
    </p>
    <router-link to="/" class="home-link">
      Return to Home
    </router-link>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'NotFound'
})
</script>

<style scoped>
.not-found {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  text-align: center;
  padding: 2rem;
}

h1 {
  font-size: 6rem;
  font-weight: 700;
  color: var(--primary-color);
  margin-bottom: 1rem;
  line-height: 1;
}

h2 {
  font-size: 2rem;
  font-weight: 600;
  color: var(--text-color);
  margin-bottom: 1.5rem;
}

p {
  max-width: 600px;
  margin-bottom: 2rem;
  font-size: 1.125rem;
  line-height: 1.6;
  color: var(--text-secondary);
}

.home-link {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  background-color: var(--primary-color);
  color: var(--paper-color);
  text-decoration: none;
  border-radius: var(--border-radius);
  transition: var(--transition);
}

.home-link:hover {
  background-color: var(--primary-dark);
}

@media (max-width: 768px) {
  .not-found {
    padding: 1.5rem;
  }

  h1 {
    font-size: 4rem;
  }

  h2 {
    font-size: 1.5rem;
  }

  p {
    font-size: 1rem;
  }
}
</style> 