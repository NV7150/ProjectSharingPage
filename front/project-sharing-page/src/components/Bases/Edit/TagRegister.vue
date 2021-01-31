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

const CREATE_NEW = 0;

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

      axios
          .get("/userapi/skilltag/search", {params: {"keyword" : this.tagName}})
          .then((response) => {
            this.searchResult = response.data.result;
            let isFounded = false;
            for(let i = 0; i < this.searchResult.length; i++){
              if(this.searchResult[i].name === this.tagName){
                isFounded = true;
                break;
              }
            }
            if(!isFounded)
              this.searchResult.push({name: this.tagName, id: CREATE_NEW});
            this.isSearching = false;
          })
          .catch(() => {
            //TODO:エラー処理
            alert("ERROR!");
          })
    },

    selectTag(tagIndex){
      if(this.isSending || this.isSearching)
        return;

      if(tagIndex === CREATE_NEW){
        this.newTag();
      }else{
        this.tagSelected(this.searchResult[tagIndex].id);
      }
    },
    newTag(){
      let newId = 0;
      axios
          .post("/userapi/skilltag", {"name": this.tagName})
          .then((response) => {
            newId = response.data.id;
            this.tagSelected(response.data.id);
          })
          .catch(() => {
            //TODO:エラー処理
            alert("ERROR!");
          });
    }
  }
}
</script>

<style scoped>

</style>