<template>
  <v-timeline
    dense
    v-if="!isLoadingMessages"
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
              {{item.content}}
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
import axios from "axios";

export default {
  name: "ChatWindow",
  props: ["project", "channel", "thread", "onLoadingChanged"],
  data(){
    return{
      isLoadingMessages : true,
      chatCount : 0,
      chatMessages : [],
    }
  },

  methods: {
    getCount(){
      return new Promise((resolve, reject) => {
        axios
          .get("/chatapi/thread/" + this.thread.id + "/messages/count/")
          .then((response) => {
            this.chatCount = response.data
            resolve();
          })
          .catch(() => {
            reject();
          });
      });
    },

    getMessages(){
      return new Promise((resolve, reject) => {
        axios
          .get("/chatapi/thread/" + this.thread.id + "/messages/", {
            params: {
              limit: this.getLimit(),
              offset: this.getOffset()
            }
          })
          .then((response) => {
            this.chatMessages = response.data.messages.reverse();
            resolve();
          })
          .catch(() => {
            reject();
          });
      });
    },

    getUsers(){
      return new Promise((resolve, reject) => {
          let tasks = [];
          for(let i = 0; i < this.chatMessages.length; i++){
            tasks.push(
                axios.get('/userapi/user/' + this.chatMessages[i].username)
            );
          }
          Promise
              .all(tasks)
              .then((values) => {
                for(let i = 0; i < values.length; i++){
                  this.chatMessages[i].user = values[i].data;
                }
                resolve();
              })
              .catch(() => {
                reject();
              });
        }
      )
    },

    updateMessage() {
      this.isLoadingMessages = true;

      Promise.resolve()
          .then(this.getCount)
          .then(this.getMessages)
          .then(this.getUsers)
          .then(() => {
            this.isLoadingMessages = false;
          })
          .catch(() => {
            //TODO:エラー処理
          });
    },

    chatDates(message){
      return new Date(message.created_at + "Z").toLocaleString({timeZone: "Asia/Tokyo"});
    },

    getLimit(){
      return this.chatCount;
    },
    getOffset(){
      return 0;
    }
  },

  created() {
    this.updateMessage();
  },

  watch : {
    project: function (){this.updateMessage();},
    channel: function (){this.updateMessage();},
    thread: function (){this.updateMessage();},
    isLoadingMessages: function (){
      this.onLoadingChanged(this.isLoadingMessages);
    }
  }
}
</script>

<style scoped>

</style>