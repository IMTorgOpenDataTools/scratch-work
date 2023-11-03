import { createApp } from 'vue';
import App from '@/App.vue';

import { pinia }  from './stores/config.js';
import { useRepo } from 'pinia-orm'


const app = createApp(App)
app.use(pinia)


import DisplayStore from '@/stores/DisplayStore';
export const useDisplayStore = DisplayStore()


//table init
import {Person, PersonProjectStatus, StepStatus,
    Project, Interaction, UseCase, 
    Lifecycle, LifecycleStep, 
    Account} from '@/stores/Tables.js';
export const usePerson = useRepo(Person, pinia);
export const usePersonProjectStatus = useRepo(PersonProjectStatus, pinia);
export const useStepStatus = useRepo(StepStatus, pinia);

export const useProject = useRepo(Project, pinia);
export const useInteraction = useRepo(Interaction, pinia);
export const useUseCase = useRepo(UseCase, pinia);

export const useLifecycle = useRepo(Lifecycle, pinia);
export const useLifecycleStep = useRepo(LifecycleStep, pinia);

export const useAccount = useRepo(Account, pinia);


app.mount('#app')