<template>
  <v-container>
    <v-row>
      <v-col>
        <v-card class="pa-3">
          <ProjectInfoEdit :project="project" />
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
          <ProjectImgEdit :project="project" :on-load-state-changed="updateLoadState" />
        </v-card>
      </v-col>
    </v-row>

  </v-container>
</template>

<script>
import ProjectSnsEdit from "@/components/Project/ProjectEditTab/ProjectSnsEdit";
import ProjectInfoEdit from "@/components/Project/ProjectEditTab/ProjectInfoEdit";
import ProjectImgEdit from "@/components/Project/ProjectEditTab/ProjectImgEdit";

export default {
  name: "ProjectEditTab",
  components: {ProjectImgEdit, ProjectInfoEdit, ProjectSnsEdit},
  props: {
    project : {type: Object}
  },
  data(){
    return{
      isImgLoading : false
    };
  },
  methods: {
    updateLoadState(state){
      this.isImgLoading = state;
    }
  }
}
</script>

<style scoped>

</style>