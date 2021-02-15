<template>
  <v-card :loading="isSearchLoading">

    <template slot="progress">
      <v-progress-linear
          color="deep-purple"
          height="10"
          indeterminate
      />
    </template>

    <template v-if="!isSearchLoading">
      <v-container v-if="searchResult.length > 0" class="pa-3">
        <v-row>
          <v-col
            cols="12"
            sm="6"
            md="4"
            v-for="(resultProject, i) in searchResult"
            :key="i"
          >
            <ProjectCard :project-id="resultProject.id" />
          </v-col>
        </v-row>
      </v-container>

      <v-container v-else>
        <v-row justify="center" align="center" >
          <v-col class="text-center font-weight-light">
            No projects found
          </v-col>
        </v-row>
      </v-container>
    </template>
  </v-card>
</template>

<script>
import axios from "axios";
import ProjectCard from "@/components/Home/ProjectCard";

import ErrorResolver from "@/assets/scripts/ErrorResolver";

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
            "title": this.keyword
          }
        })
        .then((response) => {
          this.searchResult = response.data.projects;
          this.isSearchLoading = false;
        })
        .catch(() => {
          ErrorResolver.resolveError(this.$router);
        });
  }


}
</script>

<style scoped>

</style>