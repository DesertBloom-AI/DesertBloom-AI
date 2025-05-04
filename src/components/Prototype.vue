<template>
  <div class="prototype">
    <div class="header">
      <h1>DesertBloom AI Prototype</h1>
      <div class="controls">
        <button class="btn" @click="toggleGrid">{{ showGrid ? 'Hide Grid' : 'Show Grid' }}</button>
        <button class="btn" @click="toggleAnnotations">{{ showAnnotations ? 'Hide Annotations' : 'Show Annotations' }}</button>
      </div>
    </div>

    <div class="prototype-container">
      <div class="sidebar">
        <div class="component-list">
          <h3>Component List</h3>
          <ul>
            <li v-for="component in components" :key="component.id" 
                draggable="true"
                @dragstart="onDragStart($event, component)">
              {{ component.name }}
            </li>
          </ul>
        </div>
      </div>

      <div class="canvas" 
           ref="canvas"
           :class="{ 'show-grid': showGrid }"
           @dragover.prevent
           @drop="onDrop">
        <div v-for="(item, index) in placedComponents" 
             :key="index"
             class="placed-component"
             :class="{ 'selected': selectedComponent === item }"
             :style="getComponentStyle(item)"
             @click="selectComponent(item)">
          <div class="component-content">
            {{ item.name }}
          </div>
          <div v-if="showAnnotations" class="annotations">
            <div class="annotation">{{ item.annotation }}</div>
          </div>
        </div>
      </div>

      <div class="properties-panel" v-if="selectedComponent">
        <h3>Properties</h3>
        <div class="property-group">
          <label>Name</label>
          <input v-model="selectedComponent.name" type="text">
        </div>
        <div class="property-group">
          <label>Annotation</label>
          <textarea v-model="selectedComponent.annotation"></textarea>
        </div>
        <div class="property-group">
          <label>Position</label>
          <div class="position-controls">
            <input v-model.number="selectedComponent.x" type="number" placeholder="X">
            <input v-model.number="selectedComponent.y" type="number" placeholder="Y">
          </div>
        </div>
        <div class="property-group">
          <label>Size</label>
          <div class="size-controls">
            <input v-model.number="selectedComponent.width" type="number" placeholder="Width">
            <input v-model.number="selectedComponent.height" type="number" placeholder="Height">
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, reactive } from 'vue'

interface Component {
  id: number
  name: string
  type: string
  x: number
  y: number
  width: number
  height: number
  annotation: string
}

export default defineComponent({
  name: 'Prototype',
  setup() {
    const showGrid = ref(true)
    const showAnnotations = ref(true)
    const selectedComponent = ref<Component | null>(null)
    const canvas = ref<HTMLElement | null>(null)

    const components = reactive<Component[]>([
      { id: 1, name: 'Navigation', type: 'navigation', x: 0, y: 0, width: 0, height: 0, annotation: '' },
      { id: 2, name: 'Path Planning', type: 'path-planning', x: 0, y: 0, width: 0, height: 0, annotation: '' },
      { id: 3, name: 'Robot Control', type: 'robot-control', x: 0, y: 0, width: 0, height: 0, annotation: '' },
      { id: 4, name: 'Analytics', type: 'analytics', x: 0, y: 0, width: 0, height: 0, annotation: '' },
      { id: 5, name: 'Settings', type: 'settings', x: 0, y: 0, width: 0, height: 0, annotation: '' }
    ])

    const placedComponents = reactive<Component[]>([
      {
        id: 1,
        name: 'Navigation',
        type: 'navigation',
        x: 0,
        y: 0,
        width: 250,
        height: 100,
        annotation: 'Top navigation bar with logo and main links'
      },
      {
        id: 2,
        name: 'Path Planning',
        type: 'path-planning',
        x: 300,
        y: 150,
        width: 400,
        height: 300,
        annotation: 'Main path planning area with map and path display'
      },
      {
        id: 3,
        name: 'Robot Control',
        type: 'robot-control',
        x: 300,
        y: 500,
        width: 400,
        height: 200,
        annotation: 'Robot control panel with status and controls'
      },
      {
        id: 4,
        name: 'Analytics',
        type: 'analytics',
        x: 800,
        y: 150,
        width: 300,
        height: 300,
        annotation: 'Analytics charts and performance metrics'
      },
      {
        id: 5,
        name: 'Settings',
        type: 'settings',
        x: 800,
        y: 500,
        width: 300,
        height: 200,
        annotation: 'System settings and configuration options'
      }
    ])

    const onDragStart = (event: DragEvent, component: Component) => {
      event.dataTransfer?.setData('component', JSON.stringify(component))
    }

    const onDrop = (event: DragEvent) => {
      if (!canvas.value) return
      
      const component = JSON.parse(event.dataTransfer?.getData('component') || '{}') as Component
      const rect = canvas.value.getBoundingClientRect()
      const x = event.clientX - rect.left
      const y = event.clientY - rect.top

      placedComponents.push({
        ...component,
        x,
        y,
        width: 200,
        height: 100,
        annotation: 'New component'
      })
    }

    const selectComponent = (component: Component) => {
      selectedComponent.value = component
    }

    const getComponentStyle = (component: Component) => {
      return {
        left: `${component.x}px`,
        top: `${component.y}px`,
        width: `${component.width}px`,
        height: `${component.height}px`
      }
    }

    const toggleGrid = () => {
      showGrid.value = !showGrid.value
    }

    const toggleAnnotations = () => {
      showAnnotations.value = !showAnnotations.value
    }

    return {
      showGrid,
      showAnnotations,
      selectedComponent,
      canvas,
      components,
      placedComponents,
      onDragStart,
      onDrop,
      selectComponent,
      getComponentStyle,
      toggleGrid,
      toggleAnnotations
    }
  }
})
</script>

