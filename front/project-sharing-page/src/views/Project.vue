<template>
  <v-main>
    <Navigation></Navigation>
    <v-parallax
      :src="project.keyImage"
    >
      <v-container
        justify="center"
        class="project-header rounded"
      >
        <v-row
          align="center"
          class="text-center text--primary"
        >
          <v-col cols="12">
            <h1>{{project.title}}</h1>
          </v-col>
        </v-row>
        <v-row
          align="center"
          class="text-center text--secondary"
        >
          <v-col cols="12">
            <h2>{{project.about}}</h2>
          </v-col>
        </v-row>
      </v-container>
    </v-parallax>

    <v-card>
      <v-tabs
        v-model="tabs"
        grow
      >
        <v-tab>General</v-tab>
        <v-tab>Chat</v-tab>
        <v-tab>Links</v-tab>
      </v-tabs>

      <v-card-text>
        <v-tabs-items v-model="tabs">
          <v-tab-item>
            <ProjectProfile :project="project" :members="project.members"></ProjectProfile>
          </v-tab-item>

          <v-tab-item>
            ここにチャット
          </v-tab-item>

          <v-tab-item>
            ここにその他リンク
          </v-tab-item>
        </v-tabs-items>
      </v-card-text>
    </v-card>

  </v-main>
</template>

<script>
import Navigation from "../components/Navigation/Navigation";
import ProjectProfile from "../components/Project/ProjectProfile";

export default {
  name: "Project",
  components: {ProjectProfile, Navigation},
  data(){
    return {
      tabs: 0,
      project: {
        title: "Test",
        keyImage: "https://gochiusa.com/bloom/core_sys/images/main/home/main_img2_4.jpg",
        about: "これはテストです",
        description:"これはテストですこれはテストですこれはテストですこれはテストですこれはテストですこれはテストですこれはテストです",
        members: [
            {display_name: 'テスト1', icon: "https://gochiusa.com/core_sys/images/contents/00000022/base/l1.png"},
            {display_name: 'テスト2', icon: "https://gochiusa.com/core_sys/images/contents/00000021/base/l1.png"}
        ],
        tags: ['Python', 'Web', 'Society', 'Design', 'Software', 'Ypaaaaaaaaaaaaaaa']
      }
    }
  }
}
</script>

<style scoped>

.project-header{
  background-color: rgba(255, 255, 255, 0.5);
}

</style>