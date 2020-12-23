<template>
  <v-container fluid>
    <v-row>
      <v-col
        cols="12"
        md="10"
      >
        <ProjectMain :project="project"></ProjectMain>
      </v-col>

      <!--Display over md-->
      <v-col
        class="d-md-flex d-none "
        md="2"
      >
        <ProjectSub :project="project" :members="members"></ProjectSub>
      </v-col>
    </v-row>

    <!--Display less than md-->
    <v-row class="d-md-none d-flex">
      <v-col
        cols="12"
      >
        <ProjectSub :project="project" :members="members"></ProjectSub>
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