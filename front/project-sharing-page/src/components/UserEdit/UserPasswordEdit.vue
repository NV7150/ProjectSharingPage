<template>
  <v-card class="pa-3">
    <p v-if="isMistake" class="error--text">
      現在のパスワードが違います
    </p>
    <v-text-field
        v-model="oldPassword"
        label="現在のパスワード"
        class="mb-3"
        type="password"
    />
    <v-text-field
        v-model="newPassword"
        label="新しいパスワード"
        class="mb-3"
        type="password"
    />

    <v-btn
        :disabled="oldPassword.length <= 0 || newPassword.length <= 0"
        @click="send"
    >
      send
    </v-btn>
  </v-card>
</template>

<script>
import axios from "axios";

import ErrorResolver from "@/assets/scripts/ErrorResolver";

export default {
  name: "UserPasswordEdit",
  data(){
    return{
      isLoading: false,
      oldPassword: "",
      newPassword: "",
      isMistake : false
    };
  },
  methods: {
    send(){
      if(this.oldPassword.length <= 0 || this.newPassword.length <= 0){
        return;
      }

      this.isLoading = true;
      axios
          .patch("/userapi/password", {
            old_password: this.oldPassword,
            new_password: this.newPassword
          })
          .then(() => {
            this.isLoading = false;
            this.$router.push({name: "UserPage",
              params: {
                userName: this.$store.getters["getUser"].username
              }
            })
          })
          .catch((err) => {
            if(err.response.status === 400){
              this.isMistake = true;
            }else{
              ErrorResolver.resolveError(this.$router);
            }
          });
    }
  }
}
</script>

<style scoped>

</style>