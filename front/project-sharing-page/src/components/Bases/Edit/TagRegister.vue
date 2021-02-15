<template>
  <v-menu
      offset-y
      :close-on-click="true"
  >
    <template v-slot:activator="{on}">
      <v-text-field
          slot="activator"
          v-model="tagName"
          label="タグ"
          @keydown.enter="searchTag"
          v-on="on"
      />
    </template>
    <v-card :loading="isSearching" v-show="searchResult.length > 0">
      <v-list>
        <v-list-item
            v-for="(item, i) in searchResult"
            :key="i"
            @click="selectTag(i)"
        >
          {{item.name}}
        </v-list-item>
      </v-list>
    </v-card>
  </v-menu>
</template>

<script>
import axios from "axios";
import ErrorResolver from "@/assets/scripts/ErrorResolver";

const CREATE_NEW = -1;

export default {
  name: "TagRegister",

  props: {
    tagSelected: {type: Function}
  },

  data(){
    return{
      tagName : "",
      searchResult : [],
      isSearching : false
    };
  },
  methods: {
    searchTag(){
      this.isSearching = true;
      let searchingTag = this.tagName;

      axios
          .get("/userapi/skilltag/search", {params: {"keyword" : searchingTag}})
          .then((response) => {
            this.searchResult = response.data.result;
            let isFounded = false;
            for(let i = 0; i < this.searchResult.length; i++){
              if(this.searchResult[i].name === searchingTag){
                isFounded = true;
                break;
              }
            }
            if(!isFounded)
              this.searchResult.push({name: this.tagName, id: CREATE_NEW});
            this.isSearching = false;
          })
          .catch(() => {
            ErrorResolver.resolveError(this.$router);
          });
    },

    selectTag(tagIndex){
      if(this.isSearching)
        return;

      let tag = this.searchResult[tagIndex];
      if(tag.id === CREATE_NEW){
        this.newTag();
      }else{
        this.tagSelected(tag);
      }
    },
    newTag(){
      axios
          .post("/userapi/skilltag", {"name": this.tagName})
          .then((response) => {
            this.tagSelected(response.data);
          })
          .catch(() => {
            ErrorResolver.resolveError(this.$router);
          });
    }
  }
}
</script>

<style scoped>

</style>