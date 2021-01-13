<template>
  <v-main>
    <NavigationBar />

    <v-container>
      <v-row>
        <v-col>
          404 Not Found
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script>
import NavigationBar from "@/components/Navigation/NavigationBar";
export default {
  name: "Error",
  components: {NavigationBar}
}
</script>

<style scoped>

</style>