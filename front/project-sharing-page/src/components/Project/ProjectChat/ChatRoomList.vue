<template>
  <v-list>
    <v-list-item
      v-for="(room, i) in rooms"
      :key="i"
      @click="selected(room)"
    >
      <v-list-item-icon>
        <v-icon :color="statusIcons[room.status].color">
          {{ statusIcons[room.status].icon }}
        </v-icon>
      </v-list-item-icon>
      <v-list-item-title>{{room.name}}</v-list-item-title>
    </v-list-item>
  </v-list>
</template>

<script>
import ChatSettings from "../../../assets/scripts/ProjectPageSettings";

export default {
  name: "ChatRoomList",
  props: ['rooms', 'selectedCallback'],
  computed: {
    statusIcons(){
      return ChatSettings.statusIcons;
    }
  },
  methods: {
    selected(room){
      this.selectedCallback(room);
    }
  }
}
</script>

<style scoped>

</style>