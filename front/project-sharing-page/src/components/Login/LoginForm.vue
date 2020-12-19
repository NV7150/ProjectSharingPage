<template>
  <v-card>
    <v-card-title>
      Login
    </v-card-title>
    <v-form
        ref="form"
        v-model="valid"
        lazy-validation
    >
      <v-card-text>
        <v-text-field
            label="UserName"
            v-model="user.userName"
            :rules="usrNameRules"
        ></v-text-field>
        <v-text-field
            label="Password"
            v-model="user.password"
            :rules="passwordRules"
            type="password"
        >
        </v-text-field>
        <v-checkbox
            v-model="user.remember"
            label="remember-password"
        >
        </v-checkbox>
      </v-card-text>
      <v-card-actions>
        <v-btn
            :disabled="!valid"
            color="blue"
            @click="login"
        >
          Login
        </v-btn>
      </v-card-actions>
    </v-form>
  </v-card>
</template>

<script>

export default {
  name: "LoginForm",
  data(){
    return{
      valid: false,
      user: {
        userName: '',
        password: '',
        remember: false
      },
      usrNameRules : [
        value => !!value || 'Required'
      ],
      passwordRules : [
          value => !!value || 'Required'
      ]
    }
  },
  methods : {
    login(){
      axios.post()
    }
  }
}
</script>

<style scoped>

</style>