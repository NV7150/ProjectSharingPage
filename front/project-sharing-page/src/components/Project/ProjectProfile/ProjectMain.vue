<template>
  <v-card>
    <v-card-title>
      Description
    </v-card-title>
    <v-divider class="my-3"></v-divider>
    <v-card-text>
      {{project.description}}
    </v-card-text>
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
      let hasUser = (Boolean)(this.$store.getters['getUser']);
      if(hasUser){
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
    }
  },
  computed : {
    loginUser(){
      return this.$store.getters['getUser'];
    }
  },

  watch: {
    project : function(){
      this.checkLiked();
    },
    loginUser : function (){
      this.checkLiked();
    }
  },

  created() {
    this.checkLiked();
  }
}
</script>

<style scoped>

</style>