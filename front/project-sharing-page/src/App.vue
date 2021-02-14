<template>
  <v-app v-if="isLoaded">
    <router-view />
  </v-app>
</template>

<script>

export default {
  name: 'App',
  data() {
    return {
      isLoaded : false
    };
  },
  created() {

    this.isLoaded = false;
    //ログインを行う
    this.$store.dispatch("checkLogin")
        .then(() => {
          this.isLoaded = true;
        });
  }
};
</script>
