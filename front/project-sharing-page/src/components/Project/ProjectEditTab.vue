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

  </v-container>
</template>

<script>
import ProjectSnsEdit from "@/components/Project/ProjectEditTab/ProjectSnsEdit";
import ProjectInfoEdit from "@/components/Project/ProjectEditTab/ProjectInfoEdit";

export default {
  name: "ProjectEditTab",
  components: {ProjectInfoEdit, ProjectSnsEdit},
  props: {
    project : {type: Object}
  },
  // data() {
  //   return {
  //     project: {
  //       title: "",
  //       subtitle: "",
  //       description: "",
  //       sns: {
  //         twitter: "",
  //         facebook: ""
  //       }
  //     }
  //   }
  // }
}
</script>

<style scoped>

</style>