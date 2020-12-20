<template>
  <v-container>
    <Navigation></Navigation>
    <p> {{$route.params.userName}} 's user page.</p>
  </v-container>
</template>

<script>
import Navigation from "../components/Navigation/Navigation";

export default {
  name: "User",
  components: {Navigation}
}
</script>

<style scoped>

</style>