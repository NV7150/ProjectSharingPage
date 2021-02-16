<template>
  <v-main>
    <NavigationBar />

    <v-container>
      <v-row>
        <v-col>
          <HelpContents />
        </v-col>
      </v-row>
    </v-container>

  </v-main>
</template>

<script>
import NavigationBar from "@/components/Navigation/NavigationBar";
import HelpContents from "@/components/Help/HelpContents";
export default {
name: "Help",
  components: {HelpContents, NavigationBar}
}
</script>

<style scoped>

</style>