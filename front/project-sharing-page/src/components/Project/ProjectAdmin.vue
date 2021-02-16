<template>
  <v-card :loading="isLoading" :disabled="isLoading">
    <v-container v-if="!isLoading">
      <v-row>
        <v-col cols="12">
          <MemberRow
              :project="project"
              :members="memberList.admin_users"
              title="Admins"
              :member-selected="memberSelected"
              :can-select="false"
          />
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12">
          <MemberRow
              :project="project"
              :members="memberList.announce_users"
              title="Advanced Members"
              :member-selected="memberSelected"
          />
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12">
          <MemberRow
              :project="project"
              :members="memberList.members"
              title="Members"
              :member-selected="memberSelected"
          />
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12">
          <MemberRow
              :project="project"
              :members="memberList.waits"
              title="Waiting for Permission"
              :member-selected="memberSelected"
          />
        </v-col>
      </v-row>

      <v-snackbar
        v-model="isSelectingMember"
        :multi-line="true"
        class="pa-3"
        :timeout="-1"
      >
        <v-row justify="center">
          <v-col>
            選択メンバーの権限変更
          </v-col>
        </v-row>
        <v-row justify="center">
          <v-btn
            v-for="(key, i) in Object.keys(memberTypes) "
            @click="moveMember(key)"
            class="ml-2"
            :key="i"
          >
            {{key}}
          </v-btn>
          <v-btn
              @click="moveMember(projectConst.removeKey)"
              class="ml-2"
          >
            {{projectConst.removeKey}}
          </v-btn>
        </v-row>
      </v-snackbar>

    </v-container>
  </v-card>
</template>

<script>
import MemberRow from "@/components/Project/ProjectAdmin/MemberRow";
import axios from "axios";
import ProjectConsts from "@/assets/scripts/ProjectConsts";
import ErrorResolver from "@/assets/scripts/ErrorResolver";

export default {
  name: "ProjectAdmin",
  components: {MemberRow},
  props: {
    projectRaw: {type:Object, required: true},
    loadingStateUpdated: {type: Function}
  },
  data(){
    return{
      project: {},
      isSelectingMember: false,
      memberTypes: ProjectConsts.memberTypes,
      isLoading: true,
      memberList: {
        admin_users: [],
        announce_users: [],
        members: [],
        waits: []
      },
      selecting: [],
      projectConst: ProjectConsts
    };
  },

  methods: {
    memberSelected(username, state){
      if(state){
        if(this.selecting.indexOf(username) === -1)
          this.selecting.push(username);
      }else{
        if(this.selecting.indexOf(username) !== -1)
          this.selecting = this.selecting.filter(v => v !== username);
      }

      this.isSelectingMember = this.selecting.length > 0;
    },
    moveMember(key){
      let memberType = (key !== ProjectConsts.removeKey) ? this.memberTypes[key] : ProjectConsts.removeKey;

      this.isLoading = true;
      let tasks = [];

      for(let i = 0; i < this.selecting.length; i++) {
        let request;
        if(memberType !== ProjectConsts.removeKey && this.project[memberType.prop].indexOf(this.selecting[i]) === -1){
          request =
              axios.post("/projectapi/project/" + this.project.id + "/members", {
                username: this.selecting[i],
                type: memberType.send
              });
        }else{
          if(this.memberList.waits.indexOf(this.selecting[i]) === -1) {
            let upType = this.memberTypes[ProjectConsts.getOneRankUp(key)];

            //指定階級に存在して一つ上の階級に存在しない＝うごかさないのでcontinue
            if(this.project[upType.prop].indexOf(this.selecting[i]) === -1)
              continue;

            request =
                axios.delete("/projectapi/project/" + this.project.id + "/members", {
                  data: {
                    username: this.selecting[i],
                    type: upType.send
                  }
                });
          }else{
            request =
                axios.delete("/projectapi/project/" + this.project.id + "/join-request", {
                  params: {
                    username: this.selecting[i]
                  }
                });
          }
        }

        let task = () => new Promise((resolve, reject) => {
          request
              .then(() => {
                if(memberType !== ProjectConsts.removeKey) {
                  this.memberList[memberType.prop].push(this.selecting[i]);
                }
                resolve();
              })
              .catch(() => {
                reject();
              })
        });

        tasks.push(task());
      }

      Promise
          .resolve()
          .then(() => {
            return new Promise((resolve, reject) => {
              Promise.all(tasks)
                  .then(() => {resolve();})
                  .catch(() => {reject();})
            });
          })
          .then(() => {
            return new Promise((resolve, reject) => {
              axios
                  .get("/projectapi/project/" + this.project.id)
                  .then((response) => {
                    this.project = response.data;
                    resolve();
                  })
                  .catch(() => {
                    reject();
                  });
            })
          })
          .then(this.initMemberList)
          .then(() => {
            this.selecting = [];
            this.isSelectingMember = false;
            this.isLoading = false;
          })
          .catch(() => {
            ErrorResolver.resolveError(this.$router);
          });
    },
    hasDup(target, v){
      let exists = false;
      for(let key in this.memberList){
        if(key !== target && this.memberList[key].indexOf(v) !== -1){
          exists = true;
          break;
        }
      }
      return exists;
    },
    initMemberList(){
      this.memberList = {
        admin_users: [],
        announce_users: [],
        members: [],
        waits: []
      };
      this.memberList.admin_users = this.project.admin_users;
      this.memberList.announce_users = this.project.announce_users.filter(v => !this.hasDup("announce_users", v));
      this.memberList.members = this.project.members.filter(v => !this.hasDup("members", v));

      return new Promise((resolve, reject) => {
        axios
            .get("/projectapi/project/" + this.project.id + "/waitlist")
            .then((response) => {
              this.memberList.waits = response.data.filter(v => !this.hasDup("waits", v));
              resolve();
            })
            .catch(() => {
              reject();
            });
      });
    },
  },
  created() {
    this.isLoading = true;

    this.project = this.projectRaw;

    this.initMemberList()
        .then(() => {this.isLoading = false;})
        .catch(() => {
          ErrorResolver.resolveError(this.$router);
        })
  }
}
</script>

<style scoped>

</style>