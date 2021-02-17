<template>
  <v-card
    rounded
    outlined
    height="70vh"
    class="overflow-y-auto"
  >
    <v-card-title>Contacts</v-card-title>
    <v-divider class="my-3"></v-divider>

    <v-card-text class="d-flex flex-row flex-wrap">
        <div v-for="(snsName, i) in activeSns" :key="i">
          <v-chip
              class="ma-2"
              :color="snsSettings[snsName].color"
              text-color="white"
              label
              :href="user.sns[snsName]"
              target="_blank"
              :link="true"
          >
            <v-icon left v-if="snsSettings[snsName].icon">
              {{snsSettings[snsName].icon}}
            </v-icon>
            {{snsSettings[snsName].display}}
          </v-chip>
        </div>
    </v-card-text>
  </v-card>
</template>

<script>
import SnsSettings from "@/assets/scripts/SnsConstants";

export default {
  name: "UserContacts",
  props:{
    user: {
      type: Object,
      require: true
    }
  },
  data() {
    return{
      activeSns : []
    };
  },
  computed : {
    snsSettings() {
      return SnsSettings.sns;
    }
  },

  created() {
    let _this = this;
    this.activeSns = Object.keys(this.user.sns).filter(function (name){
      return _this.user.sns[name];
    });
  },

  watch : {
    user : function (){
      let _this = this;
      this.activeSns = Object.keys(this.user.sns).filter(function (name){
        return _this.user.sns[name];
      });
    }
  }

}
</script>

<style scoped>

</style>