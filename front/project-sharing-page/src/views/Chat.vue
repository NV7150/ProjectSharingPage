<template>
  <v-main>
    <Navigation />

    <v-container>
      <v-row>
        <v-col>
          <v-card>
            <v-toolbar>

            </v-toolbar>
            <ChatWindow :project="getProject" />
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
  methods: {
    getProject(){
      //TODO:プロジェクトを取得

    }
  }
}
</script>

<style scoped>

</style>