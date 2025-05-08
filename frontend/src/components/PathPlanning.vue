<template>
  <div class="path-planning">
    <div class="controls">
      <div class="control-group">
        <label for="robot-select">Select Robot</label>
        <select
          id="robot-select"
          v-model="selectedRobot"
          @change="onRobotSelect"
        >
          <option value="robot1">Robot 1</option>
          <option value="robot2">Robot 2</option>
          <option value="robot3">Robot 3</option>
        </select>
      </div>

      <div class="control-group">
        <button
          class="btn"
          :disabled="!hasValidInput"
          @click="planPath"
        >
          Plan Path
        </button>
        <button
          class="btn"
          :disabled="!path"
          @click="clearPath"
        >
          Clear Path
        </button>
      </div>

      <div class="control-group">
        <button
          class="btn"
          @click="addObstacle"
        >
          Add Obstacle
        </button>
        <button
          class="btn"
          :disabled="obstacles.length === 0"
          @click="clearObstacles"
        >
          Clear Obstacles
        </button>
      </div>

      <div class="metrics" v-if="path">
        <h3>Path Metrics</h3>
        <div class="metric">
          <span class="label">Length:</span>
          <span class="value">{{ pathLength.toFixed(2) }} m</span>
        </div>
        <div class="metric">
          <span class="label">Time:</span>
          <span class="value">{{ estimatedTime.toFixed(2) }} s</span>
        </div>
        <div class="metric">
          <span class="label">Energy:</span>
          <span class="value">{{ energyConsumption.toFixed(2) }} J</span>
        </div>
      </div>
    </div>

    <div class="map-container">
      <div
        class="map"
        ref="map"
        @click="onMapClick"
      >
        <div
          v-if="startPosition"
          class="marker start"
          :style="getMarkerStyle(startPosition)"
        ></div>
        <div
          v-if="goalPosition"
          class="marker goal"
          :style="getMarkerStyle(goalPosition)"
        ></div>
        <div
          v-for="(obstacle, index) in obstacles"
          :key="`obstacle-${index}`"
          class="marker obstacle"
          :style="getMarkerStyle(obstacle)"
        ></div>
        <svg
          v-if="path"
          class="path-line"
          :viewBox="getViewBox"
        >
          <path
            :d="getPathD"
            fill="none"
            stroke="#2196f3"
            stroke-width="2"
          />
        </svg>
      </div>
    </div>

    <div v-if="error" class="error">
      {{ error }}
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { key } from '@/store'
// import { calculatePathMetrics } from '@/utils/path_planning'

