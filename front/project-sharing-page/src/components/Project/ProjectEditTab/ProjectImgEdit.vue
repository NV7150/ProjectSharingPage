<template>
  <div>
    <v-file-input
        v-model="imgFile"
        accept="image/*"
        show-size
        label="プロジェクト画像"
    />
  </div>
</template>

<script>
// import axios from "axios";

export default {
  name: "ProjectImgEdit",
  props: {
    project : {type: Object, required: true},
    imgUploaded: {type: Function, required: true}
  },
  data(){
    return{
      imgFile : null
    };
  },
  // methods: {
  //   upload(){
  //     if(this.imgFile === null)
  //       return;
  //
  //     let formData = new FormData();
  //     formData.append("file", this.imgFile);
  //
  //     this.isLoading = true;
  //     axios
  //         .post("/projectapi/projectimage/" + this.project.id, formData)
  //         .then(() => {
  //           this.isLoading = false;
  //         })
  //         .catch(() => {
  //           //TODO:エラー処理
  //           alert("Error!");
  //         });
  //   }
  // },
  watch: {
    imgFile: function (){
      this.imgUploaded(this.imgFile);
    }
  }
}
</script>

<style scoped>

</style>