<template>
  <v-main>
    <v-container v-if="$store.getters['getUser']">
      <v-row>
        <v-col>
          <v-card class="pa-3" :loading="isLoading" :disabled="isLoading">
            <template slot="progress">
              <v-progress-linear
                  color="deep-purple"
                  height="10"
                  indeterminate
              >
              </v-progress-linear>
            </template>
            <v-container>

              <v-row>
                <v-col>
                  <UserInfoEdit
                      ref="info"
                      :user="$store.getters['getUser']"
                      :field-updated="fieldUpdated"
                  />
                </v-col>
              </v-row>

              <v-row>
                <v-col>
                  <UserTagEdit
                      :user="$store.getters['getUser']"
                      :field-updated="fieldUpdated"
                  />
                </v-col>
              </v-row>

              <v-row>
                <v-col>
                  <UserSnsEdit
                      :user="$store.getters['getUser']"
                      :field-updated="fieldUpdated"
                  />
                </v-col>
              </v-row>

              <v-row>
                <v-col>
                  <UserIconEdit
                      :img-uploaded="imgUploaded"
                  />
                </v-col>
              </v-row>

            </v-container>
            <v-card-actions>
              <v-btn :disabled="!isValid || isLoading" @click="send">
                UPDATE
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script>
import UserInfoEdit from "@/components/UserEdit/UserInfoEdit";
import UserSnsEdit from "@/components/UserEdit/UserSnsEdit";
import UserIconEdit from "@/components/UserEdit/UserIconEdit";
import UserTagEdit from "@/components/UserEdit/UserTagEdit";
import axios from "axios";

export default {
  name: "UserEdit",
  components: {UserTagEdit, UserIconEdit, UserSnsEdit, UserInfoEdit},
  data(){
    return {
      isLoading: false,
      newUser: {},
      imgFile: null,
      isValid : false
    };
  },
  created() {
    if(!this.$store.getters["getUser"])
      this.$router.push({name: "Home"});
  },
  methods: {
    fieldUpdated(fieldName, val) {
      this.newUser[fieldName] = val;

      this.isLoading = true;
      this.$refs.info.validate()
          .then((result) => {
            this.isLoading = false;
            this.isValid = result;
          })
          .catch(() => {
            //TODO:エラー処理
            alert("error in validate");
          })
    },
    imgUploaded(file) {
      this.imgFile = file;
    },
    send(){
      let patchInfo = () => {
        return new Promise((resolve, reject) => {
          axios
              .patch("/userapi/user", {}, {params: {json_data: JSON.stringify(this.newUser)}})
              .then((response) => {
                this.user = response.data;
                this.$store.dispatch("checkLogin")
                    .then(() => {
                      resolve();
                    });
              })
              .catch(() => {
                reject();
              });
        });
      };

      let patchImg = () => {
        return new Promise((resolve, reject) => {
          if(this.imgFile === null)
            resolve();

          let formData = new FormData();
          formData.append("file", this.imgFile);

          axios
              .post("/userapi/usericon", formData)
              .then(() => {
                resolve();
              })
              .catch(() => {
                reject();
              });
        });
      };

      this.isLoading = true;
      Promise
          .all([patchInfo(), patchImg()])
          .then(() => {this.isLoading = false;})
          .catch(() => {
            //TODO:エラー処理
            alert("error in send");
          });
    }
  }
}
</script>

<style scoped>

</style>