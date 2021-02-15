<template>
  <v-main>
    <NavigationBar />
    <v-container>
      <v-responsive min-height="80vh">
        <v-row>
          <v-col>

            <v-card :key="$route.path" :elevation="5">
              <v-tabs v-model="tabs" grow>
                <v-tab>User</v-tab>
                <v-tab>Project</v-tab>
              </v-tabs>

              <v-tabs-items v-model="tabs">
                <v-tab-item>
                  <UserSearch :keyword="$route.params.keyword" />
                </v-tab-item>
                <v-tab-item>
                  <ProjectSearch :keyword="$route.params.keyword" />
                </v-tab-item>
              </v-tabs-items>
            </v-card>

          </v-col>
        </v-row>
      </v-responsive>
    </v-container>
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
      tabs: 0
    }
  },
  created() {
    this.keyword = this.$route.params.keyword;
  },
}
</script>

<style scoped>

</style>