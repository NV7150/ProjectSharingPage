<template>
  <v-main>
    <Navigation></Navigation>
    <v-parallax
      :src="project.keyImage"
    >
      <v-container
        justify="center"

      >
        <v-row justify="center">
          <v-col cols="12" md="6" class="project-about rounded-xl">

            <v-row
                align="center"
                justify="center"
                class="text-center text--primary"
            >
              <v-col cols="8">
                <h1
                    v-bind:style="headStyle"
                    class="text-h1"
                >
                  {{project.title}}
                </h1>
              </v-col>
            </v-row>
            <v-divider class="my-3"></v-divider>
            <v-row
                align="center"
                justify="center"
                class="text-center text--secondary"
            >
              <v-col
                  cols="8"
                  class="rounded"
              >
                <p
                    class="font-weight-light"
                >
                  {{project.about}}
                </p>
              </v-col>
            </v-row>

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
            <ProjectProfileTab :project="project" :members="project.members"></ProjectProfileTab>
          </v-tab-item>

          <v-tab-item>
            <ProjectChatTab></ProjectChatTab>
          </v-tab-item>

          <v-tab-item>
            <v-card height="100">
              ここにその他のリンク
            </v-card>
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

export default {
  name: "Project",
  components: {ProjectChatTab, ProjectProfileTab, Navigation},
  data(){
    return {
      tabs: 0,
      project: {
        title: "Test",
        titleColor: "#1E88E5",
        keyImage: "https://gochiusa.com/bloom/core_sys/images/main/home/main_img2_4.jpg",
        about: "これはテストです",
        description:"これはテストですこれはテストですこれはテストですこれはテストですこれはテストですこれはテストですこれはテストですYpaaaaaaaこれはテストですこれはテストですこれはテストですこれはテストですこれはテストですこれはテストですこれはテストです",
        members: [
            {display_name: 'テスト1', icon: "https://gochiusa.com/core_sys/images/contents/00000022/base/l1.png"},
            {display_name: 'テスト2', icon: "https://gochiusa.com/core_sys/images/contents/00000021/base/l1.png"}
        ],
        tags: ['Python', 'Web', 'Society', 'Design', 'Software', 'Ypaaaaaaaaaaaaaaa']
      }
    }
  },
  computed: {
    headStyle(){
      return {
        color: this.project.titleColor
      }
    }
  }
}
</script>

<style scoped>

.project-about{
  background-color: rgba(255, 255, 255, 0.75);
  color: dimgrey;
}

</style>