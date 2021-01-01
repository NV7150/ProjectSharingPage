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
      logined: false,
      user: null,
      navPages: [
        {name: "Home", link: "Home"}
      ]
    }
  },
  created() {
    axios.get('/userapi/user')
    .then((response)=> {
      this.user = response.data;
      this.logined = true;
    })
    .catch(() => {
      this.logined = false;
    });
  },
  methods: {
    moveTo(pageName){
      this.$router.push({name: pageName});
    },
    logout(){
      axios.post("userapi/logout");
      this.logined = false;
    }
  }
}
</script>

<style scoped>

</style>