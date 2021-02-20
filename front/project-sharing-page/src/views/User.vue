<template>
  <v-main>

    <div v-if="!isLoading">
      <v-container v-if="hasContact">
        <v-row>
          <v-col md="9" cols="12">
            <UserProfile :user="user" />
          </v-col>
  <!--        Show LARGER than md -->
          <v-col md="3" class="d-md-flex d-none">
            <UserContacts :user="user" />
          </v-col>
        </v-row>

  <!--      Show SMALLER than md -->
        <v-row class="d-md-none">
          <v-col cols="12">
            <UserContacts :user="user" />
          </v-col>
        </v-row>
      </v-container>
      <v-container v-else>
        <v-row>
          <v-col cols="12">
            <UserProfile :user="user" />
          </v-col>
        </v-row>
      </v-container>

      <v-container>
        <v-row>
          <v-col cols="12">
            <UserProjects :user="user" />
          </v-col>
        </v-row>
      </v-container>
    </div>
  </v-main>
</template>

<script>
import axios from "axios";
import UserProfile from "../components/User/UserProfile";
import UserProjects from "../components/User/UserProjects";
import UserContacts from "../components/User/UserContacts";

export default {
  name: "User",
  components: {UserContacts, UserProjects, UserProfile},
  data(){
    return {
      window: 0,
      user: {},
      isLoading: true
    }
  },
  computed :{
    hasContact(){
      if(typeof this.user.sns === "undefined")
        return false;

      let _this = this;
      let activeSns = Object.keys(this.user.sns).filter(function (name){
        return _this.user.sns[name];
      });
      return activeSns.length > 0;
    }
  },

  created() {
    this.isLoading = true;
    axios
      .get('/userapi/user/' + this.$route.params.userName)
      .then((response) => {
        this.user = response.data;
        this.isLoading = false;
      })
      .catch(() =>{
        this.$router.push({name: '404'});
      });
  }
}
</script>

<style scoped>

</style>