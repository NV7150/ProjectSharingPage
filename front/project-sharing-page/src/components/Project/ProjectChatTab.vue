<template>
  <v-container
    fluid
    class="mb-5"
  >
    <v-row>
      <v-col cols="12">
        <ProjectChat
            :project="project"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import ProjectChat from "./ProjectChatTab/ProjectChat";
export default {
  name: "ProjectChatTab",
  components: {ProjectChat},
  props:{
    project : {Type: Object, required : true}
  },
  methods: {
    channelChanged(selectId){
      this.$router.push({
        path: this.$router.currentRoute.path,
        query: {

        }
      });
    }
  }
}
</script>

<style scoped>

</style>