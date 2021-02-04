<template>
  <v-main>
    <NavigationBar></NavigationBar>

    <template v-if="!isProjectLoading">
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
    </template>
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
      members: [],
      isProjectLoading : true
    }
  },
  methods: {
    getProject(){
      return new Promise((resolve, reject) => {
        axios
          .get('/projectapi/project/' + this.$route.params.projectId)
          .then((response) => {
            this.project = response.data;
            resolve();
          })
          .catch(() => {
            reject();
          });
      });
    },

    getUsers(){
      return new Promise((resolve, reject) => {
        let userTasks = [];
        for(let i = 0; i < this.project.members.length; i++){
          userTasks.push(axios.get('/userapi/user/' + this.project.members[i]));
        }
        Promise
          .all(userTasks)
          .then((values) => {
            for(let i = 0; i < values.length; i++){
              this.members.push(values[i].data);
            }
            resolve();
          })
          .catch(() => {
            reject();
          });
      });
    },

    getSkillTags(){
      return new Promise((resolve, reject) => {
        let tagTasks = [];
        for(let i = 0; i < this.project.skilltags.length; i++){
          tagTasks.push(axios.get("/userapi/skilltag/" + this.project.skilltags[i]))
        }
        this.project.skillTag = [];
        Promise
          .all(tagTasks)
          .then((values) => {
            for(let i = 0; i < values.length; i++){
              this.project.skillTag.push(values[i].data);
            }
            resolve();
          })
          .catch(() => {
            reject();
          });

      });
    }
  },


  created() {
    this.isProjectLoading = true;

    //get project object -> parallel[get Members, get SkillTags] -> end load
    Promise.resolve()
        .then(this.getProject)
        .then(() =>{
          return new Promise((resolve, reject) => {
            Promise
                .all([this.getUsers(), this.getSkillTags()])
                .then(() => {
                  resolve();
                })
                .catch(() => {
                  reject();
                })
          });
        })
        .then(() => {
          this.isProjectLoading = false;
        })
        .catch(() => {
          this.$router.push({name: "404"});
        });
  },

}
</script>

<style scoped>


</style>