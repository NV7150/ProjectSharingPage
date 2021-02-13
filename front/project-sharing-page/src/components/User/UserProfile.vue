<template>
  <v-card
    rounded
    outlined
    height="70vh"
  >
    <v-card-title>
      <v-row align="center">
        <v-avatar
            class="ml-4"
        >
          <v-img :src="user.icon" />
        </v-avatar>
        <strong class="ml-3"> {{user.display_name}}</strong>
      </v-row>
    </v-card-title>
    <v-divider class="my-3"></v-divider>

    <v-card-text>
      {{user.bio}}
    </v-card-text>

    <v-card-actions class="d-flex flex-row flex-wrap pa-3">
      <v-card
        outlined
        class="ma-2 pa-2 rounded-pill"
        v-for="(tag, i) in user.skilltags"
        :key="i"
      >
        {{tag.name}}
      </v-card>
    </v-card-actions>
  </v-card>
</template>

<script>
import PlaceHolder from "../../assets/img/PlaceHolder.png";

export default {
  name: "UserProfile",
  props: {
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
    },
  },
  methods: {
    getColor(){
      //TODO:タグの色を取得
      return "";
    }
  }

}
</script>

<style scoped>

</style>