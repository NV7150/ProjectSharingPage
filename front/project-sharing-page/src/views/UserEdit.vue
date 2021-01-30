<template>
  <v-main>
    <NavigationBar />
    <v-container v-if="$store.getters['getUser']">
      <v-row>
        <v-col>
          <v-card class="pa-3" :loading="isLoadingInfo">
            <template slot="progress">
              <v-progress-linear
                  color="deep-purple"
                  height="10"
                  indeterminate
              >
              </v-progress-linear>
            </template>

            <UserInfoEdit
                :user="$store.getters['getUser']"
                :loading-state-updated="updateInfo"
            />
          </v-card>
        </v-col>
      </v-row>

      <v-row>
        <v-col>
          <v-card class="pa-3" :loading="isLoadingSns">
            <template slot="progress">
              <v-progress-linear
                  color="deep-purple"
                  height="10"
                  indeterminate
              >
              </v-progress-linear>
            </template>

            <UserSnsEdit
                :user="$store.getters['getUser']"
                :loading-state-updated="updateSns"
            />
          </v-card>
        </v-col>
      </v-row>

      <v-row>
        <v-col>
          <v-card :loading="isLoadingIcon" class="pa-3">
            <template slot="progress">
              <v-progress-linear
                  color="deep-purple"
                  height="10"
                  indeterminate
              >
              </v-progress-linear>
            </template>
            <UserIconEdit
                :on-load-state-changed="updateIcon"
            />
          </v-card>
        </v-col>
      </v-row>

      <v-row>
        <v-col>
          <v-card class="pa-3">
            <UserTagEdit :user="$store.getters['getUser']" />
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
import UserIconEdit from "@/components/UserEdit/UserIconEdit";
import UserTagEdit from "@/components/UserEdit/UserTagEdit";

export default {
  name: "UserEdit",
  components: {UserTagEdit, UserIconEdit, UserSnsEdit, UserInfoEdit, NavigationBar},
  data(){
    return {
      isLoadingInfo: false,
      isLoadingSns : false,
      isLoadingIcon : false
    };
  },
  created() {
    if(!this.$store.getters["getUser"])
      this.$router.push({name: "Home"});
  },
  methods: {
    updateInfo(status){
      this.isLoadingInfo = status;
    },
    updateSns(status){
      this.isLoadingSns = status;
    },
    updateIcon(status){
      this.isLoadingIcon = status;
    }
  }
}
</script>

<style scoped>

</style>