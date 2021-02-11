<template>
  <v-card>
    <v-card-title>
      Description
    </v-card-title>
    <v-divider class="my-3"></v-divider>
    <v-card-text>
      {{project.description}}
    </v-card-text>
    <v-row justify="center">
      <v-btn :disabled="!hasJoinRight" @click="join">
        Join this project
      </v-btn>
    </v-row>
    <v-responsive class="align-center">
      <v-card-actions>
        <v-btn
          icon
          @click="like"
          :disabled="!hasLikeRight"
        >
          <v-icon :color="getColor()" class="mr-1">mdi-heart</v-icon>
        </v-btn>
        {{project.likes}}
      </v-card-actions>
    </v-responsive>
  </v-card>
</template>

<script>
import axios from "axios";

export default {
  name: "ProjectMain",
  props:['project'],
  data() {
    return{
      hasLikeRight : false,
      hasJoinRight: false,
      liked : false,
      movingLike: false
    }
  },
  methods: {
    like(){
      if(this.movingLike)
        return;
      this.movingLike = true;

      if(!this.liked){
        axios
            .patch('/projectapi/project/' + this.project.id + '/like')
            .then(() => {
              this.liked = true;
              this.movingLike = false;
              this.project.likes++;
            })
            .catch(() => {
              //TODO:その他のエラーページへ飛ばす
            });
      }else{
        axios
            .delete('/projectapi/project/' + this.project.id + '/like')
            .then(() => {
              this.liked = false;
              this.movingLike = false;
              this.project.likes--;
            })
            .catch(() => {
              //TODO:その他のエラーページへ飛ばす
            });
      }
    },
    getColor(){
      return (this.liked) ? 'pink' : 'gray';
    },
    checkLiked(){
      if(this.$store.getters['getUser'] && this.project && this.project["id"] !== undefined){
        axios
            .get('/projectapi/project/' + this.project["id"] + '/like')
            .then((response) => {
              let users = response.data["users"];
              let userName = this.$store.getters['getUser'].username;

              this.liked = false;
              for(let i = 0; i < users.length; i++){
                if(users[i] === userName){
                  this.liked = true;
                  break;
                }
              }
              this.hasLikeRight = true;
            })
            .catch(() => {
              this.hasLikeRight = false;
            });
      }
    },
    checkIsMember(){
      let user = this.$store.getters["getUser"];
      if(!user){
        this.hasJoinRight = false;
        return;
      }
      let mems = this.project.members;

      for(let i = 0; i < mems.length;i++){
        if(mems[i] === user.username){
          this.hasJoinRight = false;
          return;
        }
      }

      //TODO:ウェイトリストに入ってるかを取得
      this.hasJoinRight = true;

      // axios
      //     .get("/projectapi/project/" + this.project.id + "/waitlist")
      //     .then((response) => {
      //       let wait = response.data;
      //       for(let i = 0; i < wait.length; i++){
      //         if(wait[i] === user.username){
      //           this.hasJoinRight = false;
      //           return;
      //         }
      //       }
      //       this.hasJoinRight = true;
      //     })
      //     .catch(() => {
      //       alert("error in waitlist");
      //     });

    },

    join(){
      axios
          .post("/projectapi/project/" + this.project.id + "/join-request")
          .catch(() => {
            //TODO:エラー処理
            alert("error in join");
          });
    }
  },

  created() {
    this.checkLiked();
    this.checkIsMember();
  }
}
</script>

<style scoped>

</style>