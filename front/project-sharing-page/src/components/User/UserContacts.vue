<template>
  <v-card
    rounded
    outlined
    height="500"
  >
    <v-card-title>Contacts</v-card-title>
    <v-divider class="my-3"></v-divider>
    <v-card-text>ここにSNSリンクをどーん</v-card-text>
  </v-card>
</template>

<script>
import PlaceHolder from "../../assets/img/PlaceHolder.png";

export default {
  name: "UserContacts",
  props:{
    user: {
      type: Object,
      default: function () {
        return {
          username: '',
          name: 'Loading...',
          bio: '',
          icon: PlaceHolder,
          skillTags: []
        };
      }
    }
  },

}
</script>

<style scoped>

</style>