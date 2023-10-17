<template>

    <button type="button" @click="setUser">Create</button>
    <button type="button" @click="getUser">Read Users</button>
    <button type="button" @click="getPost">Read Posts</button>

    <button type="button" @click="getUser">Update</button>
    <button type="button" @click="deleteUser">Delete</button>
    <button type="button" @click="deleteAll">Delete All</button>

    <div v-for="user of display.users" >
      {{user}}
    </div>

    <div v-for="post of display.posts" >
      {{post}}
    </div>

</template>

<script>
import {useUser, useComment, usePost} from '@/main.js';

export default {
  name: `Test`,
  data() {
    return {
      display:{
        users:[],
        posts:[]
      }
    }
  },
  methods:{
    setUser(){
        const posts = [
              {
                id: 1,
                body: '.....',
                author: { id: 1, name: 'User 1' },
                comments: [
                  {
                    id: 1,
                    comment: '.....',
                    author: { id: 2, name: 'User 2' }
                  },
                  {
                    id: 2,
                    comment: '.....',
                    author: { id: 2, name: 'User 2' }
                  }
                ]
              },
              {
                id: 2,
                author: { id: 2, name: 'User 2' },
                body: '.....',
                comments: [
                  {
                    id: 3,
                    comment: '.....',
                    author: { id: 3, name: 'User 3' }
                  },
                  {
                    id: 4,
                    comment: '.....',
                    author: { id: 1, name: 'User 1' }
                  },
                  {
                    id: 5,
                    comment: '.....',
                    author: { id: 3, name: 'User 3' }
                  }
                ]
              }
            ]
        usePost.save(posts);
    },
    getUser(){
        this.display.posts.length = 0
        const users = useUser.all()
        this.display.users.push(...users )
    },
    getPost(){
        this.display.users.length = 0
        const posts = usePost.all()
        this.display.posts.push(...posts)
    },
    deleteUser(){
        const user0 = useUser.all()[0]
        useUser.destroy(user0.id)
        const idx = this.display.users.map(user => user.id).indexOf(user0.id)
        this.display.users.splice(idx,1)
    },
      deleteAll(){
        useUser.flush()
        this.display.users.length = 0
    }
  }
};



</script>