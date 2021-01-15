<template>
  <v-container>
    <v-row>
      <v-col>
        <v-card class="pa-3">
          <InfoEdit :project="project" />
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <v-card class="pa-3">
          <SnsEdit :project="project" />
        </v-card>
      </v-col>
    </v-row>

  </v-container>
</template>

<script>
import SnsEdit from "@/components/Project/ProjectEditTab/SnsEdit";
import InfoEdit from "@/components/Project/ProjectEditTab/InfoEdit";

export default {
  name: "ProjectEditTab",
  components: {InfoEdit, SnsEdit},
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