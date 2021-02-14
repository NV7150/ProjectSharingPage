<template>
  <v-card :loading="isLoading" height="40vh">
    <template slot="progress">
      <v-progress-linear
          color="deep-purple"
          height="10"
          indeterminate
      />
    </template>

    <v-container>
      <v-row align="center" justify="center">
        <v-col>
          <v-row  v-if="!isLoading" justify="center" >
            <v-avatar size="15vh">
              <v-img :src="user.icon" />
            </v-avatar>
          </v-row>

          <v-card-title v-if="!isLoading" class="justify-center">
            {{user.display_name}}
          </v-card-title>

          <v-spacer />

          <v-row v-if="!isLoading" class="justify-center">
            <v-btn @click="move">
              See More
            </v-btn>
          </v-row>
        </v-col>
      </v-row>
    </v-container>
  </v-card>
</template>

<script>
import axios from "axios";
import ProjectPageConstants from "@/assets/scripts/ProjectConsts";

export default {
  name: "UserCard",
  props: {
    username: {type:String}
  },
  data(){
    return{
      isLoading: true,
      user: {}
    }
  },

  methods:{
    move(){
      this.$router.push({
        name: "UserPage",
        params: {userName: this.username}
      });
    }
  },

  created() {
    axios.get("/userapi/user/" + this.username)
        .then((response) => {
          this.user = response.data;
          this.isLoading = false;
        })
        .catch(() => {
          this.user = ProjectPageConstants.failedProject;
          this.isLoading = false;
        });
  }
}
</script>

<style scoped>

</style>