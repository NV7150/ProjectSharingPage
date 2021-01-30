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
    <v-card :loading="isSearching || isSending">
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
          console.log(this.searchResult);
          this.isSearching = false;
        })
        .catch(() => {
          //TODO:エラー処理
          alert("ERROR!");
        })
    },
    selectTag(tagIndex){
      this.nowTags.push(this.searchResult[tagIndex].id);
      let newUser = {
        "skilltags" : this.nowTags
      };
      this.isSending = true;
      axios
          .patch("/userapi/user?json_data=" + JSON.stringify(newUser))
          .then(() => {
            this.isSending = false;
          })
          .catch(() => {
            //TODO:エラー処理
            alert("ERROR");
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