<template>
  <v-card>
    <v-toolbar>
      <v-toolbar-title>{{title}}</v-toolbar-title>
    </v-toolbar>
    <v-row v-if="members.length > 0" class="pa-3">
      <v-col
        v-for="(member, i) in members"
        :key="i"
        cols="12"
        sm="6"
        md="4"
        lg="3"
        xl="2"
      >
        <MemberAdminCard
            :username="member"
            :select-state-changed="selectMember"
        />
      </v-col>
    </v-row>
    <v-row v-else justify="center" align="center">
      <v-responsive height="10vh">
        <v-card-text class="text-center">
          No users included.
        </v-card-text>
      </v-responsive>
    </v-row>
  </v-card>
</template>

<script>
import MemberAdminCard from "@/components/Project/ProjectAdmin/MemberRow/MemberAdminCard";
export default {
  name: "MemberRow",
  components: {MemberAdminCard},
  props: {
    project: {type: Object, required: true},
    members: {type: Array, required: true},
    title: {type: String, required: true},
    memberSelected: {type: Function, required: true}
  },

  methods: {
    selectMember(username, state){
      this.memberSelected(username, state);
    }
  }

}
</script>

<style scoped>

</style>