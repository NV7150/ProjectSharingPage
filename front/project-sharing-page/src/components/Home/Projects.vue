<template>
  <v-container>
    <v-row v-if="!isLoading">
      <v-col
          cols="12"
          sm="6"
          md="4"
          lg="3"
          xl="2"
          v-for="recommend in recommends" :key="recommend"
      >
        <ProjectCard :project-id="recommend"></ProjectCard>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import ProjectCard from "./ProjectCard";
import axios from "axios";

export default {
  name: "Projects",
  components: {ProjectCard},
  data(){
    return{
      recommends: [],
      isLoading : false
    }
  },
  mounted() {
    if(!this.$store.getters["getUser"]){
      //TODO:ログイン者じゃない向けの処理
      this.recommends=[1,2,3,4];
      return;
    }


    this.isLoading = true;
    axios
        .get("/recommendapi/project")
        .then((response) => {
          this.recommends = response.data;
          this.isLoading = false;
        })
        .catch(() => {
          //TODO:エラー処理
          alert("Error in get:recommend");
        });
  }
}
</script>

<style scoped>

</style>