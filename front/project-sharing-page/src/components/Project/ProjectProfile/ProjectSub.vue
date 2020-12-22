<template>
  <v-card>
    <v-list>
      <v-list-item-group>
        <!--Tags-->
        <v-list-item>
          <v-list-item-title>Tags</v-list-item-title>
          <v-list-item-content
              class="d-flex flex-row flex-wrap"
          >
            <v-card
                outlined
                class="ml-2 rounded-b-pill"
                v-for="(item, i) in project.tags"
                :key="i"
            >
              {{item}}
            </v-card>
          </v-list-item-content>
          <v-divider class="my-3"></v-divider>
        </v-list-item>

        <!--Members-->
        <v-list-item>
          <v-list-item-title>Members</v-list-item-title>
          <v-list-item-content
              class="d-flex flex-row flex-wrap"
          >
            <v-tooltip
                v-for="(member, i) in members"
                :key="i"
                class="ml-2"
            >
              <template v-slot:activator="{on}">
                <v-avatar
                    class="ml-2"
                    @click="userPage(member)"
                    v-on="on"
                >
                  <img :src="member.icon">
                </v-avatar>
              </template>
              <span>{{member.display_name}}</span>
            </v-tooltip>
          </v-list-item-content>
          <v-divider class="my-3"></v-divider>
        </v-list-item>

      </v-list-item-group>
    </v-list>
  </v-card>
</template>

<script>
export default {
  name: "ProjectSub",
  props: ['project', 'members'],
  methods: {
    userPage(user){
      this.$router.push({
        name: 'UserPage',
        params: {userName: user.username}
      });
    }
  }
}
</script>

<style scoped>

</style>