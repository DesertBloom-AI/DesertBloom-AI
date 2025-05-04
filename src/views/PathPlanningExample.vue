<template>
  <div class="path-planning-example">
    <h1>Path Planning Example</h1>
    <p>
      This example demonstrates the path planning component in action. You can:
    </p>
    <ul>
      <li>Select a robot from the dropdown</li>
      <li>Click on the map to set start and goal positions</li>
      <li>Plan and optimize paths</li>
      <li>Toggle map layers</li>
      <li>View path metrics</li>
    </ul>

    <div class="component-container">
      <PathPlanning />
    </div>

    <div class="code-example">
      <h2>Code Example</h2>
      <pre><code>{{ exampleCode }}</code></pre>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import PathPlanning from '@/components/PathPlanning.vue'

export default defineComponent({
  name: 'PathPlanningExample',
  components: {
    PathPlanning
  },
  setup() {
    const exampleCode = `<template>\n  <PathPlanning />\n</template>\n\n<script>\nimport PathPlanning from '@/components/PathPlanning.vue'\n\nexport default {\n  components: {\n    PathPlanning\n  }\n}\n</script>`;

    return {
      exampleCode
    }
  }
})
</script>

<style scoped>
.path-planning-example {
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
  margin-bottom: 1.5rem;
  max-width: 800px;
}

ul {
  list-style-position: inside;
  margin-bottom: 2rem;
}

ul li {
  font-size: 1.125rem;
  color: var(--text-secondary);
  margin-bottom: 0.5rem;
}

.component-container {
  background-color: var(--paper-color);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);
  padding: 2rem;
  margin-bottom: 2rem;
}

.code-example {
  background-color: var(--paper-color);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);
  padding: 2rem;
}

.code-example h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-color);
  margin-bottom: 1rem;
}

pre {
  background-color: var(--background-color);
  border-radius: var(--border-radius);
  padding: 1rem;
  overflow-x: auto;
}

code {
  font-family: 'Courier New', Courier, monospace;
  font-size: 0.875rem;
  color: var(--text-color);
}

@media (max-width: 768px) {
  .path-planning-example {
    padding: 1rem;
  }

  h1 {
    font-size: 1.5rem;
  }

  p, ul li {
    font-size: 1rem;
  }

  .component-container,
  .code-example {
    padding: 1rem;
  }
}
</style> 