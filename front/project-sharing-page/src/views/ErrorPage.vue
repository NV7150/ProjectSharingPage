<template>
  <v-main>
    <NavigationBar />
    <v-container>
      <v-row class="text-center" align="center" justify="center" >
        <v-responsive height="30vh">
          <v-col class="text--primary text-center text-h1 font-weight-bold" >
            Whoops!
          </v-col>
        </v-responsive>
      </v-row>
      <v-row align="center" justify="center">
          <v-col class="text-center text-h3 font-weight-light">
            不明なエラー:管理者に報告してください
          </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script>
import NavigationBar from "@/components/Navigation/NavigationBar";
export default {
name: "ErrorPage",
  components: {NavigationBar}
}
</script>

<style scoped>

</style>