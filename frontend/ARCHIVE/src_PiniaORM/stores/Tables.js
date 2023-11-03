import { Model } from 'pinia-orm'

export class Post extends Model {
  static entity = 'posts'
  static fields () {
    return {
      id: this.attr(null),
      //post_id: this.uid(),
      user_id: this.uid(),
      author: this.belongsTo(User, 'user_id'),  // 1)author records inserted to User, with Post's foreign key 'user_id' belonging to User
                                                //   this displays in `local storage / posts` as `user_id`
                                                // 3)queries will match Post `user_id` to an `id` on User.
      body: this.string(''),
      comments: this.hasMany(Comment, 'post_id')
    }
  }
}
export class Comment extends Model {
  static entity = 'comments'
  static fields () {
    return {
      id: this.attr(null),
      user_id: this.attr(null),
      post_id: this.attr(null),
      comment: this.string(''),
      author: this.belongsTo(User, 'user_id')
    }
  }
}
export class User extends Model {
  static entity = 'users'
  static fields () {
    return {
      id: this.attr(null),
      name: this.string(''),
      age: this.number(),
      posts: this.hasMany(Post, 'user_id'),  // 2)query matches User primary key `id` to Posts' foreign key `user_id` 
      comments: this.hasMany(Comment, 'user_id')
    }
  }
}