/* global jest, describe, it, expect, beforeEach */
import { mount } from '@vue/test-utils'
import PathPlanning from '@/components/PathPlanning.vue'
import axios from 'axios'

// Mock axios
jest.mock('axios')

describe('PathPlanning.vue', () => {
  let wrapper
  
  beforeEach(() => {
    // Reset axios mock
    axios.get.mockReset()
    axios.post.mockReset()
    
    // Mock API responses
    axios.get.mockImplementation((url) => {
      if (url === '/api/v1/robots') {
        return Promise.resolve({
          data: [
            { id: 'robot1', name: 'Robot 1' },
            { id: 'robot2', name: 'Robot 2' }
          ]
        })
      } else if (url === '/api/v1/map/obstacles') {
        return Promise.resolve({
          data: [
            {
              type: 'rectangle',
              x1: 100,
              y1: 100,
              x2: 200,
              y2: 200,
              description: 'Building 1'
            }
          ]
        })
      } else if (url === '/api/v1/map/zones') {
        return Promise.resolve({
          data: [
            {
              id: 'zone1',
              type: 'planting',
              area: { x1: 50, y1: 50, x2: 150, y2: 150 }
            }
          ]
        })
      } else if (url === '/api/v1/map/charging_stations') {
        return Promise.resolve({
          data: [
            {
              id: 'station1',
              position: { x: 50, y: 50 }
            }
          ]
        })
      } else if (url === '/api/v1/map/paths') {
        return Promise.resolve({
          data: [
            {
              id: 'path1',
              points: [
                { x: 0, y: 0 },
                { x: 100, y: 100 }
              ]
            }
          ]
        })
      }
    })
    
    // Mock path planning response
    axios.post.mockImplementation((url, data) => {
      if (url.includes('/path')) {
        return Promise.resolve({
          data: [
            { x: 0, y: 0 },
            { x: 50, y: 50 },
            { x: 100, y: 100 }
          ]
        })
      } else if (url.includes('/optimize')) {
        return Promise.resolve({
          data: [
            { x: 0, y: 0, velocity: 0 },
            { x: 50, y: 50, velocity: 0.5 },
            { x: 100, y: 100, velocity: 0 }
          ]
        })
      }
    })
    
    wrapper = mount(PathPlanning)
  })
  
  it('renders correctly', () => {
    expect(wrapper.exists()).toBe(true)
    expect(wrapper.find('.map-canvas').exists()).toBe(true)
    expect(wrapper.find('.controls').exists()).toBe(true)
    expect(wrapper.find('.path-info').exists()).toBe(false)
  })
  
  it('loads robots on mount', async () => {
    await wrapper.vm.$nextTick()
    expect(axios.get).toHaveBeenCalledWith('/api/v1/robots')
    expect(wrapper.vm.robots).toHaveLength(2)
    expect(wrapper.vm.selectedRobot).toBe('robot1')
  })
  
  it('loads map data on mount', async () => {
    await wrapper.vm.$nextTick()
    expect(axios.get).toHaveBeenCalledWith('/api/v1/map/obstacles')
    expect(axios.get).toHaveBeenCalledWith('/api/v1/map/zones')
    expect(axios.get).toHaveBeenCalledWith('/api/v1/map/charging_stations')
    expect(axios.get).toHaveBeenCalledWith('/api/v1/map/paths')
  })
  
  it('plans path when button is clicked', async () => {
    wrapper.vm.startPosition = { x: 0, y: 0 }
    wrapper.vm.goalPosition = { x: 100, y: 100 }
    
    await wrapper.find('.plan-btn').trigger('click')
    await wrapper.vm.$nextTick()
    
    expect(axios.post).toHaveBeenCalledWith(
      '/api/v1/robots/robot1/path',
      {
        start: { x: 0, y: 0 },
        goal: { x: 100, y: 100 }
      }
    )
    expect(wrapper.vm.currentPath).toHaveLength(3)
    expect(wrapper.find('.path-info').exists()).toBe(true)
  })
  
  it('optimizes path when button is clicked', async () => {
    wrapper.vm.currentPath = [
      { x: 0, y: 0 },
      { x: 50, y: 50 },
      { x: 100, y: 100 }
    ]
    
    await wrapper.find('.optimize-btn').trigger('click')
    await wrapper.vm.$nextTick()
    
    expect(axios.post).toHaveBeenCalledWith(
      '/api/v1/robots/robot1/path/optimize',
      wrapper.vm.currentPath
    )
    expect(wrapper.vm.currentPath[0]).toHaveProperty('velocity')
  })
  
  it('calculates path metrics correctly', () => {
    wrapper.vm.currentPath = [
      { x: 0, y: 0 },
      { x: 3, y: 4 },
      { x: 6, y: 8 }
    ]
    
    wrapper.vm.calculatePathMetrics()
    
    expect(wrapper.vm.pathLength).toBeCloseTo(10, 2)
    expect(wrapper.vm.estimatedTime).toBeCloseTo(0.17, 2)
  })
  
  it('toggles map layers correctly', async () => {
    const checkboxes = wrapper.findAll('input[type="checkbox"]')
    
    // Test obstacles toggle
    await checkboxes[0].setChecked(false)
    expect(wrapper.vm.showObstacles).toBe(false)
    
    // Test zones toggle
    await checkboxes[1].setChecked(false)
    expect(wrapper.vm.showZones).toBe(false)
    
    // Test charging stations toggle
    await checkboxes[2].setChecked(false)
    expect(wrapper.vm.showChargingStations).toBe(false)
    
    // Test paths toggle
    await checkboxes[3].setChecked(false)
    expect(wrapper.vm.showPaths).toBe(false)
  })
  
  it('handles API errors gracefully', async () => {
    axios.get.mockRejectedValueOnce(new Error('API Error'))
    
    await wrapper.vm.$nextTick()
    
    expect(wrapper.vm.robots).toHaveLength(0)
    expect(console.error).toHaveBeenCalled()
  })
}) 