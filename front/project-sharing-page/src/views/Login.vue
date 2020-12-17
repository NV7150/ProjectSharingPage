<template>
  <v-container>
    <v-row justify="center">
      <v-col lg="4" md="6" sm="7" cols="11">
        <LoginForm></LoginForm>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import LoginForm from "../components/Login/LoginForm";

export default {
  name: "Login",
  components: {LoginForm}
}
</script>

<style scoped>

</style>