<template>
  <v-card :loading="isSearchLoading">

    <template slot="progress">
      <v-progress-linear
          color="deep-purple"
          height="10"
          indeterminate
      />
    </template>

    <v-toolbar>
      <v-toolbar-title>
        Projects
      </v-toolbar-title>
    </v-toolbar>

    <v-container v-if="!isSearchLoading" class="pa-3">
      <v-row>
        <v-col
          cols="12"
          sm="6"
          md="4"
          lg="3"
          xl="2"
          v-for="(resultProject, i) in searchResult"
          :key="i"
        >
          <ProjectCard :project-id="resultProject.id" />
        </v-col>
      </v-row>
    </v-container>
  </v-card>
</template>

<script>
import axios from "axios";
import ProjectCard from "@/components/Home/ProjectCard";

export default {
  name: "ProjectSearch",
  components: {ProjectCard},
  props: {
    keyword : {type:String}
  },
  data(){
    return {
      isSearchLoading : true,
      searchResult : []
    };
  },

  created() {
    axios.get("/projectapi/project/search",
        {
          params: {
            "title": this.keyword,
            "limit": 99999,
            "offset": 0
          }
        })
        .then((response) => {
          this.searchResult = response.data.projects;
          this.isSearchLoading = false;
        })
        .catch(() => {
          this.$router.push("404");
        });
  }


}
</script>

<style scoped>

</style>