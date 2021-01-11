<template>
  <v-main>
    <Navigation />

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
import Navigation from "@/components/Navigation/Navigation";
export default {
  name: "Error",
  components: {Navigation}
}
</script>

<style scoped>

</style>