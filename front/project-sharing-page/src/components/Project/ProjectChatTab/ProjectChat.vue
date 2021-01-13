<template>
  <v-card>
    <v-toolbar>
      <v-btn
        icon
        :disabled="window <= 0"
        @click="back"
      >
        <v-icon>mdi-arrow-left</v-icon>
      </v-btn>
      <v-toolbar-title>{{toolbarText}}</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-tooltip bottom>
        <template v-slot:activator="{on}">
          <v-btn
              icon
              @click="goToPage"
              v-on="on"
              :disabled="window < 2"
          >
            <v-icon>mdi-application</v-icon>
          </v-btn>
        </template>
        <span>Go to chat page</span>
      </v-tooltip>
    </v-toolbar>

    <v-row>
      <v-col cols="12">
        <v-window
          v-model="window"
        >
          <v-window-item>
            <v-card>
              <ChatDestList
                :destinations="channels"
                :selected-callback="selectChannel"
              ></ChatDestList>
            </v-card>
          </v-window-item>

          <v-window-item>
            <v-card
              :loading="isLoadingThreads"
              v-if="threadObjects.length > 0"
            >
              <template slot="progress">
                <v-progress-linear
                    color="deep-purple"
                    height="10"
                    indeterminate
                />
              </template>

              <ChatDestList
                :destinations="threadObjects"
                :selected-callback="selectThread"
              />
            </v-card>

            <v-card v-else>
              <v-card-text>
                No thread included in this channel.
              </v-card-text>
            </v-card>
          </v-window-item>

          <v-window-item>
            <v-card>
              <ChatWindow
                  :project="project"
                  :channel="selectingChannel"
                  :thread="selectingThread"
              ></ChatWindow>
              <v-spacer></v-spacer>
              <ChatInput></ChatInput>
            </v-card>
          </v-window-item>
        </v-window>
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
import axios from "axios";
import ChatDestList from "./ProjectChat/ChatDestList";
import ChatSettings from "../../../assets/scripts/ProjectPageConstants";
import ChatWindow from "./ProjectChat/ChatWindow";
import ChatInput from "./ProjectChat/ChatInput";

export default {
  name: "ProjectChat",
  props:["project"],
  components: {ChatWindow, ChatDestList, ChatInput},
  data(){
    return{
      window: 0,
      channels: ChatSettings.channels,
      selectingChannel: {},
      isLoadingThreads: false,
      threads: [],
      threadObjects : [],
      selectingThread: {}
    }
  },
  methods: {
    selectChannel(channel){
      this.selectingChannel = channel;
      this.window = 1;

      this.isLoadingThreads = true;
      axios
          .get('/chatapi/thread/project/' + this.project.id + '/' + this.selectingChannel.send)
          .then((response) => {
            this.isLoadingThreads = false;
            this.threads = response.data;
            this.threadObjects = this.getThreads();
          })
          .catch(() => {
            this.isLoadingThreads = false;
            this.threads = [];
          });
    },
    selectThread(thread){
      this.selectingThread = thread;
      this.window = 2;
    },
    back(){
      this.window--;
      if(this.window < 0){
        this.window = 0;
      }
    },
    goToPage(){
      this.$router.push({
        name: "Chat",
        params: {
          projectId: this.$route.params.projectId,
          channel: this.selectingChannel.name,
          thread: this.selectingThread.name
        }
      });
    },
    getThreads(){
      let threadObjects = [];
      for(let i = 0; i < this.threads.length; i++){
        let thread = this.threads[i];
        threadObjects.push({
          name: thread.title,
          //THREADSTATUS_****なので文字列処理
          status: thread.status.replace('THREADSTATUS_', '').toLowerCase()
        });
      }
      return threadObjects;
    }
  },
  computed: {
    toolbarText(){
      switch (this.window){
        case 1:
          return this.selectingChannel.name;
        case 2:
          return this.selectingThread.name;
      }
      return "";
    }
  }
}
</script>

<style scoped>

</style>