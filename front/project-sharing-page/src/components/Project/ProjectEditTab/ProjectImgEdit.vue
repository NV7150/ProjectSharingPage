<template>
  <div>
    <v-file-input
        v-if="!isLoading"
        v-model="imgFile"
        accept="image/*"
        show-size
        label="プロジェクト画像"
    />
    <v-btn @click="upload">
      Upload
    </v-btn>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ProjectImgEdit",
  props: {
    project : {type: Object},
    onLoadStateChanged: {type: Function}
  },
  data(){
    return{
      isLoading: false,
      imgFile : null
    };
  },
  methods: {
    upload(){
      if(this.imgFile === null)
        return;

      let formData = new FormData();
      formData.append("file", this.imgFile);

      this.isLoading = true;
      axios
          .post("/projectapi/projectimage/" + this.project.id, formData)
          .then(() => {
            this.isLoading = false;
          })
          .catch(() => {
            //TODO:エラー処理
            alert("Error!");
          });
    }
  },

  watch: {
    isLoading : function (){
      this.onLoadStateChanged(this.isLoading);
    }
  }
}
</script>

<style scoped>

</style>