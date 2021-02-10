<template>
  <div>
    <TagRegister :tag-selected="editTag" />
    <div class="d-flex flex-row flex-wrap pa-3">
      <v-chip
          v-for="(tag, i) in nowTags"
          :key="i"
          close
          @click:close="close(tag.id)"
          class="mr-2 mb-4"
      >
        {{tag.name}}
      </v-chip>
    </div>
  </div>
</template>

<script>
import TagRegister from "@/components/Bases/Edit/TagRegister";
import _ from "lodash";

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
    editTag(tag) {
      for(let i = 0; i < this.nowTags.length; i++){
        if(this.nowTags[i].id === tag.id){
          return;
        }
      }

      this.nowTags.push(tag);
      this.send();
    },
    close(id) {
      this.nowTags = this.nowTags.filter(tag => tag.id !== id);
      this.send();
    },
    send(){
      let tagIds = [];
      for(let i = 0; i < this.nowTags.length; i++){
        tagIds.push(this.nowTags[i].id);
      }
      console.log(tagIds);

      this.fieldUpdated("skilltags", tagIds);
    },
  },

  created() {
    this.nowTags = _.cloneDeep(this.user.skilltags);
    console.log(this.nowTags);
  }
}
</script>

<style scoped>

</style>