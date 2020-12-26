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
            <ChatWindow :project="project" :channel="channel" :room="room" />
            <ChatInput />
          </v-card>
        </v-col>
      </v-row>
    </v-container>

  </v-main>
</template>

<script>
import Navigation from "../components/Navigation/Navigation";
import ChatWindow from "../components/Project/ProjectChat/ChatWindow";
import ChatInput from "../components/Project/ProjectChat/ChatInput";

export default {
  name: "Chat",
  components: {ChatInput, ChatWindow, Navigation},
  data(){
    return {
      project: {},
      channel: {},
      room: {}
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
    //TODO:プロジェクトをAPIから取得
    this.project = {
      title: "Test",
      titleColor: "#1E88E5",
      keyImage: "https://gochiusa.com/bloom/core_sys/images/main/home/main_img2_4.jpg",
      about: "これはテストです",
      description:"これはテストですこれはテストですこれはテストですこれはテストですこれはテストですこれはテストですこれはテストですYpaaaaaaaこれはテストですこれはテストですこれはテストですこれはテストですこれはテストですこれはテストですこれはテストです",
      members: [
        {display_name: 'テスト1', icon: "https://gochiusa.com/core_sys/images/contents/00000022/base/l1.png"},
        {display_name: 'テスト2', icon: "https://gochiusa.com/core_sys/images/contents/00000021/base/l1.png"}
      ],
      tags: ['Python', 'Web', 'Society', 'Design', 'Software', 'Ypaaaaaaaaaaaaaaa'],
      sns: [
        {name: "twitter", link: "https://twitter.com/publicClassMain"},
        {name: "facebook", link: ""},
        {name: "tiktok", link:""}
      ]
    };

    //TODO:チャンネルとルームを取得
    this.channel = {name: this.$route.params.channel};
    this.room = {name: this.$route.params.room};
  },
}
</script>

<style scoped>

</style>