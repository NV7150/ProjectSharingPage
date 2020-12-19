<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <v-btn
          text
          color="real accent-4"
          @click="toLogin"
      >
        Login
      </v-btn>
    </v-app-bar>

    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script>

export default {
  name: 'App',

  components: {
  },

  data: () => ({
    //
  }),
  methods: {
    toLogin(){
      this.$router.push({name: 'Login'})
    }
  }
};
</script>
