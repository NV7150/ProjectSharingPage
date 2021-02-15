<template>
  <v-container>
    <v-container v-if="!isLoading">
      <v-row>
        <v-col
            cols="12"
            sm="6"
            md="4"
            lg="3"
            xl="2"
            v-for="(recommend, i) in recommends"
            :key="i"
        >
          <ProjectCard :project-id="recommend"></ProjectCard>
        </v-col>
      </v-row>

      <div class="text-center">
        <v-pagination v-model="page" :length="length" />
      </div>
    </v-container>

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
import axios from "axios";

import ProjectCard from "./ProjectCard";

import ErrorResolver from "@/assets/scripts/ErrorResolver";
import HomeConsts from "@/assets/scripts/HomeConsts";

export default {
  name: "Projects",
  components: {ProjectCard},
  data(){
    return{
      length: 0,
      recommends: [],
      isLoading : false,
      page: 1
    }
  },
  methods: {
    getCount(){
      return new Promise((resolve, reject) => {
        axios
            .get("/projectapi/project/count")
            .then((response) => {
              this.length = Math.floor((Number)(response.data) / HomeConsts.projectPerPage) + 1;
              this.page = 1;
              resolve();
            })
            .catch(() => {
              reject();
            });
      })
    },

    getLoginRecommend(){
      return new Promise((resolve, reject) => {
        axios
            .get("/recommendapi/project", {
              params: {
                limit: HomeConsts.projectPerPage,
                offset: (this.page - 1) * HomeConsts.projectPerPage
              }
            })
            .then((response) => {
              this.responseRecommend(response.data);
              resolve();
            })
            .catch(() => {
              reject();
            });
      });
    },
    getNotLoginRecommend(){
      return new Promise((resolve, reject) => {
        axios
            .get("/recommendapi/project/no-user", {
              params: {
                limit: HomeConsts.projectPerPage,
                offset: (this.page - 1) * HomeConsts.projectPerPage
              }
            })
            .then((response) => {
              this.responseRecommend(response.data);
              resolve();
            })
            .catch(() => {
              reject();
            });
      });
    },
    responseRecommend(data){
      this.recommends = data;
    },


    getRecommend(){
      let user = this.$store.getters["getUser"];
      if(!user || !user["skilltags"].length || user["skilltags"].length <= 0){
        return this.getNotLoginRecommend();
      }
      return this.getLoginRecommend();
    }
  },

  created() {

    this.isLoading = true;
    Promise.resolve()
        .then(this.getCount)
        .then(this.getRecommend)
        .then(() => {
          this.isLoading = false;
        })
        .catch(() => {
          ErrorResolver.resolveError(this.$router);
        });
  },

  watch: {
    page: function (){
      this.isLoading = true;
      this.getRecommend()
          .then(() => {
            this.isLoading = false;
          })
          .catch(() => {
            ErrorResolver.resolveError(this.$router);
          });
    }
  }
}
</script>

<style scoped>

</style>