<template>
  <div>单文件组件：{{ content }}</div>
</template>

<script>
export default {
  data: function () {
    return {
      content: 'hello!'
    }
  }
}
</script>

<style scoped>
</style>
