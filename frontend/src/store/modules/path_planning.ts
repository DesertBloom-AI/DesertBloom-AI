import { Module } from 'vuex'
import { RootState } from '../types'

export interface PathPlanningState {
  selectedRobot: string | null
  startPosition: [number, number] | null
  goalPosition: [number, number] | null
  path: [number, number][] | null
  obstacles: [number, number][]
  isPlanning: boolean
  error: string | null
}

const pathPlanningModule: Module<PathPlanningState, RootState> = {
  namespaced: true,

  state: {
    selectedRobot: null,
    startPosition: null,
    goalPosition: null,
    path: null,
    obstacles: [],
    isPlanning: false,
    error: null
  },

  mutations: {
    SET_SELECTED_ROBOT(state, robotId: string) {
      state.selectedRobot = robotId
    },

    SET_START_POSITION(state, position: [number, number]) {
      state.startPosition = position
    },

    SET_GOAL_POSITION(state, position: [number, number]) {
      state.goalPosition = position
    },

    SET_PATH(state, path: [number, number][]) {
      state.path = path
    },

    ADD_OBSTACLE(state, position: [number, number]) {
      state.obstacles.push(position)
    },

    CLEAR_OBSTACLES(state) {
      state.obstacles = []
    },

    SET_PLANNING(state, isPlanning: boolean) {
      state.isPlanning = isPlanning
    },

    SET_ERROR(state, error: string | null) {
      state.error = error
    },

    RESET_STATE(state) {
      state.selectedRobot = null
      state.startPosition = null
      state.goalPosition = null
      state.path = null
      state.obstacles = []
      state.isPlanning = false
      state.error = null
    }
  },

  actions: {
    selectRobot({ commit }, robotId: string) {
      commit('SET_SELECTED_ROBOT', robotId)
    },

    setStartPosition({ commit }, position: [number, number]) {
      commit('SET_START_POSITION', position)
    },

    setGoalPosition({ commit }, position: [number, number]) {
      commit('SET_GOAL_POSITION', position)
    },

    addObstacle({ commit }, position: [number, number]) {
      commit('ADD_OBSTACLE', position)
    },

    clearObstacles({ commit }) {
      commit('CLEAR_OBSTACLES')
    },

    async planPath({ commit, state }) {
      if (!state.selectedRobot || !state.startPosition || !state.goalPosition) {
        commit('SET_ERROR', 'Missing required parameters')
        return
      }

      commit('SET_PLANNING', true)
      commit('SET_ERROR', null)

      try {
        // TODO: Implement actual path planning logic
        const mockPath: [number, number][] = [
          state.startPosition,
          [state.startPosition[0] + 1, state.startPosition[1] + 1],
          [state.goalPosition[0] - 1, state.goalPosition[1] - 1],
          state.goalPosition
        ]

        commit('SET_PATH', mockPath)
      } catch (error) {
        commit('SET_ERROR', error instanceof Error ? error.message : 'Unknown error')
      } finally {
        commit('SET_PLANNING', false)
      }
    },

    resetState({ commit }) {
      commit('RESET_STATE')
    }
  },

  getters: {
    hasValidInput: (state) => {
      return !!state.selectedRobot && !!state.startPosition && !!state.goalPosition
    },

    pathLength: (state) => {
      if (!state.path) return 0

      let length = 0
      for (let i = 1; i < state.path.length; i++) {
        const [x1, y1] = state.path[i - 1]
        const [x2, y2] = state.path[i]
        length += Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2))
      }
      return length
    }
  }
}

export default pathPlanningModule 