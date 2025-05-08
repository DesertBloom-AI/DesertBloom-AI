import { createStore } from 'vuex'
import pathPlanningModule from './modules/path_planning'
import { RootState } from './types'

const store = createStore<RootState>({
  modules: {
    pathPlanning: pathPlanningModule
  }
})

export default store 