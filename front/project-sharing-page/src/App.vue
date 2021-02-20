<template>
  <v-app v-if="isLoaded">
    <NavigationBar />
    <router-view class="main" />
    <Footer />
  </v-app>
</template>

<script>

import NavigationBar from "@/components/Navigation/NavigationBar";
import Footer from "@/components/Footer/Footer";
export default {
  name: 'App',
  components: {Footer, NavigationBar},
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
<style scoped>
</style>
