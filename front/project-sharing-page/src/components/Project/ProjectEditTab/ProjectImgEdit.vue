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
  watch: {
    imgFile: function (){
      this.imgUploaded(this.imgFile);
    }
  }
}
</script>

<style scoped>

</style>