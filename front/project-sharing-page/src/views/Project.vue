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
import Navigation from "../components/Navigation/Navigation";
import ProjectProfileTab from "../components/Project/ProjectProfileTab";
import ProjectChatTab from "../components/Project/ProjectChatTab";
import ProjectTop from "../components/Project/ProjectChat/ProjectTop";

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
    //TODO:プロジェクトをAPIから取得
    this.project = {
      title: "Test",
        titleColor: "#1E88E5",
      keyImage: "https://gochiusa.com/bloom/core_sys/images/main/home/main_img2_4.jpg",
      about: "これはテストです",
      description:"これはテストですこれはテストですこれはテストですこれはテストですこれはテストですこれはテストですこれはテストですYpaaaaaaaこれはテストですこれはテストですこれはテストですこれはテストですこれはテストですこれはテストですこれはテストです",
      members: [
        {display_name: 'テスト1', icon: "https://gochiusa.com/core_sys/images/contents/00000022/base/l1.png"},
        {display_name: 'テスト2', icon: "https://gochiusa.com/core_sys/images/contents/00000021/base/l1.png"}
      ],
      tags: ['Python', 'Web', 'Society', 'Design', 'Software', 'Ypaaaaaaaaaaaaaaa'],
      sns: [
        {name: "twitter", link: "https://twitter.com/publicClassMain"},
        {name: "facebook", link: ""},
        {name: "tiktok", link:""}
      ]
    };
  }
}
</script>

<style scoped>


</style>