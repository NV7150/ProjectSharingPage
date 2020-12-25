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
    </v-toolbar>

    <v-row>
      <v-col cols="12">
        <v-window
          v-model="window"
        >
          <v-window-item>
            <ChatRoomList
              :rooms="categories"
              :selected-callback="selectCategory"
            ></ChatRoomList>
          </v-window-item>

          <v-window-item>
            <ChatRoomList
              :rooms="getCategoryRoom()"
              :selected-callback="selectRoom"
            ></ChatRoomList>
          </v-window-item>

          <v-window-item>
            <ChatWindow
              :chat-messages="getChatMessages()"
            ></ChatWindow>
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

export default {
  name: "ProjectChat",
  components: {ChatWindow, ChatRoomList},
  data(){
    return{
      window: 0,
      categories: ChatSettings.categories,
      selectingCategory: {},
      selectingRoom: {}
    }
  },
  methods: {
    selectCategory(category){
      this.selectingCategory = category;
      this.window = 1;
    },
    selectRoom(room){
      this.selectingRoom = room;
      this.window = 2;
    },
    getCategoryRoom(){
      //TODO:サーバからチャットルームを取得
      //仮置き
      return [
        {name: "Test1", status: "open"},
        {name: "Test2", status: "solved"},
        {name: "Test3", status: "open"}
      ];
    },
    getChatMessages(){
      //TODO:サーバからチャットを取得
      //仮置き
      return [
        {message: "これはテストです", date: 23, month: 'Dec', year:2020, user: {display_name: "テスト", icon: "https://gochiusa.com/core_sys/images/contents/00000022/base/l1.png"}},
        {message: "これはテストです2", date: 23, month: 'Dec', year:2020, user: {display_name: "テスト", icon: "https://gochiusa.com/core_sys/images/contents/00000021/base/l1.png"}}
      ]
    },
    back(){
      this.window--;
      if(this.window < 0){
        this.window = 0;
      }
    }
  },
  computed: {
    toolbarText(){
      switch (this.window){
        case 1:
          return this.selectingCategory.name;
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