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
        </v-row>
      </v-snackbar>

    </v-container>
  </v-card>
</template>

<script>
import MemberRow from "@/components/Project/ProjectAdmin/MemberRow";
import axios from "axios";
import ProjectPageConstants from "@/assets/scripts/ProjectPageConstants";

export default {
  name: "ProjectAdmin",
  components: {MemberRow},
  props: {
    project: {type:Object, required: true},
    loadingStateUpdated: {type: Function}
  },
  data(){
    return{
      isSelectingMember: false,
      memberTypes: ProjectPageConstants.memberTypes,
      isLoading: true,
      memberList: {
        admin_users: [],
        announce_users: [],
        members: [],
        waits: []
      },
      selecting: []
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
      if(key === "Remove"){
        //TODO:メンバーの削除
        return;
      }
      let memberType = this.memberTypes[key];
      this.isLoading = true;
      let tasks = [];
      for(let i = 0; i < this.selecting.length; i++) {
        let task = () => new Promise((resolve, reject) => {
          //TODO:/を削除
          axios
              .post("/projectapi/project/" + this.project.id + "/members/", {
                username: this.selecting[i],
                type: memberType.send
              })
              .then(() => {
                this.memberList[memberType.prop].push(this.selecting[i]);
                resolve();
              })
              .catch(() => {
                reject();
              })
        });

        tasks.push(task());
      }
      Promise
          .all(tasks)
          .then(() => {
            this.isLoading = false;
            this.removeDup(memberType.prop);
            this.selecting = [];
            this.isSelectingMember = false;
          })
          .catch(() => {
            //TODO:エラー処理
            alert("Error in change member");
          });
    },
    removeDup(target){
      let checking = ["waits"];
      for(let key in this.memberTypes){
        checking.push(this.memberTypes[key].prop);
      }
      checking = checking.filter(v => v !== target);
      for(let i in checking){
        let check = checking[i];
        this.memberList[check] = this.memberList[check].filter(v => !this.hasDup(check, v));
      }
    },
    hasDup(target, v){
      let exists = false;
      for(let key in this.memberList){
        console.log(this.memberList[key] + " " + key);
        if(key !== target && this.memberList[key].indexOf(v) !== -1){
          exists = true;
          break;
        }
      }
      return exists;
    }
  },

  created() {
    this.isLoading = true;

    this.memberList.admin_users = this.project.admin_users;
    this.memberList.announce_users = this.project.announce_users.filter(v => !this.hasDup("announce_users", v));
    this.memberList.members = this.project.members.filter(v => !this.hasDup("members", v));

    // this.memberTypes["Remove"] = {};

    axios
        .get("/projectapi/project/" + this.project.id + "/waitlist")
        .then((response) => {
          this.memberList.waits = response.data.filter(v => !this.hasDup("waits", v));
          this.isLoading = false;
        })
        .catch(() => {
          //TODO:エラー処理
          alert("Error in get waitlist");
        });
  }

}
</script>

<style scoped>

</style>