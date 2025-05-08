declare module 'vuex' {
  import { Store } from 'vuex'
  export { Store }
  export function useStore(): Store<any>
} 