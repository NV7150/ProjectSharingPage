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
              <ChatRoomList
                :rooms="channels"
                :selected-callback="selectChannel"
              ></ChatRoomList>
            </v-card>
          </v-window-item>

          <v-window-item>
            <v-card
              :loading="isLoadingRooms"
              v-if="roomObjects.length > 0"
            >
              <template slot="progress">
                <v-progress-linear
                    color="deep-purple"
                    height="10"
                    indeterminate
                />
              </template>

              <ChatRoomList
                :rooms="roomObjects"
                :selected-callback="selectRoom"
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
                  :room="selectingRoom"
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
import ChatRoomList from "./ProjectChat/ChatRoomList";
import ChatSettings from "../../../assets/scripts/ProjectPageConstants";
import ChatWindow from "./ProjectChat/ChatWindow";
import ChatInput from "./ProjectChat/ChatInput";

export default {
  name: "ProjectChat",
  props:["project"],
  components: {ChatWindow, ChatRoomList, ChatInput},
  data(){
    return{
      window: 0,
      channels: ChatSettings.channels,
      selectingChannel: {},
      isLoadingRooms: false,
      rooms: [],
      roomObjects : [],
      selectingRoom: {}
    }
  },
  methods: {
    selectChannel(channel){
      this.selectingChannel = channel;
      this.window = 1;

      this.isLoadingRooms = true;
      axios
          .get('/chatapi/thread/project/' + this.project.id + '/' + this.selectingChannel.send)
          .then((response) => {
            this.isLoadingRooms = false;
            this.rooms = response.data;
            this.roomObjects = this.getRooms();
          })
          .catch(() => {
            this.isLoadingRooms = false;
            this.rooms = [];
          });
    },
    selectRoom(room){
      this.selectingRoom = room;
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
          room: this.selectingRoom.name
        }
      });
    },
    getRooms(){
      let roomObjects = [];
      for(let i = 0; i < this.rooms.length; i++){
        let room = this.rooms[i];
        roomObjects.push({
          name: room.title,
          //THREADSTATUS_****なので文字列処理
          status: room.status.replace('THREADSTATUS_', '').toLowerCase()
        });
      }
      return roomObjects;
    }
  },
  computed: {
    toolbarText(){
      switch (this.window){
        case 1:
          return this.selectingChannel.name;
        case 2:
          return this.selectingRoom.name;
      }
      return "";
    }
  }
}
</script>

<style scoped>

</style>