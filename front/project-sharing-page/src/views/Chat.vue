<template>
  <v-main>
    <NavigationBar />

    <v-container>
      <v-row>
        <v-col
          cols="12"
        >
          <v-card
            :loading="isThreadLoading || isMessageLoading"
          >
            <template slot="progress">
              <v-progress-linear
                  color="deep-purple"
                  height="10"
                  indeterminate
              />
            </template>

            <v-toolbar>
              <v-btn
                  icon
                  @click="back"
              >
                <v-icon>mdi-arrow-left</v-icon>
              </v-btn>
              <v-toolbar-title
                  v-if="!isThreadLoading"
              >
                {{this.thread.title}}
              </v-toolbar-title>
            </v-toolbar>
            <ChatWindow
              v-if="!isThreadLoading"
              :thread="thread"
              :on-loading-changed="changeMessageLoadState"
            />
            <ChatInput
              v-if="!isThreadLoading"
              :thread="thread"
            />
          </v-card>
        </v-col>
      </v-row>
    </v-container>

  </v-main>
</template>

<script>
import axios from "axios";

import NavigationBar from "../components/Navigation/NavigationBar";
import ChatWindow from "../components/Project/ProjectChatTab/ProjectChat/ChatWindow";
import ChatInput from "../components/Project/ProjectChatTab/ProjectChat/ChatInput";

export default {
  name: "Chat",
  components: {ChatInput, ChatWindow, NavigationBar},
  data(){
    return {
      isThreadLoading: true,
      isMessageLoading: true,
      thread: {}
    }
  },
  methods: {
    back(){
      this.$router.push({
        name:'Project',
        params: { projectId: this.$route.params.projectId }
      });
    },
    changeMessageLoadState(state){
      this.isMessageLoading = state;
    }
  },

  created() {
    this.isThreadLoading = true;
    axios
      .get('/chatapi/thread/' + this.$route.params.threadId)
      .then((response) => {
        this.thread = response.data;
        this.isThreadLoading = false;
      })
      .catch(() => {
        this.$router.push({name: '404'});
      });
  },
}
</script>

<style scoped>

</style>