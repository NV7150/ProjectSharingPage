<template>
  <v-main>
    <NavigationBar />
    <v-container v-if="$store.getters['getUser']">
      <v-row>
        <v-col>
          <v-card class="pa-3">
            <UserInfoEdit :user="$store.getters['getUser']" />
          </v-card>
        </v-col>
      </v-row>

      <v-row>
        <v-col>
          <v-card class="pa-3">
            <UserSnsEdit :user="$store.getters['getUser']" />
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script>
import NavigationBar from "@/components/Navigation/NavigationBar";
import UserInfoEdit from "@/components/UserEdit/UserInfoEdit";
import UserSnsEdit from "@/components/UserEdit/UserSnsEdit";

export default {
  name: "UserEdit",
  components: {UserSnsEdit, UserInfoEdit, NavigationBar},
  created() {
    if(!this.$store.getters["getUser"])
      this.$router.push({name: "404"});
  }
}
</script>

<style scoped>

</style>