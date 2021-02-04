<template>
  <div>
    <TagRegister :tag-selected="editProject" />
  </div>
</template>

<script>
import TagRegister from "@/components/Bases/Edit/TagRegister";
import axios from "axios";

export default {
  name: "ProjectTagEdit",
  components: {TagRegister},
  props: {
    project: {type:Object, required: true}
  },
  data(){
    return{
      isLoading : false,
      nowTags: []
    }
  },

  methods: {
    editProject(tagId){
      if(this.nowTags.indexOf(tagId) !== -1)
        return;
      this.nowTags.push(tagId);
      this.nowTags = this.nowTags.filter(v => (typeof v) === "number");

      let newProject = {
        "skilltags": this.nowTags
      };

      this.isLoading = true;
      axios
          .patch("/projectapi/project/" + this.project.id + "?update_fields=" + JSON.stringify(newProject))
          .then(() => {
            this.isLoading = false;
          })
          .catch(() => {
            //TODO:エラー処理
            alert("ERROR in patch Project");
          });
    }
  },

  created() {
    this.nowTags = []
    let tags = this.project.skilltags;
    for(let i = 0; i < tags.length; i++){
      this.nowTags.push(tags[i]);
    }
  }
}
</script>

<style scoped>

</style>