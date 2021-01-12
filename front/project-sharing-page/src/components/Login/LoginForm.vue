<template>
  <v-card>

    <v-card-title>
      Login
    </v-card-title>
    <v-form
        ref="form"
        v-model="valid"
    >
      <v-card-text>
        <div
            v-if="errorLogin"
            class="error--text"
        >
          Invalid username or password
        </div>

        <v-text-field
            label="UserName"
            v-model="user.username"
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
            v-model="user.remember_password"
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

import axios from "axios";

export default {
  name: "LoginForm",
  data(){
    return{
      valid: false,
      errorLogin: false,
      user: {
        username: '',
        password: '',
        remember_password: false
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
    error(){
      this.errorLogin = true;
    },

    login(){
      let _this = this;

      axios
          .post('/userapi/login', {
            "username": _this.user.username,
            "raw_password": _this.user.password,
            "remember_password": _this.user.remember_password
          })
          .then(() => {
            _this.$store.dispatch('checkLogin');
            _this.$router.push({
              name: 'UserPage',
              params: { userName: _this.user.username }
            });
          })
          .catch((error) => {
            let code = error.response.status;
            if (code === 401){
              _this.error();
            }else{
              //TODO:エラーページへのリダイレクト
            }
          });
    },

    mounted() {
      if(this.$store.getters.getIsLoggedIn)
        this.$router.push({name: 'UserPage', params: {userName : this.$store.state.user.username}});
    }
  }
}
</script>

<style scoped>

</style>