<template>

    <button type="button" @click="setUser">Create</button>
    <button type="button" @click="getUser">Read</button>
    <button type="button" @click="getUser">Update</button>
    <button type="button" @click="deleteUser">Delete</button>
    <button type="button" @click="deleteAll">Delete All</button>

    <div v-for="user of display.users" >
      {{user}}
    </div>

</template>

<script>
import {useUser} from '@/main.js';

export default {
  name: `Test`,
  data() {
    return {
      display:{
        users:[]
      }
    }
  },
  methods:{
    setUser(){
        const users = [
          { name: 'John Doe', age: 40 },
          { name: 'Jane Doe', age: 30 },
          { name: 'Johnny Doe', age: 20 }
        ]
        useUser.save(users);
    },
    getUser(){
        const users = useUser.all()
        this.display.users.push(...users )
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