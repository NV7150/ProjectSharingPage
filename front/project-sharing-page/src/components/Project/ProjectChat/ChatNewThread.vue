<template>
  <v-card class="pa-3">
    <v-card-title class="headline grey lighten-2">
      新規スレッド
    </v-card-title>
    <v-text-field
        v-model="newThreadName"
        label="スレッド名"
        class="mt-3 mb-3"
    />
    <v-card-actions>
      <v-btn :disabled="!newThreadName" @click="createThread">
        新規作成
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import axios from "axios";

export default {
  name: "ChatNewThread",
  props: {
    project: {type: Object, required: true},
    type: {type: String, required: true},
    selected: {type: Function}
  },
  data(){
    return{
      newThreadName: ""
    };
  },
  methods:{
    createThread(){
      axios
          .post("/chatapi/thread", {
            type: this.type,
            project_id: this.project.id,
            title: this.newThreadName})
          .then(() => {
            this.selected();
          });
    }
  }
}
</script>

<style scoped>

</style>