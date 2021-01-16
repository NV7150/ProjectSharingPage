<template>
  <v-card :loading="isLoading">

    <template slot="progress">
      <v-progress-linear
          color="deep-purple"
          height="10"
          indeterminate
      />
    </template>

    <v-toolbar>
      <v-toolbar-title>
        Users
      </v-toolbar-title>
    </v-toolbar>

    <v-container v-if="!isLoading">
      <v-row>
        <v-col
            cols="12"
            sm="6"
            md="4"
            lg="3"
            xl="2"
            v-for="(resultUser, i) in results"
            :key="i"
        >
          <UserCard :username="resultUser.username" />
        </v-col>
      </v-row>
    </v-container>
  </v-card>
</template>

<script>
import UserCard from "@/components/Search/UserSearch/UserCard";

export default {
  name: "UserSearch",
  components: {UserCard},
  props: {
    keyword: {type: String}
  },
  data(){
    return{
      //TODO:仮置き削除
      results: [{username: "tester1"}],
      isLoading: false
    };
  }
}

</script>

<style scoped>

</style>