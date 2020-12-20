<template>
  <v-container>
    <Navigation></Navigation>
    <p>This user Id is {{$route.params.projectId}}</p>
  </v-container>
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