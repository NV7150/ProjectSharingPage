<template>
  <v-main>
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
export default {
  name: "EditPassword",
  components: { UserPasswordEdit}
}
</script>

<style scoped>

</style>