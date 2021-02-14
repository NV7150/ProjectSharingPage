<template>
  <v-card
    rounded
    outlined
    :loading="isLoading"
    :disabled="isLoading"
  >
    <template slot="progress">
      <v-progress-linear
          color="deep-purple"
          height="10"
          indeterminate
      >
      </v-progress-linear>
      <v-skeleton-loader
          class="mx-auto"
          type="card"
      />
    </template>

    <v-card-title>Projects</v-card-title>

    <v-divider class="my-3" />

    <v-card-text>
      <v-list v-if="!isLoading">
        <v-list-item
          v-for="(project, i) in projects"
          :key = "i"
          class="mb-2"
        >
          <UserProjectCard :project="project" height="10vh" />
        </v-list-item>
      </v-list>
    </v-card-text>

  </v-card>
</template>

<script>

import UserProjectCard from "@/components/User/UserProjects/UserProjectCard";
import axios from "axios";
import ErrorResolver from "@/assets/scripts/ErrorResolver";

export default {
  name: "UserProjects",
  components: {UserProjectCard},
  props:{
    user: {
      type: Object,
      required: true
    }
  },
  data(){
    return{
      projects: [],
      isLoading: true
    }
  },
  created() {
    this.isLoading = true;
    axios
        .get("/projectapi/project/" + this.user.username)
        .then((response) => {
          this.projects = response.data;
          this.isLoading = false;
        })
        .catch(() => {
          ErrorResolver.resolveError(this.$router);
        });
  }
}
</script>

<style scoped>
</style>