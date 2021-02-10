<template>
  <div>
    <TagRegister :tag-selected="editTag" />
  </div>
</template>

<script>
import TagRegister from "@/components/Bases/Edit/TagRegister";

export default {
  name: "UserTagEdit",
  components: {TagRegister},
  props: {
    user : {type: Object, required: true},
    fieldUpdated: {type: Function, required: true}
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
      this.fieldUpdated("skilltags", this.nowTags);
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