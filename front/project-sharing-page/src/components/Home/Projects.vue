<template>
  <v-container>
    <v-row>
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

export default {
  name: "Projects",
  components: {ProjectCard},
  data(){
    return{
      recommends: []
    }
  },
  mounted() {
    //TODO:APIからリコメンドのIDを取得
    //仮置き
    this.recommends = [0, 1, 2, 3]
    //仮置きここまで
  }
}
</script>

<style scoped>

</style>