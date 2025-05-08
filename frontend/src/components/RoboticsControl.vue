<template>
  <div class="robotics-control">
    <h2>Robotics Control</h2>
    
    <!-- Robot Status Cards -->
    <div class="robot-cards">
      <div v-for="robot in robots" :key="robot.id" class="robot-card">
        <h3>{{ robot.id }}</h3>
        <div class="status-indicator" :class="robot.status"></div>
        <div class="robot-info">
          <p>Battery: {{ robot.battery }}%</p>
          <p>Position: ({{ robot.position.x }}, {{ robot.position.y }})</p>
          <p>Current Task: {{ robot.currentTask || 'None' }}</p>
        </div>
        <div class="robot-actions">
          <button @click="emergencyStop(robot.id)" class="emergency-btn">Emergency Stop</button>
          <button @click="showTaskModal(robot.id)" class="assign-btn">Assign Task</button>
        </div>
      </div>
    </div>
    
    <!-- Task Queue -->
    <div class="task-queue">
      <h3>Task Queue</h3>
      <table>
        <thead>
          <tr>
            <th>Task ID</th>
            <th>Robot</th>
            <th>Type</th>
            <th>Status</th>
            <th>Priority</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="task in taskQueue" :key="task.id">
            <td>{{ task.id }}</td>
            <td>{{ task.robot_id }}</td>
            <td>{{ task.type }}</td>
            <td>{{ task.status }}</td>
            <td>{{ task.priority }}</td>
            <td>
              <button @click="cancelTask(task.id)" class="cancel-btn">Cancel</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <!-- Task Assignment Modal -->
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <h3>Assign Task to {{ selectedRobot }}</h3>
        <form @submit.prevent="assignTask">
          <div class="form-group">
            <label>Task Type</label>
            <select v-model="newTask.type">
              <option value="planting">Planting</option>
              <option value="watering">Watering</option>
              <option value="monitoring">Monitoring</option>
            </select>
          </div>
          
          <div v-if="newTask.type === 'planting'" class="form-group">
            <label>Quantity</label>
            <input type="number" v-model="newTask.quantity" min="1">
            <label>Species</label>
            <input type="text" v-model="newTask.species">
            <label>Spacing (m)</label>
            <input type="number" v-model="newTask.spacing" min="0.1" step="0.1">
          </div>
          
          <div v-if="newTask.type === 'watering'" class="form-group">
            <label>Water Amount (L)</label>
            <input type="number" v-model="newTask.water_amount" min="1">
            <label>Duration (min)</label>
            <input type="number" v-model="newTask.duration" min="1">
          </div>
          
          <div v-if="newTask.type === 'monitoring'" class="form-group">
            <label>Interval (min)</label>
            <input type="number" v-model="newTask.interval" min="1">
            <label>Duration (min)</label>
            <input type="number" v-model="newTask.duration" min="1">
          </div>
          
          <div class="form-group">
            <label>Priority</label>
            <select v-model="newTask.priority">
              <option value="1">Low</option>
              <option value="2">Medium</option>
              <option value="3">High</option>
            </select>
          </div>
          
          <div class="modal-actions">
            <button type="submit" class="submit-btn">Assign Task</button>
            <button @click="closeModal" class="cancel-btn">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'RoboticsControl',
  setup() {
    const robots = ref([])
    const taskQueue = ref([])
    const showModal = ref(false)
    const selectedRobot = ref('')
    const newTask = ref({
      type: 'planting',
      priority: '2',
      quantity: 1,
      species: '',
      spacing: 0.5,
      water_amount: 10,
      duration: 30,
      interval: 5
    })

    const fetchRobots = async () => {
      try {
        const response = await axios.get('/api/v1/robots')
        robots.value = response.data
      } catch (error) {
        console.error('Error fetching robots:', error)
      }
    }

    const fetchTaskQueue = async () => {
      try {
        const response = await axios.get('/api/v1/tasks/queue')
        taskQueue.value = response.data.tasks
      } catch (error) {
        console.error('Error fetching task queue:', error)
      }
    }

    const emergencyStop = async (robotId) => {
      try {
        await axios.post(`/api/v1/robots/${robotId}/emergency_stop`)
        await fetchRobots()
      } catch (error) {
        console.error('Error stopping robot:', error)
      }
    }

    const showTaskModal = (robotId) => {
      selectedRobot.value = robotId
      showModal.value = true
    }

    const closeModal = () => {
      showModal.value = false
      selectedRobot.value = ''
      newTask.value = {
        type: 'planting',
        priority: '2',
        quantity: 1,
        species: '',
        spacing: 0.5,
        water_amount: 10,
        duration: 30,
        interval: 5
      }
    }

    const assignTask = async () => {
      try {
        await axios.post(`/api/v1/robots/${selectedRobot.value}/tasks`, newTask.value)
        await fetchTaskQueue()
        closeModal()
      } catch (error) {
        console.error('Error assigning task:', error)
      }
    }

    const cancelTask = async (taskId) => {
      try {
        await axios.delete(`/api/v1/tasks/${taskId}`)
        await fetchTaskQueue()
      } catch (error) {
        console.error('Error canceling task:', error)
      }
    }

    onMounted(() => {
      fetchRobots()
      fetchTaskQueue()
      // Set up polling for real-time updates
      setInterval(() => {
        fetchRobots()
        fetchTaskQueue()
      }, 5000)
    })

    return {
      robots,
      taskQueue,
      showModal,
      selectedRobot,
      newTask,
      emergencyStop,
      showTaskModal,
      closeModal,
      assignTask,
      cancelTask
    }
  }
}
</script>

<style scoped>
.robotics-control {
  padding: 20px;
}

.robot-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.robot-card {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.status-indicator {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  margin: 10px 0;
}

.status-indicator.ready {
  background-color: #4CAF50;
}

.status-indicator.busy {
  background-color: #FFC107;
}

.status-indicator.emergency_stop {
  background-color: #F44336;
}

.robot-info {
  margin: 10px 0;
}

.robot-actions {
  display: flex;
  gap: 10px;
}

.task-queue {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: #fff;
  padding: 30px;
  border-radius: 8px;
  width: 500px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input, select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.emergency-btn {
  background-color: #F44336;
  color: white;
}

.assign-btn {
  background-color: #2196F3;
  color: white;
}

.cancel-btn {
  background-color: #9E9E9E;
  color: white;
}

.submit-btn {
  background-color: #4CAF50;
  color: white;
}
</style> 