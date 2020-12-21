<template>
  <v-card
    rounded
    outlined
    height="500"
  >
    <v-card-title>
      <v-row align="center">
        <v-avatar
            class="ml-4"
        >
          <img :src="user.icon">
        </v-avatar>
        <strong class="ml-3"> {{user.display_name}}</strong>
      </v-row>
    </v-card-title>
    <v-divider class="my-3"></v-divider>

    <v-card-text>
      {{user.bio}}
    </v-card-text>
    <v-card-actions>
      <v-chip-group>
        <v-chip
          disabled
          v-for="(tag, i) in user.skillTags"
          :key="i"
          :color="getColor()"
        >
          {{tag}}
        </v-chip>
      </v-chip-group>
    </v-card-actions>
  </v-card>
</template>

<script>
import PlaceHolder from "../../assets/PlaceHolder.png";

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