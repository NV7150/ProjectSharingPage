<template>
  <v-main>
    <Navigation></Navigation>

    <v-container>
      <v-row>
        <v-col md="10" cols="12">
          <UserProfile :user="user" />
        </v-col>
<!--        Show LARGER than md -->
        <v-col md="2" class="d-md-flex d-none">
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

    <v-container>
      <v-row>
        <v-col cols="12">
          <UserProjects :user="user" />
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script>
import axios from "axios";
import Navigation from "../components/Navigation/Navigation";
import UserProfile from "../components/User/UserProfile";
import UserProjects from "../components/User/UserProjects";
import UserContacts from "../components/User/UserContacts";

export default {
  name: "User",
  components: {UserContacts, UserProjects, UserProfile, Navigation},
  data(){
    return {
      window: 0,
      user: {
      }
    }
  },
  created() {
    axios
      .get('/userapi/user/' + this.$route.params.userName)
      .then((response) => {
        this.user = response.data;
      })
      .catch(() =>{
        //TODO:404ページへ
      });
  }
}
</script>

<style scoped>

</style>