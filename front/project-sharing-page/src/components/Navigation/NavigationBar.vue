<template>
  <v-app-bar
      app
      color="primary"
      dark
  >
    <v-toolbar-title @click="moveTo('Home')">
      SFC21 Project Sharing Port
    </v-toolbar-title>

    <SearchBar class="mt-7 ml-4" />

    <v-spacer></v-spacer>

    <template
      v-if="logined"
    >
      <UserMenu v-on:logout="logout" :user="user" class="mr-10 mt-4" />
    </template>
    <template
      v-else
    >
      <v-btn
        text
        @click="moveTo('Login')"
      >
        Login
      </v-btn>
    </template>
  </v-app-bar>
</template>

<script>
import UserMenu from "./NavigationBar/UserMenu";
import axios from "axios";
import SearchBar from "@/components/Navigation/NavigationBar/SearchBar";

export default {
  name: "NavigationBar",
  components: {SearchBar, UserMenu},
  methods: {
    moveTo(pageName){
      this.$router.push({name: pageName});
    },
    logout(){
      axios.post("/userapi/logout");
      this.$store.commit('removeUser');
    }
  },
  computed: {
    user(){
      return this.$store.getters['getUser'];
    },
    logined(){
      return this.$store.getters['getIsLoggedIn'];
    }
  }
}
</script>

<style scoped>

</style>