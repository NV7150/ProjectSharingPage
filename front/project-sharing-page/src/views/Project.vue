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
          <v-tab v-if="getIsAdmin">Edit</v-tab>
          <v-tab v-if="getIsAdmin">Admin</v-tab>
        </v-tabs>

        <v-card-text>
          <v-tabs-items v-model="tabs">

            <v-tab-item>
              <v-responsive min-height="100vh">
                <ProjectProfileTab :project="project" :members="members" />
              </v-responsive>
            </v-tab-item>

            <v-tab-item>
              <v-responsive min-height="100vh">
                <v-container
                  fluid
                  class="mb-5"
                >
                  <v-row>
                    <v-col cols="12">
                      <ProjectChat
                          :project="project"
                          :channel-id="initChannel"
                          :thread-id="initThread"
                          :channel-selected="onChannelChanged"
                          :thread-selected="onThreadChanged"
                          :select-reset="onChatReset"
                      />
                    </v-col>
                  </v-row>
                </v-container>
              </v-responsive>
            </v-tab-item>

            <v-tab-item v-if="getIsAdmin">
              <v-responsive min-height="100vh">
                <ProjectEditTab :project="project" />
              </v-responsive>
            </v-tab-item>

            <v-tab-item v-if="getIsAdmin">
              <v-responsive min-height="100vh">
                <ProjectAdmin :projectRaw="project"/>
              </v-responsive>
            </v-tab-item>

          </v-tabs-items>
        </v-card-text>
      </v-card>
    </template>
    <Footer />
  </v-main>
</template>

<script>
import axios from "axios";
import NavigationBar from "../components/Navigation/NavigationBar";
import ProjectProfileTab from "../components/Project/ProjectProfileTab";
import ProjectChat from "../components/Project/ProjectChat";
import ProjectTop from "../components/Project/ProjectTop";
import ProjectEditTab from "@/components/Project/ProjectEditTab";
import ProjectAdmin from "@/components/Project/ProjectAdmin";
import Footer from "@/components/Footer/Footer";

export default {
  name: "Project",
  components: {Footer, ProjectAdmin, ProjectEditTab, ProjectTop, ProjectChat, ProjectProfileTab, NavigationBar},
  props: {
    initTab: {type: Number, default: 0},
    initChannel: {type: Number, default: -1},
    initThread: {type: Number, default: -1}
  },
  data(){
    return {
      tabs : 0,
      project: {},
      members: [],
      nonQuery : [0, 2, 3],

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
    },

    onChannelChanged(id){
      this.$router.push({
        name: "Project",
        query: {
          tab: 1,
          channel: id
        }
      });
    },

    onThreadChanged(channelId, threadId){
      this.$router.push({
        name: "Project",
        query: {
          tab: 1,
          channel: channelId,
          thread: threadId
        }
      })
    },
    onChatReset(){
      this.$router.push({
            name: "Project",
            query: {tab: 1}
      });
    },

    processLink(){
      if(this.initThread !== -1 || this.initChannel !== -1) {
        this.tabs = 1;
      }else if(this.nonQuery.indexOf(this.initTab) === -1 ){
        this.tabs = this.initTab;
      }else{
        this.tabs = 0;
      }
    },
  },

  computed : {
    getIsAdmin(){
      if(!this.$store.getters["getUser"] || !this.$store.getters["getUser"].username)
        return;

      return this.project.admin_users.indexOf(this.$store.getters["getUser"].username) !== -1;
    }
  },


  created() {
    this.processLink();

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
          // this.$router.push({name: "404"});
          this.isProjectLoading = false;
        });
  },
  watch: {
    tabs: function () {
      if(this.initTab === this.tabs)
        return;

      if(this.nonQuery.indexOf(this.tabs) !== -1){
        if(this.$route.query.tab && this.nonQuery.indexOf((Number)(this.$route.query.tab)) === -1) {
          this.$router.push({
            name: 'Project',
            params: {projectId: this.project.id}
          });
        }
      }else{
        this.$router.push({
          name: 'Project',
          params: {projectId: this.project.id},
          query: {tab: this.tabs}
        });
      }
    }
  }
}
</script>

<style scoped>


</style>