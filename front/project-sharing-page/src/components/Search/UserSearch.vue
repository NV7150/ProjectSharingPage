<template>
  <v-card :loading="isLoading" :disabled="isLoading">

    <template slot="progress">
      <v-progress-linear
          color="deep-purple"
          height="10"
          indeterminate
      />
    </template>

    <template v-if="!isLoading">
      <v-container v-if="results.length > 0">
        <v-row>
          <v-col
              cols="12"
              sm="6"
              md="4"
              v-for="(resultUser, i) in results"
              :key="i"
          >
            <UserCard :username="resultUser.username" />
          </v-col>
        </v-row>
      </v-container>

      <v-container v-else>
        <v-row justify="center" align="center" >
          <v-col class="text-center font-weight-light">
            No users found
          </v-col>
        </v-row>
      </v-container>
    </template>
  </v-card>
</template>

<script>
import UserCard from "@/components/Search/UserSearch/UserCard";
import axios from "axios";

import ErrorResolver from "@/assets/scripts/ErrorResolver";

export default {
  name: "UserSearch",
  components: {UserCard},
  props: {
    keyword: {type: String}
  },
  data(){
    return{
      results: [],
      isLoading: false,
    };
  },
  created() {
    this.isLoading = true;
    axios
        .get("/userapi/user/search", {
          params: {
            keyword: this.keyword
          }
        })
        .then((response) => {
          this.results = response.data.all_result;
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