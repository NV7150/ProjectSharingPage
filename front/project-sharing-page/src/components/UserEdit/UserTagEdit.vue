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
    <v-card :loading="isSearching || isSending" v-show="searchResult.length > 0">
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
  name: "UserTagEdit",
  props: {
    user : {type: Object}
  },

  data(){
    return{
      tagName : "",
      searchResult : [],
      isSearching : false,
      isSending : false,
      nowTags : []
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
        this.editTag(this.searchResult[tagIndex].id);
      }
    },
    editTag(tagId){
      return new Promise( (resolve, reject) => {
        this.nowTags.push(tagId);
        let newUser = {
          "skilltags" : this.nowTags
        };
        this.isSending = true;
        axios
            .patch("/userapi/user?json_data=" + JSON.stringify(newUser))
            .then(() => {
              this.isSending = false;
              resolve();
            })
            .catch(() => {
              reject();
            });
      });

    },
    newTag(){
      let newId = 0;
      let createTagDel = () => {
        return new Promise((resolve, reject) => {
          axios
              .post("/userapi/skilltag", {"name": this.tagName})
              .then((response) => {
                newId = response.data.id;
                resolve();
              })
              .catch(() => {
                reject();
              });
        });
      }
      Promise
          .resolve()
          .then(createTagDel)
          .then(() => {
            return new Promise((resolve, reject) => {
              this.editTag(newId).then(() => {resolve();}).catch(() => {reject();});
            });
          })
          .catch(() => {
            //TODO:エラー処理
            alert("ERROR!")
          })
    }
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