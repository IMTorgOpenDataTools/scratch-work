<template>

    <button type="button" @click="setUser">Create</button><br>
      <code>usePost.save(originalPosts);</code><br>
      Observations:
      <ul>
        <li>Looking into `local storage: posts` for `author` data, the associated referencing data is stored as `user_id`.</li>
      </ul><br>

    <button type="button" @click="getPost">Read Posts</button><br>
      <code>usePost.all()</code><br>

    <button type="button" @click="getPostWithAuthors">Read Posts with Authors</button><br>
      <code>usePost.query().with('author').get()</code><br>
      Observations:
      <ul>
        <li>The difference between using `hasOne()` / `hasMany()`, and `belongsTo()` which Repo the foreign key is expected.</li>
        <li>The only relationship data maintained is the foreign key.</li>
        <li>Use a foreign key to maintain best practices: https://stackoverflow.com/questions/10982992/is-it-fine-to-have-foreign-key-as-primary-key</li> 
      </ul>
      <br>

    <button type="button" @click="getPostWithCondition">Read Posts with Condition</button><br>
      <code>usePost.query().with('author').where('id', 1).get()</code><br>

    <button type="button" @click="getPostWithNestedCondition">Read Posts with Nested Condition</button><br>
      <code>usePost.whereHas('author', (query)=>{query.where('id',1) }).with('comments').get()</code><br>

    <button type="button" @click="getPostWithMultiNestedCondition">Read Posts with Multi Nested Condition</button><br>
      <code>usePost.whereHas('author', 
                        (query)=>{query.where('id',1)
                        }).with('comments',
                        (query)=>{query.where('id',1)
                        }).get()
      </code><br>

    <br><h3>Results</h3>
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
        usePost.save(originalPosts);
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
    getPostWithAuthors(){
        //users with posts
        const users = useUser.query().with('posts').get()
        this.display.posts.push(...users)

        //posts with users
        const posts = usePost.query().with('author').get()
        this.display.posts.push(...posts)
    },
    getPostWithCondition(){
        this.display.users.length = 0
        this.display.posts.length = 0
        const posts = usePost.query().with('comments').with('author').where('id', 1).get()
        this.display.posts.push(...posts)
    },
    getPostWithNestedCondition(){
        this.display.users.length = 0
        this.display.posts.length = 0
        //const posts = usePost.with('author', (query)=>{query.where('id',1) }).with('comments').get()   <<< does not constrain authors, instead returns `null`
        const posts = usePost.whereHas('author', (query)=>{query.where('id',1) }).with('comments').get()
        this.display.posts.push(...posts)
    },
    getPostWithMultiNestedCondition(){
        this.display.users.length = 0
        this.display.posts.length = 0     /*
        const posts = usePost.whereHas('author', 
                        (query)=>{query.where('id',1)
                        }).with('comments',
                        (query)=>{query.where('author',1)
                        }).get()
        */
        //or, maybe this is better 
        const posts = useUser.where('id',1).with('posts').with('comments').get()
        this.display.posts.push(...posts)
    }
  }
};


const originalPosts = [
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
</script>