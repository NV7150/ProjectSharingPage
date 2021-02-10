<template>
  <v-main>
    <NavigationBar />
    <v-container>
      <v-row>
        <v-col>
          <ProjectCreator />
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script>
import NavigationBar from "@/components/Navigation/NavigationBar";
import ProjectCreator from "@/components/CreateProject/ProjectCreator";
export default {
  name: "CreateProject",
  components: {ProjectCreator, NavigationBar}
}
</script>

<style scoped>

</style>