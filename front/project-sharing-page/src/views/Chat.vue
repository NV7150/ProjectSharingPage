<template>
  <v-main>
    <Navigation />

    <v-container>
      <v-row>
        <v-col
          cols="12"
        >
          <v-card>
            <v-toolbar>
              <v-btn
                  icon
                  :disabled="window <= 0"
                  @click="back"
              >
                <v-icon>mdi-arrow-left</v-icon>
              </v-btn>
              <v-toolbar-title>{{$route.params.room}}</v-toolbar-title>
            </v-toolbar>
            <ChatWindow :project="project" :channel="channel" :room="thread" />
            <ChatInput />
          </v-card>
        </v-col>
      </v-row>
    </v-container>

  </v-main>
</template>

<script>
import axios from "axios";

import Navigation from "../components/Navigation/Navigation";
import ChatWindow from "../components/Project/ProjectChatTab/ProjectChat/ChatWindow";
import ChatInput from "../components/Project/ProjectChatTab/ProjectChat/ChatInput";

export default {
  name: "Chat",
  components: {ChatInput, ChatWindow, Navigation},
  data(){
    return {
      project: {},
      channel: {},
      thread: {}
    }
  },
  methods: {
    back(){
      this.$router.push({
        name:'Project',
        params: { projectId: this.$route.params.projectId }
      });
    }
  },

  created() {
    this.project =
        axios
            .get('/projectapi/project/' + this.$route.params.userId)
            .then((response) => {
              this.project = response.data;
            })
            .catch(() => {
              //TODO:エラーページへ飛ばす
            });

    //TODO:チャンネルとルームを取得
    this.channel = {name: this.$route.params.channel};
    this.thread = {name: this.$route.params.room};
  },
}
</script>

<style scoped>

</style>