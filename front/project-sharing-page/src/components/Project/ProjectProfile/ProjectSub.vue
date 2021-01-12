<template>
  <v-card width="100%">
    <v-list>
      <span v-if="hasTags">
        <!--Tags-->
        <v-list-item class="mb-3">
          <v-list-item-content>
            <v-list-item-title class="mb-2">Tags</v-list-item-title>
            <v-list-item-subtitle class="d-flex flex-row flex-wrap">
              <v-card
                  outlined
                  class="ma-2 pa-2 rounded-pill"
                  v-for="(item, i) in project.skilltags"
                  :key="i"
              >
                {{item}}
              </v-card>
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>

        <v-divider class="my-3"></v-divider>
      </span>

      <!--Members-->
      <v-list-item class="mb-3">
        <v-list-item-content>
          <v-list-item-title class="mb-2">Members</v-list-item-title>
          <v-list-item-subtitle
              class="d-flex flex-row flex-wrap"
          >
            <v-tooltip
                v-for="(member, i) in members"
                :key="i"
                top
            >
              <template v-slot:activator="{on}">
                <v-avatar
                    class="ma-2"
                    @click="userPage(member)"
                    v-on="on"
                >
                  <img :src="member.icon">
                </v-avatar>
              </template>
              <span>{{member.display_name}}</span>
            </v-tooltip>
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>

      <v-divider class="my-3" v-if="activeSns.length > 0" />

      <v-list-item v-if="activeSns.length > 0">
        <v-list-item-content>
          <v-list-item-title>Contact</v-list-item-title>
          <v-list-item-subtitle class="d-flex flex-row flex-wrap">
            <div v-for="(snsName, i) in activeSns" :key="i">
              <v-chip
                  class="ma-2"
                  :color="snsSettings[snsName].color"
                  text-color="white"
                  label
                  :href="project.sns[snsName]"
              >
                <v-icon left v-if="snsSettings[snsName].icon">
                  {{snsSettings[snsName].icon}}
                </v-icon>
                {{snsSettings[snsName].display}}
              </v-chip>
            </div>
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>

    </v-list>
  </v-card>
</template>

<script>
import SnsSettings from "../../../assets/scripts/SnsConstants";

export default {
  name: "ProjectSub",
  props: {
    project : {
      type: Object
    },
    members : {type: Array}
  },
  data(){
    return{
      activeSns: []
    }
  },
  methods: {
    userPage(user){
      this.$router.push({
        name: 'UserPage',
        params: {userName: user.username}
      });
    }
  },
  computed: {
    snsSettings(){
      return SnsSettings.sns;
    },
    hasTags(){
      return this.project
          && Object.prototype.hasOwnProperty.call(this.project, "skillTags")
          && this.project.skillTags.length > 0;
    }
  },
  watch: {
    project: function (){
      let _this = this;
      this.activeSns = Object.keys(this.project.sns).filter(function (name){
        return _this.project.sns[name];
      });
    }
  }
}
</script>

<style scoped>

</style>