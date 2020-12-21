<template>
  <v-main>
    <Navigation></Navigation>
    <p>This user Id is {{$route.params.projectId}}</p>
  </v-main>
</template>

<script>
import Navigation from "../components/Navigation/Navigation";

export default {
  name: "Project",
  components: {Navigation}
}
</script>

<style scoped>

</style>