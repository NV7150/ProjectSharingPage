<template>
  <v-main>
    <Navigation></Navigation>

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
            <ProjectProfileTab :project="project" :members="project.members"></ProjectProfileTab>
          </v-tab-item>

          <v-tab-item>
            <ProjectChatTab :project="project"></ProjectChatTab>
          </v-tab-item>

        </v-tabs-items>
      </v-card-text>
    </v-card>

  </v-main>
</template>

<script>
import axios from "axios";
import Navigation from "../components/Navigation/Navigation";
import ProjectProfileTab from "../components/Project/ProjectProfileTab";
import ProjectChatTab from "../components/Project/ProjectChatTab";
import ProjectTop from "../components/Project/ProjectTop";

export default {
  name: "Project",
  components: {ProjectTop, ProjectChatTab, ProjectProfileTab, Navigation},
  data(){
    return {
      tabs: 0,
      project: {}
    }
  },
  created() {
    axios
        .get('/projectapi/project/' + this.$route.params.projectId)
        .then((response) => {
          this.project = response.data;
        })
        .catch(() => {
          //TODO:エラーページへ飛ばす
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