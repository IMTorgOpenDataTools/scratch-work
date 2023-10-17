<template>
    <div>
        <h1>{{msg}}</h1>
        <Test/>
    </div>
</template>
  
<script>
import Test from '@/components/Test3.vue'

export default {
  name: `App`,
  components:{
    Test
  },
  data() {
    return {
      msg:'Hi!'
    };
  }
};



</script>