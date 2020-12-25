<template>
  <v-card>
    <v-list>
      <!--Tags-->
      <v-list-item class="mb-3">
        <v-list-item-content>
          <v-list-item-title class="mb-2">Tags</v-list-item-title>
          <v-list-item-subtitle class="d-flex flex-row flex-wrap">
            <v-card
                outlined
                class="ma-2 pa-2 rounded-pill"
                v-for="(item, i) in project.tags"
                :key="i"
            >
              {{item}}
            </v-card>
          </v-list-item-subtitle>
          <v-divider class="my-3"></v-divider>
        </v-list-item-content>
      </v-list-item>

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
          <v-divider class="my-3"></v-divider>
        </v-list-item-content>
      </v-list-item>

      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>Contact</v-list-item-title>
          <v-list-item-subtitle class="d-flex flex-row flex-wrap">
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
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>

    </v-list>
  </v-card>
</template>

<script>
import SnsSettings from "../../../assets/scripts/SnsSettings";

export default {
  name: "ProjectSub",
  props: ['project', 'members'],
  methods: {
    userPage(user){
      this.$router.push({
        name: 'UserPage',
        params: {userName: user.username}
      });
    }
  },
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