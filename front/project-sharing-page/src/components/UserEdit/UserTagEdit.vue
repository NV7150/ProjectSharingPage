<template>
  <div>
    <TagRegister :tag-selected="editTag" />
  </div>
</template>

<script>
import axios from "axios";
import TagRegister from "@/components/Bases/Edit/TagRegister";

export default {
  name: "UserTagEdit",
  components: {TagRegister},
  props: {
    user : {type: Object}
  },
  data(){
    return{
      nowTags : []
    };
  },

  methods: {
    editTag(tagId) {
      if(this.nowTags.indexOf(tagId) !== -1)
        return;

      this.nowTags.push(tagId);
      let newUser = {
        "skilltags": this.nowTags
      };

      this.isSending = true;
      axios
          .patch("/userapi/user?json_data=" + JSON.stringify(newUser))
          .then(() => {
            this.isSending = false;
          })
          .catch(() => {
            alert("ERROR in patch user")
          });
    },
  },

  created() {
    this.nowTags = [];
    let tags = this.user.skilltags;
    for(let i = 0; i < tags.length; i++){
      this.nowTags.push(tags[i].id);
    }
  }
}
</script>

<style scoped>

</style>