<template>
  <div v-if="!isLoading">
    <TagRegister :tag-selected="editProject" />
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
import axios from "axios";
import ErrorResolver from "@/assets/scripts/ErrorResolver";

export default {
  name: "ProjectTagEdit",
  components: {TagRegister},
  props: {
    project: {type:Object, required: true},
    fieldUpdated: {type:Function, required: true},
    loadingStateUpdated: {type:Function}
  },
  data(){
    return{
      nowTags: [],
      isLoading: false
    }
  },

  methods: {
    editProject(tag){
      for(let i = 0; i < this.nowTags.length; i++){
        if(this.nowTags[i].id === tag.id){
          return;
        }
      }
      this.nowTags.push(tag);
      this.send();
    },

    close(id){
      this.nowTags = this.nowTags.filter(tag => tag.id !== id);
      this.send();
    },

    send(){
      let tagIds = [];
      for(let i = 0; i < this.nowTags.length; i++){
        tagIds.push(this.nowTags[i].id);
      }

      this.fieldUpdated("skilltags", tagIds);
    },

    getTag(id){
      return new Promise((resolve, reject) => {
        axios
            .get("/userapi/skilltag/" + id)
            .then((response) => {
              this.nowTags.push(response.data);
              resolve();
            })
            .catch(() => {
              reject();
            });
      });
    }
  },

  created() {
    this.nowTags = [];
    let tags = this.project.skilltags;
    let tasks = [];
    for(let i = 0; i < tags.length; i++){
      tasks.push(this.getTag(tags[i]));
    }

    this.isLoading = true;
    Promise
        .all(tasks)
        .then(() => {
          this.isLoading = false;
        })
        .catch(() => {
          ErrorResolver.resolveError(this.$router);
        });
  },

  watch: {
    isLoading: function (){
      this.loadingStateUpdated(this.isLoading);
    }
  }
}
</script>

<style scoped>

</style>