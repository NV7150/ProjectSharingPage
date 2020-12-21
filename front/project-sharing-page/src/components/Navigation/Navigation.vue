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
      <UserMenu v-on:logout="logout"></UserMenu>
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
          v-for="page in navPages"
          @click="moveTo(page.link)"
          :key="page"
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
    let _this = this;
    axios.get('/userapi/user')
    .then(response=> {
      //TODO:loginとの分岐

      _this.user = response.data;
      _this.logined = true;
    })
    .catch(() => {
      _this.logout();
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