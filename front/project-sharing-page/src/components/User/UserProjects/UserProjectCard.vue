<template>
  <v-card
      :loading="loading"
      @mouseover="hovered = true"
      @mouseleave="hovered = false"
      :height="height"
      width="100%"
  >

    <v-img
        height="100%"
        :src="project.bg_image"
        class="align-center"
    >
      <v-card-title class="white--text"> {{project.title}} </v-card-title>
    </v-img>

    <v-expand-transition>
      <v-card
          v-if="hovered"
          class="transition-fast-in-fast-out hover-trans"
      >
        <v-card-text>
          <v-row align="center" class="pl-3">
            {{project.subtitle}}
            <v-spacer></v-spacer>
            <v-btn
              icon
              :disabled="loading || failed"
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
import axios from "axios";
import ProjectPageSettings from "@/assets/scripts/ProjectPageConstants";

export default {
  name: "UserProjectCard",
  props: {
    projectId : {
      type: Number,
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
      //place holder
      project : ProjectPageSettings.defaultProject,
      loading : true,
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
    },
    getProject(){
      axios
          .get("/projectapi/project/" + this.projectId)
          .then((response) => {
            this.project = response.data;
            this.loading = false;
          })
          .catch(() => {
            this.project = ProjectPageSettings.failedProject;
            this.loading = false;
            this.failed = true;
          });
    }
  },

  created() {
    this.getProject();
  },
  // watch: {
  //   projectId: function (){
  //     this.getProject();
  //   }
  // }
}
</script>

<style scoped>
.hover-trans{
  height: 100%;
  bottom: 0;
  opacity: 0.8 !important;
  position: absolute;
  width: 100%;
}
</style>