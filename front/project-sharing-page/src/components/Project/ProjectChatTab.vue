<template>
  <v-container
    fluid
    class="mb-5"
  >
    <v-row>
      <v-col cols="12">
        <ProjectChat></ProjectChat>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import ProjectChat from "./ProjectChat/ProjectChat";
export default {
  name: "ProjectChatTab",
  components: {ProjectChat}
}
</script>

<style scoped>

</style>