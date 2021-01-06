<template>
  <v-app-bar
      app
      color="primary"
      dark
  >
    <v-toolbar-title>
      SFC21 Project Sharing Port
    </v-toolbar-title>
    <v-spacer></v-spacer>
    <template
      v-if="logined"
    >
      <UserMenu v-on:logout="logout" :user="user"></UserMenu>
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

    <template v-slot:extension>
      <v-tabs>
        <v-tab
          v-for="(page, i) in navPages"
          @click="moveTo(page.link)"
          :key="i"
        >
          {{page.name}}
        </v-tab>
      </v-tabs>
    </template>
  </v-app-bar>
</template>

<script>
import UserMenu from "./UserMenu";
import axios from "axios";

export default {
  name: "Navigation",
  components: {UserMenu},
  data(){
    return{
      navPages: [
        {name: "Home", link: "Home"}
      ]
    }
  },
  methods: {
    moveTo(pageName){
      this.$router.push({name: pageName});
    },
    logout(){
      axios.post("userapi/logout");
      this.$store.commit('removeUser');
      this.$router.push({path: this.$router.currentRoute.path, force: true});
    }
  },
  computed: {
    user(){
      return this.$store.getters['getUser'];
    },
    logined(){
      return this.$store.getters['getIsLoggedIn'];
    }
  },
  // watch: {
  //   loginUser (){
  //     this.user = this.$store.getters['getUser'];
  //     console.log(this.user);
  //     this.logined = true;
  //   }
  // }
}
</script>

<style scoped>

</style>