<style scoped>
.prototype {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.header {
  padding: 1rem;
  background-color: var(--paper-color);
  border-bottom: 1px solid var(--background-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header h1 {
  font-size: 1.5rem;
  color: var(--text-color);
}

.controls {
  display: flex;
  gap: 1rem;
}

.btn {
  padding: 0.5rem 1rem;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn:hover {
  background-color: var(--primary-dark);
}

.prototype-container {
  flex: 1;
  display: grid;
  grid-template-columns: 250px 1fr 300px;
  gap: 1rem;
  padding: 1rem;
  overflow: hidden;
}

.sidebar {
  background-color: var(--paper-color);
  border-radius: 8px;
  padding: 1rem;
  overflow-y: auto;
}

.component-list h3 {
  margin-bottom: 1rem;
  color: var(--text-color);
}

.component-list ul {
  list-style: none;
  padding: 0;
}

.component-list li {
  padding: 0.5rem;
  margin-bottom: 0.5rem;
  background-color: var(--background-color);
  border-radius: 4px;
  cursor: move;
}

.component-list li:hover {
  background-color: var(--primary-light);
  color: white;
}

.canvas {
  background-color: var(--paper-color);
  border-radius: 8px;
  position: relative;
  overflow: auto;
}

.canvas.show-grid {
  background-image: linear-gradient(var(--background-color) 1px, transparent 1px),
                    linear-gradient(90deg, var(--background-color) 1px, transparent 1px);
  background-size: 20px 20px;
}

.placed-component {
  position: absolute;
  background-color: white;
  border: 1px solid var(--background-color);
  border-radius: 4px;
  cursor: move;
  transition: all 0.3s ease;
}

.placed-component:hover {
  border-color: var(--primary-color);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.placed-component.selected {
  border: 2px solid var(--primary-color);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1;
}

.component-content {
  padding: 0.5rem;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.annotations {
  position: absolute;
  bottom: -20px;
  left: 0;
  width: 100%;
}

.annotation {
  font-size: 0.75rem;
  color: var(--text-secondary);
  text-align: center;
}

.properties-panel {
  background-color: var(--paper-color);
  border-radius: 8px;
  padding: 1rem;
  overflow-y: auto;
}

.properties-panel h3 {
  margin-bottom: 1rem;
  color: var(--text-color);
}

.property-group {
  margin-bottom: 1rem;
}

.property-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: var(--text-secondary);
}

.property-group input,
.property-group textarea {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid var(--background-color);
  border-radius: 4px;
}

.position-controls,
.size-controls {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
}
</style> 