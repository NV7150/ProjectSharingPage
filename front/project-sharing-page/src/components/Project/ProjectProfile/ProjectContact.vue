<template>
  <v-card>
    <v-card-title>Contact</v-card-title>

    <v-divider class="my-3"></v-divider>

    <v-card-text class="d-flex flex-row flex-wrap">
      <div v-for="(sns, i) in activeSns" :key="i">
        <v-chip
          class="ma-2"
          :color="snsSettings[sns.name].color"
          text-color="white"
          label
          :href="sns.link"
        >
          <v-icon left v-if="snsSettings[sns.name].icon">
            {{snsSettings[sns.name].icon}}
          </v-icon>
          {{snsSettings[sns.name].display}}
        </v-chip>
      </div>
    </v-card-text>
  </v-card>
</template>

<script>
import SnsSettings from "../../../assets/scripts/SnsSettings";

export default {
  name: "ProjectContact",
  props: ["project"],
  computed: {
    activeSns(){
      return this.project.sns.filter(function (sns){
        return sns;
      });
    },
    snsSettings(){
      return SnsSettings.sns;
    }
  }
}
</script>

<style scoped>

</style>