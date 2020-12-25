<template>
  <v-card>
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
    <v-spacer></v-spacer>
    <ChatInput></ChatInput>
  </v-card>
</template>

<script>
import ChatInput from "./ChatWindow/ChatInput";
export default {
  name: "ChatWindow",
  components: {ChatInput},
  props: ['chatMessages'],
  methods: {
    chatDates(message){
      return message.date + ", " + message.month + ", " + message.year;
    }
  }
}
</script>

<style scoped>

</style>