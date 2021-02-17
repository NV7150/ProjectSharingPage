<template>
  <v-main>
    <NavigationBar />

    <v-container>
      <v-row>
        <v-col>
          <UserPasswordEdit />
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script>


import UserPasswordEdit from "@/components/UserEdit/UserPasswordEdit";
import NavigationBar from "@/components/Navigation/NavigationBar";
export default {
  name: "EditPassword",
  components: {NavigationBar, UserPasswordEdit}
}
</script>

<style scoped>

</style>