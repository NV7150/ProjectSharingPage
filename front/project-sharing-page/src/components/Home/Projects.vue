<template>
  <v-container>
    <v-row v-if="!isLoading">
      <v-col
          cols="12"
          sm="6"
          md="4"
          lg="3"
          xl="2"
          v-for="(recommend, i) in recommends"
          :key="i"
      >
        <v-lazy
            v-model="isActive[i]"
            :options="{threshold: .5}"
            transition="fade-transition"
        >
          <ProjectCard :project-id="recommend"></ProjectCard>
        </v-lazy>
      </v-col>
    </v-row>
    <v-container v-else>
      <v-row align="center" justify="center" >
        <v-progress-circular
            class="ma-3"
            indeterminate
            color="primary"
            :size="100"
            :width="7"
        />
      </v-row>
      <v-row>
        <v-col class="text-center font-weight-light text--secondary">
          Loading, please wait...
        </v-col>
      </v-row>
    </v-container>
  </v-container>
</template>

<script>
import ProjectCard from "./ProjectCard";
import axios from "axios";
import ErrorResolver from "@/assets/scripts/ErrorResolver";

export default {
  name: "Projects",
  components: {ProjectCard},
  data(){
    return{
      recommends: [],
      isLoading : false,
      isActive: []
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
          for(let i = 0; i < this.recommends.length; i++){
            this.isActive.push(false);
          }
        })
        .catch(() => {
          ErrorResolver.resolveError(this.$router);
        });
  }
}
</script>

<style scoped>

</style>