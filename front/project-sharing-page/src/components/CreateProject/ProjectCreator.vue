<template>
  <v-card v-if="!initing">
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
            <ProjectInfoEdit ref="info" :project="newProject" :field-updated="fieldUpdated" />
          </v-col>
        </v-row>

        <v-row>
          <v-col>
            <ProjectTagEdit :project="newProject" :field-updated="fieldUpdated" :loading-state-updated="updateLoad" />
          </v-col>
        </v-row>

        <v-row>
          <v-col>
            <ProjectSnsEdit :project="newProject" :field-updated="fieldUpdated" />
          </v-col>
        </v-row>

        <v-row>
          <v-col>
            <ProjectImgEdit :project="newProject" :img-uploaded="imgUploaded" />
          </v-col>
        </v-row>
      </v-container>

      <v-card-actions>
        <v-btn  @click="send" :disabled="!isValid || isLoading" >
          Update
        </v-btn>
      </v-card-actions>
    </v-card>

  </v-card>
</template>

<script>
import axios from "axios";

import ProjectTagEdit from "@/components/Project/ProjectEditTab/ProjectTagEdit";
import ProjectImgEdit from "@/components/Project/ProjectEditTab/ProjectImgEdit";
import ProjectSnsEdit from "@/components/Project/ProjectEditTab/ProjectSnsEdit";
import ProjectInfoEdit from "@/components/Project/ProjectEditTab/ProjectInfoEdit";

import SnsConstants from "@/assets/scripts/SnsConstants";
import ErrorResolver from "@/assets/scripts/ErrorResolver";

export default {
  name: "ProjectCreator",
  components: {ProjectInfoEdit, ProjectImgEdit, ProjectSnsEdit, ProjectTagEdit},

  data(){
    return {
      initing: true,
      isLoading : false,
      newProject : {
        title: "",
        subtitle: "",
        description: "",
        sns: {},
        skilltags: []
      },
      isValid: false,
      imgFile: null
    }
  },

  methods: {
    validation(){
      if(this.imgFile === null) {
        this.isValid = false;
        return;
      }

      this.isLoading = true;
      this.$refs.info.validate()
          .then((result) => {
            this.isLoading = false;
            this.isValid = result;
          })
          .catch(() => {
            ErrorResolver.resolveError(this.$router);
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
      this.validation();
    },

    send(){
      if(!this.isValid)
        return;
      this.isLoading = true;
      axios
          .post("/projectapi/project", this.newProject)
          .then((response) => {
            this.editImg(response.data.id)
                .then(() => {
                  this.moveToCratedPage(response.data.id);
                })
                .catch(() => {
                  ErrorResolver.resolveError(this.$router);
                });
          });
    },

    editImg(id){

      return new Promise((resolve, reject) => {
        if(! this.imgFile)
          resolve();

        let formData = new FormData();
        formData.append("file", this.imgFile);

        axios
            .post("/projectapi/projectimage/" + id, formData)
            .then(() => {
              resolve();
            })
            .catch(() => {
              reject();
            });
      });
    },

    moveToCratedPage(id){
      this.$router.push({
        name:'Project',
        params: { projectId: id, tab: 0 }
      })
    }
  },
  created() {
    let keys = Object.keys(SnsConstants.sns);
    for(let i = 0; i < keys.length; i++){
      this.newProject.sns[keys[i]] = "";
    }
    this.initing = false;
  }
}
</script>

<style scoped>

</style>