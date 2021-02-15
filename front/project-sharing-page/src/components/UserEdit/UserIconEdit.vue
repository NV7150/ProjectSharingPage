<template>
  <div>
    <v-file-input
        v-if="!isLoading"
        v-model="iconFile"
        accept="image/*"
        show-size
        label="アイコン画像"
    />
<!--    <v-btn @click="upload">-->
<!--      Upload-->
<!--    </v-btn>-->
  </div>
</template>

<script>
import axios from "axios";
import ErrorResolver from "@/assets/scripts/ErrorResolver";

export default {
  name: "UserIconEdit",
  props: {
    imgUploaded: {type: Function, required: true}
  },
  data(){
    return{
      iconFile : null,
      isLoading : false
    };
  },
  methods: {
    upload(){
      if(this.iconFile === null)
        return;
      this.isLoading = true;
      Promise
          .resolve()
          .then(this.uploadUserIcon)
          .then(() => {
            this.isLoading = false;
          })
          .catch(() => {
            ErrorResolver.resolveError(this.$router);
          });
    },
    uploadUserIcon(){
      return new Promise((resolve, reject) => {

        if(this.iconFile === null)
          reject();
        let formData = new FormData();
        formData.append("file", this.iconFile);

        axios
          .post("/userapi/usericon", formData)
          .then(() => {
            resolve();
          })
          .catch(() => {
            reject();
          });
      });
    },
  },
  watch: {
    iconFile: function (){
      this.uploadUserIcon(this.iconFile);
    }
  }
}
</script>

<style scoped>

</style>