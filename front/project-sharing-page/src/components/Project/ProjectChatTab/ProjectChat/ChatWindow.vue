<template>
  <v-timeline
    dense
  >
    <v-timeline-item
      small
      right
      v-for="(item, i) in chatMessages"
      :key="i"
    >
      <template v-slot:icon>
        <v-avatar>
          <img :src="item.user.icon" alt="avatar">
        </v-avatar>
      </template>
      <v-row>
        <v-col
          cols="10"
        >
          <v-card
            rounded
          >
            <v-card-text>
              {{item.message}}
            </v-card-text>

            <v-footer class="pa-2">
              {{item.user.display_name}}
              <v-spacer></v-spacer>
              {{chatDates(item)}}
            </v-footer>
          </v-card>
        </v-col>
      </v-row>
    </v-timeline-item>
  </v-timeline>
</template>

<script>
export default {
  name: "ChatWindow",
  props: ["project", "channel", "thread"],
  data(){
    return{
      chatMessages : []
    }
  },

  methods: {
    updateMessage(){
      //TODO:チャットを取得
      //仮置き
      this.chatMessages = [
        {message: "これはテストです", date: 23, month: 'Dec', year:2020, user: {display_name: "テスト", icon: "https://gochiusa.com/core_sys/images/contents/00000022/base/l1.png"}},
        {message: "これはテストです2", date: 23, month: 'Dec', year:2020, user: {display_name: "テスト", icon: "https://gochiusa.com/core_sys/images/contents/00000021/base/l1.png"}},
        {message: "project:" + this.project.title + " channel:" + this.channel.name + " thread:" + this.thread.name, date: 23, month: 'Dec', year:2020, user: {display_name: "テスト", icon: "https://gochiusa.com/core_sys/images/contents/00000022/base/l1.png"}}
      ];
    },

    chatDates(message){
      return message.date + ", " + message.month + ", " + message.year;
    }
  },

  created() {
    this.updateMessage();
  },

  watch : {
    project: function (){this.updateMessage();},
    channel: function (){this.updateMessage();},
    thread: function (){this.updateMessage();}
  }
}
</script>

<style scoped>

</style>