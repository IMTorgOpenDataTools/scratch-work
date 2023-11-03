import { createApp } from 'vue';
import App from '@/App.vue';

import { pinia}  from './stores/config.js';
import { useRepo } from 'pinia-orm'


const app = createApp(App)
app.use(pinia)

//table init
import {User, Post, Comment} from '@/stores/Tables.js';
export const useUser = useRepo(User, pinia);
export const usePost = useRepo(Post, pinia);
export const useComment = useRepo(Comment, pinia);


app.mount('#app')