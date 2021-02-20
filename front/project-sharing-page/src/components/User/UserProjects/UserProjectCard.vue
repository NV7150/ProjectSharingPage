<template>
  <v-card
      @mouseover="hovered = true"
      @mouseleave="hovered = false"
      :height="height"
      width="100%"
  >
    <v-img
        height="100%"
        :src="project.bg_image"
        class="align-center"
        gradient="to right, rgba(0,0,0,0.5), rgba(0,0,0,0.1)"
    >
      <v-card-title class="white--text">
        <div class="rounded">
          <div class="mr-1 ml-1">
            {{project.title}}
          </div>
        </div>
        <v-spacer />
      </v-card-title>
    </v-img>

    <v-expand-transition>
      <v-card
          v-if="hovered"
          class="transition-fast-in-fast-out hover-trans"
      >
        <v-card-text>
          <v-row align="center" class="pl-3 subtitle">
            {{project.subtitle}}
            <v-spacer></v-spacer>
            <v-btn
              icon
              :disabled="failed"
              @click="toProjectPage"
            >
              <v-icon>mdi-page-next</v-icon>
            </v-btn>
          </v-row>
        </v-card-text>
      </v-card>
    </v-expand-transition>
  </v-card>
</template>

<script>
export default {
  name: "UserProjectCard",
  props: {
    project : {
      type: Object,
      require: true
    },
    height: {
      type: String,
      require: false,
      "default": () => ('30vh')
    }
  },
  data() {
    return {
      hovered : false,
      failed : false
    }
  },
  methods:{
    toProjectPage() {
      this.$router.push({
        name:'Project',
        params: { projectId: this.project.id }
      })
    }
  },
}
</script>

<style scoped>
.hover-trans{
  height: 100%;
  bottom: 0;
  opacity: 0.9 !important;
  position: absolute;
  width: 100%;
}

.subtitle{
  font-size: 0.8em;
}
</style>