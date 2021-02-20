<template>
  <v-main>
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
import ProjectCreator from "@/components/CreateProject/ProjectCreator";
export default {
  name: "CreateProject",
  components: {ProjectCreator}
}
</script>

<style scoped>

</style>