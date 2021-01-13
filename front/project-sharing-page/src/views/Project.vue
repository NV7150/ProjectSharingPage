<template>
  <v-main>
    <NavigationBar></NavigationBar>

    <ProjectTop :project="project"></ProjectTop>

    <v-card>
      <v-tabs
        v-model="tabs"
        grow
      >
        <v-tab>General</v-tab>
        <v-tab>Chat</v-tab>
      </v-tabs>

      <v-card-text>
        <v-tabs-items v-model="tabs">

          <v-tab-item>
            <v-responsive min-height="100vh">
              <ProjectProfileTab :project="project" :members="members"></ProjectProfileTab>
            </v-responsive>
          </v-tab-item>

          <v-tab-item>
            <v-responsive min-height="100vh">
              <ProjectChatTab :project="project"></ProjectChatTab>
            </v-responsive>
          </v-tab-item>

        </v-tabs-items>
      </v-card-text>
    </v-card>

  </v-main>
</template>

<script>
import axios from "axios";
import NavigationBar from "../components/Navigation/NavigationBar";
import ProjectProfileTab from "../components/Project/ProjectProfileTab";
import ProjectChatTab from "../components/Project/ProjectChatTab";
import ProjectTop from "../components/Project/ProjectTop";

export default {
  name: "Project",
  components: {ProjectTop, ProjectChatTab, ProjectProfileTab, NavigationBar},
  data(){
    return {
      tabs: 0,
      project: {},
      members: []
    }
  },
  created() {
    axios
        .get('/projectapi/project/' + this.$route.params.projectId)
        .then((response) => {
          this.project = response.data;
          let tasks = [];
          for(let i = 0; i < this.project.members.length; i++){
            tasks.push(axios.get('/userapi/user/' + this.project.members[i]));
          }
          Promise
              .all(tasks)
              .then((values) => {
                for(let i = 0; i < values.length; i++){
                  this.members.push(values[i].data);
                }
              })
              .catch(() => {
                //TODO:エラー処理
              })
        })
        .catch(() => {
          this.$router.push({name: '404'});
        });
  },
  methods: {
    getMembers(){
      //TODO:メンバーの一覧を取得
      return []
    }
  }
}
</script>

<style scoped>


</style>