<template>
  <v-app>
    <router-view />
  </v-app>
</template>

<script>

export default {
  name: 'App',
  beforeCreate() {
    //ログインを行う
    this.$store.dispatch("checkLogin");
  }
};
</script>
