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
      <UserMenu></UserMenu>
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

export default {
  name: "Navigation",
  data(){
    return{
      navPages: [
        {name: "Home", link: "Home"}
      ]

    }
  },
  components: {UserMenu},
  computed: {
    logined(){
      //TODO:ログイン状態を取得
      return true;
    }
  },
  methods: {
    moveTo(pageName){
      this.$router.push({name: pageName});
    },
  }
}
</script>

<style scoped>

</style>