export default defineComponent({
  name: 'PathPlanning',

  setup() {
    const store = useStore(key)
    const map = ref<HTMLElement | null>(null)

    const selectedRobot = ref('robot1')
    const startPosition = ref<[number, number] | null>(null)
    const goalPosition = ref<[number, number] | null>(null)
    const path = ref<[number, number][] | null>(null)
    const obstacles = ref<[number, number][]>([])
    const isPlanning = ref(false)
    const error = ref<string | null>(null)

    const hasValidInput = computed(() => {
      return !!selectedRobot.value && !!startPosition.value && !!goalPosition.value
    })

    const pathLength = computed(() => {
      if (!path.value) return 0
      return path.value.reduce((total, point, index) => {
        if (index === 0) return 0
        const prevPoint = path.value![index - 1]
        const dx = point[0] - prevPoint[0]
        const dy = point[1] - prevPoint[1]
        return total + Math.sqrt(dx * dx + dy * dy)
      }, 0)
    })

    const estimatedTime = computed(() => {
      if (!path.value) return 0
      return pathLength.value / 1.0 // Assuming 1 m/s speed
    })

    const energyConsumption = computed(() => {
      if (!path.value) return 0
      return pathLength.value * 10 // Assuming 10 J/m energy consumption
    })

    const getViewBox = computed(() => {
      if (!map.value) return '0 0 0 0'
      const { width, height } = map.value.getBoundingClientRect()
      return `0 0 ${width} ${height}`
    })

    const getPathD = computed(() => {
      if (!path.value) return ''
      return path.value
        .map((point, index) => {
          const [x, y] = point
          return `${index === 0 ? 'M' : 'L'} ${x} ${y}`
        })
        .join(' ')
    })

    const getMarkerStyle = (position: [number, number]) => {
      const [x, y] = position
      return {
        left: `${x}px`,
        top: `${y}px`
      }
    }

    const onRobotSelect = () => {
      store.dispatch('pathPlanning/selectRobot', selectedRobot.value)
    }

    const onMapClick = (event: MouseEvent) => {
      if (!map.value) return

      const rect = map.value.getBoundingClientRect()
      const x = event.clientX - rect.left
      const y = event.clientY - rect.top

      if (!startPosition.value) {
        startPosition.value = [x, y]
        store.dispatch('pathPlanning/setStartPosition', [x, y])
      } else if (!goalPosition.value) {
        goalPosition.value = [x, y]
        store.dispatch('pathPlanning/setGoalPosition', [x, y])
      }
    }

    const planPath = async () => {
      if (!hasValidInput.value) return

      isPlanning.value = true
      error.value = null

      try {
        const result = await store.dispatch('pathPlanning/planPath')
        path.value = result
      } catch (err) {
        error.value = err instanceof Error ? err.message : 'An error occurred'
      } finally {
        isPlanning.value = false
      }
    }

    const clearPath = () => {
      startPosition.value = null
      goalPosition.value = null
      path.value = null
      store.dispatch('pathPlanning/resetState')
    }

    const addObstacle = (event: MouseEvent) => {
      if (!map.value) return

      const rect = map.value.getBoundingClientRect()
      const x = event.clientX - rect.left
      const y = event.clientY - rect.top

      obstacles.value.push([x, y])
      store.dispatch('pathPlanning/addObstacle', [x, y])
    }

    const clearObstacles = () => {
      obstacles.value = []
      store.dispatch('pathPlanning/clearObstacles')
    }

    onMounted(() => {
      // Initialize map
    })

    return {
      map,
      selectedRobot,
      startPosition,
      goalPosition,
      path,
      obstacles,
      isPlanning,
      error,
      hasValidInput,
      pathLength,
      estimatedTime,
      energyConsumption,
      getViewBox,
      getPathD,
      getMarkerStyle,
      onRobotSelect,
      onMapClick,
      planPath,
      clearPath,
      addObstacle,
      clearObstacles
    }
  }
})
</script>

<style scoped>
.path-planning {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 2rem;
  height: 100%;
}

.controls {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.control-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-color);
}

select {
  padding: 0.75rem;
  border: 1px solid var(--background-color);
  border-radius: var(--border-radius);
  background-color: var(--paper-color);
  color: var(--text-color);
  font-size: 1rem;
  transition: var(--transition);
}

select:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px var(--primary-light);
}

.btn {
  padding: 0.75rem 1.5rem;
  background-color: var(--primary-color);
  color: var(--paper-color);
  border: none;
  border-radius: var(--border-radius);
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: var(--transition);
}

.btn:hover:not(:disabled) {
  background-color: var(--primary-dark);
}

.btn:disabled {
  background-color: var(--background-color);
  color: var(--text-secondary);
  cursor: not-allowed;
}

.metrics {
  background-color: var(--paper-color);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);
  padding: 1.5rem;
}

.metrics h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-color);
  margin-bottom: 1rem;
}

.metric {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.metric:last-child {
  margin-bottom: 0;
}

.metric .label {
  color: var(--text-secondary);
}

.metric .value {
  font-weight: 500;
  color: var(--text-color);
}

.map-container {
  background-color: var(--paper-color);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);
  overflow: hidden;
}

.map {
  width: 100%;
  height: 100%;
  min-height: 500px;
}

.marker {
  position: absolute;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  transform: translate(-50%, -50%);
}

.marker.start {
  background-color: #4caf50;
}

.marker.goal {
  background-color: #f44336;
}

.marker.obstacle {
  background-color: #ff9800;
}

.path-line {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.error {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  padding: 10px 20px;
  background-color: #f44336;
  color: white;
  border-radius: 4px;
  z-index: 1;
}

@media (max-width: 768px) {
  .path-planning {
    grid-template-columns: 1fr;
  }

  .controls {
    gap: 1rem;
  }

  .metrics {
    padding: 1rem;
  }

  .map {
    min-height: 300px;
  }
}
</style> 