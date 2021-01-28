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
  data(){
    return{
      tagName : "",
      searchResult : [],
      isSearching : false,
      isSending : false
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
    selectTag(tag){
      let data = new FormData();
      data.append("skilltags", [tag]);
      this.isSending = true;
      axios
          .patch("/userapi/user", data)
          .then(() => {
            this.isSending = false;
          })
          .catch(() => {
            //TODO:エラー処理
            alert("ERROR");
          })
    }
  }

}
</script>

<style scoped>

</style>