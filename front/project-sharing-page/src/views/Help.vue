<template>
  <v-main>
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
import HelpContents from "@/components/Help/HelpContents";
export default {
name: "Help",
  components: {HelpContents}
}
</script>

<style scoped>

</style>