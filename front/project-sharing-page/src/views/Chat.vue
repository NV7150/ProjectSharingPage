<template>
  <v-main>
    <Navigation />

    <v-container>
      <v-row>
        <v-col>
          <ChatWindow />
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script>
import Navigation from "../components/Navigation/Navigation";
import ChatWindow from "../components/Project/ProjectChat/ChatWindow";

export default {
  name: "Chat",
  components: {ChatWindow, Navigation}
}
</script>

<style scoped>

</style>