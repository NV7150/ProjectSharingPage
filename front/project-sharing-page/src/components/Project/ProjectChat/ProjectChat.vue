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
            <v-card>
              <ChatRoomList
                :rooms="getRooms()"
                :selected-callback="selectRoom"
              ></ChatRoomList>
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
import ChatRoomList from "./ChatRoomList";
import ChatSettings from "../../../assets/scripts/ProjectPageSettings";
import ChatWindow from "./ChatWindow";
import ChatInput from "./ChatInput";

export default {
  name: "ProjectChat",
  props:["project"],
  components: {ChatWindow, ChatRoomList, ChatInput},
  data(){
    return{
      window: 0,
      channels: ChatSettings.channels,
      selectingChannel: {},
      selectingRoom: {}
    }
  },
  methods: {
    selectChannel(channel){
      this.selectingChannel = channel;
      this.window = 1;
    },
    selectRoom(room){
      this.selectingRoom = room;
      this.window = 2;
    },
    getRooms(){
      //TODO:サーバからチャットルームを取得
      //仮置き
      return [
        {name: "Test1", status: "open"},
        {name: "Test2", status: "solved"},
        {name: "Test3", status: "open"}
      ];
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