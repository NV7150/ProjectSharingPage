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
            v-model="userName"
            :rules="usrNameRules"
        ></v-text-field>
        <v-text-field
            label="Password"
            v-model="password"
            :rules="passwordRules"
            type="password"
        >
        </v-text-field>
        <v-checkbox
            v-model="rememberUser"
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
      userName : '',
      usrNameRules : [
        value => !!value || 'Required'
      ],
      password : '',
      passwordRules : [
          value => !!value || 'Required'
      ],
      rememberUser: false
    }
  },
  methods : {
    login(){
      this.$refs.form.validate()
      //TODO:ログイン処理
      alert('login:' + this.userName + " " + this.password)
    }
  }
}
</script>

<style scoped>

</style>