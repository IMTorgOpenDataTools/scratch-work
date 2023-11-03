import { createPinia } from 'pinia'
import { createPersistedState } from 'pinia-plugin-persistedstate'
import { createORM } from 'pinia-orm'

export const pinia = createPinia()

pinia.use(createORM(
  { 
    model: { withMeta:true } 
  }
))
pinia.use(createPersistedState({
    auto: true,
    storage: localStorage
  }))