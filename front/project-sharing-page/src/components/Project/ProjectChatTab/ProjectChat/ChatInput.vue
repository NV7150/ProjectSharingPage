<template>
  <v-card>
    <v-card-text>
      <v-row>
        <v-col cols="11">
          <v-text-field
            label="Message"
            v-model="message"
          ></v-text-field>
        </v-col>
        <v-col cols="1">
          <v-btn
            color="primary"
            @click="send"
          >
            Send
          </v-btn>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
import axios from "axios";

export default {
  name: "ChatInput",
  props: ["thread"],
  data(){
    return {
      message : ""
    };
  },
  methods : {
    send(){
      axios
          .post("/chatapi/message", {
            "thread_id" : this.thread.id,
            "content" : this.message
          })
          .then(() => {
            this.$router.go({path: this.$router.currentRoute.path, force: true});
          });
    }
  }
}
</script>

<style scoped>

</style>