<template>
  <v-main>
    <NavigationBar />

    <div ref="bodies" :key="$route.path">
      <v-container>
        <v-row>
          <v-col>
            <UserSearch :keyword="$route.params.keyword" />
          </v-col>
        </v-row>
      </v-container>

      <v-container>
        <v-row>
          <v-col>
            <ProjectSearch :keyword="$route.params.keyword" />
          </v-col>
        </v-row>
      </v-container>
    </div>
  </v-main>
</template>

<script>
import ProjectSearch from "@/components/Search/ProjectSearch";
import NavigationBar from "@/components/Navigation/NavigationBar";
import UserSearch from "@/components/Search/UserSearch";
export default {
  name: "Search",
  components: {UserSearch, NavigationBar, ProjectSearch},
  data(){
    return {
      keyword: "",
      reset : false
    }
  },
  created() {
    this.keyword = this.$route.params.keyword;
  },
}
</script>

<style scoped>

</style>