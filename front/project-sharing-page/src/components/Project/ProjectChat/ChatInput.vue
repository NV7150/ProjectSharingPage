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
export default {
  name: "ChatInput",
  props: ["project", "channel", "room"],
  data(){
    return {
      message : ""
    };
  },
  methods : {
    send(){
      //TODO:メッセージを送る
      alert(this.message);
    }
  }
}
</script>

<style scoped>

</style>