<template>
  <div id="app">
    <TopBar></TopBar>
    <router-view></router-view>
  </div>
</template>

<script>
import TopBar from "@/components/TopBar";
export default {
  name: 'App',
  components: {TopBar},
}
</script>

<style scoped lang="css">
#app{
  width:100%;
}

</style>
