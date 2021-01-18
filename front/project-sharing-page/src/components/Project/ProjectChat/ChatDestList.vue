<template>
  <v-list>
    <v-list-item
      v-for="(destination, i) in destinations"
      :key="i"
      @click="selected(destination)"
    >
      <v-list-item-icon>
        <v-icon :color="statusIcons[destination.status].color">
          {{ statusIcons[destination.status].icon }}
        </v-icon>
      </v-list-item-icon>
      <v-list-item-title>{{destination.name}}</v-list-item-title>
    </v-list-item>
  </v-list>
</template>

<script>
import ChatSettings from "@/assets/scripts/ProjectPageConstants";

export default {
  name: "ChatDestList",
  props: ['destinations', 'selectedCallback'],
  computed: {
    statusIcons(){
      return ChatSettings.statusIcons;
    }
  },
  methods: {
    selected(dest){
      this.selectedCallback(dest);
    }
  }
}
</script>

<style scoped>

</style>