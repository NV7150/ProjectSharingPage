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
      <v-dialog v-model="createDialog">
        <template v-slot:activator="{on, attrs}">
          <v-btn
              v-show="window === 1 && canCreateThread"
              icon
              v-bind="attrs"
              v-on="on"
          >
            <v-icon color="primary">mdi-plus</v-icon>
          </v-btn>
        </template>
        <ChatNewThread :project="project" :type="selectingChannel.send" :selected="threadNewCreated" />
      </v-dialog>
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
            <v-card
              :loading="isLoadingMessages"
            >
              <template slot="progress">
                <v-progress-linear
                    color="deep-purple"
                    height="10"
                    indeterminate
                />
              </template>
              <ChatWindow
                  :thread="selectingThread"
                  :on-loading-changed="changeLoadingMessage"
              />
              <v-spacer></v-spacer>
              <ChatInput
                  :thread="selectingThread"
              />
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
import ChatSettings from "../../assets/scripts/ProjectPageConstants";
import ChatWindow from "./ProjectChat/ChatWindow";
import ChatInput from "./ProjectChat/ChatInput";
import ChatNewThread from "@/components/Project/ProjectChat/ChatNewThread";
import ProjectPageConstants from "../../assets/scripts/ProjectPageConstants";

export default {
  name: "ProjectChat",
  props:{
    project : {Type: Object, required : true},
    channelSelected : {Type: Function},
    channelId : {Type: Number, default: -1},
    threadSelected: {Type:Function},
    threadId : {Type: Number, default: -1},
    selectReset: {Type:Function}
  },
  components: {ChatNewThread, ChatWindow, ChatDestList, ChatInput},
  data(){
    return{
      window: 0,
      channels: ChatSettings.channels,
      selectingChannel: {},
      isLoadingThreads: false,
      isLoadingMessages: true,
      threads: [],
      threadObjects : [],
      selectingThread: {},
      createDialog: false,
    }
  },
  methods: {
    selectChannel(channel){
      this.selectingChannel = channel;
      this.window = 1;
      this.loadThread();

      this.channelSelected(this.selectingChannel.id);
    },

    loadThread(){
      return new Promise((resolve, reject) => {
        this.isLoadingThreads = true;
        axios
            .get('/chatapi/thread/project/' + this.project.id + '/' + this.selectingChannel.send)
            .then((response) => {
              this.isLoadingThreads = false;
              this.threads = response.data;
              this.threadObjects = this.getThreads();
              resolve();
            })
            .catch(() => {
              this.isLoadingThreads = false;
              this.threads = [];
              reject();
            });
      });
    },

    selectThread(thread){
      this.selectingThread = thread;
      this.window = 2;

      this.threadSelected(this.selectingChannel.id, this.selectingThread.id);
    },
    back(){
      this.window--;
      if(this.window < 0){
        this.window = 0;
      }
      switch (this.window){
        case 0:
          this.selectReset();
          break;
        case 1:
          this.channelSelected(this.selectingChannel.id);
          break;
        default:
          this.selectReset();
          break;
      }
    },

    getThreads(){
      let threadObjects = [];
      for(let i = 0; i < this.threads.length; i++){
        let thread = this.threads[i];
        threadObjects.push({
          id: thread.id,
          name: thread.title,
          //THREADSTATUS_****なので文字列処理
          status: thread.status.replace('THREADSTATUS_', '').toLowerCase()
        });
      }
      return threadObjects;
    },

    changeLoadingMessage(next){
      this.isLoadingMessages = next;
    },

    checkThread(){
      if(this.threadId !== -1){
        let threads = this.getThreads();
        for(let threadKey in threads){
          if(!Object.prototype.hasOwnProperty.call(threads, threadKey))
            continue;

          let thread = threads[threadKey];
          if(thread.id === this.threadId){
            this.selectingThread = thread;
            this.window = 2;
            break;
          }
        }
      }
    },

    checkInit(){
      if(this.channelId !== -1){
        for(let channelKey in this.channels){
          if(!Object.prototype.hasOwnProperty.call(this.channels, channelKey))
            continue;

          let channel = this.channels[channelKey];
          if(channel.id === this.channelId){
            this.selectingChannel = channel;
            this.loadThread().then(() => {this.checkThread();});
            this.window = 1;
            break;
          }
        }
      }
    },

    threadNewCreated(){
      this.createDialog = false;
      this.$router.go({path: this.$router.currentRoute.path, force: true});
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
    },
    canCreateThread(){
      if(this.selectingChannel.canCreate === ProjectPageConstants.canCreateEveryone)
        return true;
      let memberProp = ProjectPageConstants.memberTypes[this.selectingChannel.canCreate].prop;
      return this.project[memberProp].indexOf(this.$store.getters["getUser"]) !== -1;
    }
  },

  created() {
    this.checkInit();
  }
}
</script>

<style scoped>

</style>