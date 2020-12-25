<template>
  <v-container fluid>
    <v-row>
      <v-col
        cols="12"
        md="9"
        lg="10"
      >
        <ProjectMain :project="project" />
      </v-col>


      <v-col
        class="d-md-flex d-none"
        md="3"
        lg="2"
      >
        <ProjectSub :project="project" :members="members" />
      </v-col>
    </v-row>

    <v-row class="d-md-none d-flex">
      <v-col cols="12">
        <ProjectSub :project="project" :members="members" />
      </v-col>
    </v-row>

  </v-container>
</template>

<script>
import ProjectMain from "./ProjectProfile/ProjectMain";
import ProjectSub from "./ProjectProfile/ProjectSub";

export default {
  name: "ProjectProfile",
  components: {ProjectSub, ProjectMain},
  props: ['project', 'members']
}
</script>

<style scoped>

</style>