<template>
  <v-container
    fluid
    class="mb-5"
  >
    <v-row>
      <v-col cols="12">
        <ProjectChat :project="project"></ProjectChat>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import ProjectChat from "./ProjectChatTab/ProjectChat";
export default {
  name: "ProjectChatTab",
  components: {ProjectChat},
  props: ["project"]
}
</script>

<style scoped>

</style>