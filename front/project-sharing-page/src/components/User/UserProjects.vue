<template>
  <v-card
    rounded
    outlined
  >
    <v-card-title>Projects</v-card-title>

    <v-divider class="my-3"></v-divider>

    <v-card-text>
      <v-list>
        <v-list-item
          v-for="(project, i) in projects"
          :key = "i"
          class="mb-2"
        >
          <UserProjectCard :project-id="project" height="10vh" />
        </v-list-item>
      </v-list>
    </v-card-text>

  </v-card>
</template>

<script>

import PlaceHolder from "../../assets/img/PlaceHolder.png";
import UserProjectCard from "@/components/User/UserProjects/UserProjectCard";

export default {
  name: "UserProjects",
  components: {UserProjectCard},
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
    this.projects = [1, 2, 3, 1, 2, 3, 1]
  }
}
</script>

<style scoped>
</style>