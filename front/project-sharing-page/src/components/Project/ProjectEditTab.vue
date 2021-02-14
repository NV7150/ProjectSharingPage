<template>
  <v-container>
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
                <ProjectInfoEdit ref="info" :project="project" :field-updated="fieldUpdated" />
              </v-col>
            </v-row>

            <v-row>
              <v-col>
                <ProjectTagEdit :project="project" :field-updated="fieldUpdated" :loading-state-updated="updateLoad" />
              </v-col>
            </v-row>

            <v-row>
              <v-col>
                <ProjectSnsEdit :project="project" :field-updated="fieldUpdated" />
              </v-col>
            </v-row>

            <v-row>
              <v-col>
                <ProjectImgEdit :project="project" :img-uploaded="imgUploaded" />
              </v-col>
            </v-row>
          </v-container>

          <v-card-actions>
            <v-btn  @click="send" :disabled="!isValid || isLoading" >
              Update
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios";

import ProjectSnsEdit from "@/components/Project/ProjectEditTab/ProjectSnsEdit";
import ProjectInfoEdit from "@/components/Project/ProjectEditTab/ProjectInfoEdit";
import ProjectImgEdit from "@/components/Project/ProjectEditTab/ProjectImgEdit";
import ProjectTagEdit from "@/components/Project/ProjectEditTab/ProjectTagEdit";

export default {
  name: "ProjectEditTab",
  components: {ProjectTagEdit, ProjectImgEdit, ProjectInfoEdit, ProjectSnsEdit},
  props: {
    project : {type: Object}
  },
  data(){
    return{
      isLoading: false,
      newProject: {},
      imgFile: null,
      isValid : false
    };
  },
  methods: {
    validation(){
      this.isLoading = true;
      this.$refs.info.validate()
          .then((result) => {
            this.isLoading = false;
            this.isValid = result;
          })
          .catch(() => {
            //TODO:エラー処理
            alert("error in validate");
          });
    },
    updateLoad(state){
      this.isLoading = state;
    },
    fieldUpdated(fieldName, val){
      this.newProject[fieldName] = val;
      this.validation();
    },
    imgUploaded(file){
      this.imgFile = file;
    },
    send(){
      let patchInfo = () => {
        return new Promise((resolve, reject) => {
          axios
              .patch("/projectapi/project/" + this.project.id, {}, {
                params: {
                  update_fields: JSON.stringify(this.newProject)
                }
              })
              .then((response) => {
                this.project = response.data;
                resolve();
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
              .post("/projectapi/projectimage/" + this.project.id, formData)
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