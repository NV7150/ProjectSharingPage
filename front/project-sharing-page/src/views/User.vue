<template>
  <v-main>
    <Navigation></Navigation>
    <v-container class="d-flex">
      <v-row align="center" justify="center">
        <v-item-group
          v-model="window"
          class="shrink mr-6 flex-row"
          mandatory
          tag="v-flex"
        >
          <v-item
            v-for="i in 3"
            :key="i"
            v-slot:default="{active, toggle}"
          >
            <div>
              <v-btn
                :input-value="active"
                icon
                @click="toggle"
              >
                <v-icon>mdi-record</v-icon>
              </v-btn>
            </div>
          </v-item>
        </v-item-group>

        <v-col
        >
          <v-window
            v-model="window"
            vertical
          >
            <v-window-item>
              <UserProfile :user="user"></UserProfile>
            </v-window-item>

            <v-window-item>
              <UserProjects :user="user"></UserProjects>
            </v-window-item>

            <v-window-item>
              <UserContacts :user="user"></UserContacts>
            </v-window-item>
          </v-window>
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
// import PlaceHolder from "../assets/PlaceHolder.png";

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