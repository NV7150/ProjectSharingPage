<template>
  <v-main>
    <NavigationBar />
    <v-container>
      <v-row>
        <v-col>
          <ProjectSearch :keyword="$route.params.keyword" />
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script>
import ProjectSearch from "@/components/Search/ProjectSearch";
import NavigationBar from "@/components/Navigation/NavigationBar";
export default {
  name: "Search",
  components: {NavigationBar, ProjectSearch}
}
</script>

<style scoped>

</style>