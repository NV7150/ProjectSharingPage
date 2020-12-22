<template>
  <v-card>
    <v-card-title>
      {{project.title}}
    </v-card-title>
    <v-divider class="my-3"></v-divider>
    <v-card-text>
      {{project.description}}
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: "ProjectMain",
  props:['project']
}
</script>

<style scoped>

</style>