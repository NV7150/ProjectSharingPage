<template>
  <v-card
    rounded
    outlined
    class="overflow-y-auto"
    height="500"
  >
    <v-card-title>Projects</v-card-title>
    <v-divider class="my-3"></v-divider>
    <v-card-text>
      <v-row>
        <v-col
          v-for="(project, i) in projects"
          :key="i"
          cols="12"
          sm="6"
          md="4"
          lg="3"
          xl="2"
        >
          <ProjectCard
            :project-id="project"
          ></ProjectCard>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>

import PlaceHolder from "../../assets/img/PlaceHolder.png";
import ProjectCard from "../Home/ProjectCard";

export default {
  name: "UserProjects",
  components: {ProjectCard},
  props:{
    user: {
      type: Object,
      default: function () {
        return {
          username: '',
          name: 'Loading...',
          bio: '',
          icon: PlaceHolder,
          skillTags: []
        };
      }
    }
  },
  data(){
    return{
      //仮置き
      projects: []
    }
  },
  created() {
    //TODO:プロジェクトを逆引き
    this.projects = [0, 0, 0, 0, 0, 0, 0]
  }
}
</script>

<style scoped>
</style>