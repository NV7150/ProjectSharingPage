<template>
  <v-container fluid>
    <v-row>
      <v-col
        cols="12"
        md="10"
      >
        <v-row>
          <v-col cols="12">
            <ProjectMain :project="project"></ProjectMain>
          </v-col>
        </v-row>

        <v-row class="d-md-flex d-none">
          <v-col cols="12">
            <ProjectContact :project="project"></ProjectContact>
          </v-col>
        </v-row>
      </v-col>


      <v-col
        class="d-md-flex d-none"
        md="2"
      >
        <ProjectSub :project="project" :members="members"></ProjectSub>
      </v-col>

    </v-row>

    <v-row class="d-md-none d-flex">
      <v-col cols="12">
        <ProjectSub :project="project" :members="members"></ProjectSub>
      </v-col>
    </v-row>

    <v-row class="d-md-none d-flex">
      <v-col cols="12">
        <ProjectContact :project="project"></ProjectContact>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import ProjectMain from "./ProjectProfile/ProjectMain";
import ProjectSub from "./ProjectProfile/ProjectSub";
import ProjectContact from "./ProjectProfile/ProjectContact";
export default {
  name: "ProjectProfile",
  components: {ProjectContact, ProjectSub, ProjectMain},
  props: ['project', 'members']
}
</script>

<style scoped>

</style>