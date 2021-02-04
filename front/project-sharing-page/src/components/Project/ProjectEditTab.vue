<template>
  <v-container>
    <v-row>
      <v-col>
        <v-card class="pa-3" :loading="isInfoLoading">
          <ProjectInfoEdit :project="project" :loading-state-updated="updateInfoLoad" />
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <v-card class="pa-3">
          <ProjectSnsEdit :project="project" />
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <v-card class="pa-3" :loading="isImgLoading">
          <template slot="progress">
            <v-progress-linear
                color="deep-purple"
                height="10"
                indeterminate
            >
            </v-progress-linear>
          </template>
          <ProjectImgEdit :project="project" :on-load-state-changed="updateImgLoad" />
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <v-card class="pa-3">
          <ProjectTagEdit :project="project" />
        </v-card>
      </v-col>
    </v-row>

  </v-container>
</template>

<script>
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
      isImgLoading : false,
      isInfoLoading : false
    };
  },
  methods: {
    updateImgLoad(state){
      this.isImgLoading = state;
    },
    updateInfoLoad(state){
      this.isInfoLoading = state;
    }
  }
}
</script>

<style scoped>

</style>