<template>
  <v-card
      :loading="loading"
      @mouseover="hovered = true"
      @mouseleave="hovered = false"
  >
    <template slot="progress">
      <v-progress-linear
          color="deep-purple"
          height="10"
          indeterminate
      >
      </v-progress-linear>
    </template>

    <v-img
        :src="project.bg_image"
        class="align-end"
    >
      <v-card-title v-text="project.title"></v-card-title>
    </v-img>

    <v-expand-transition>
      <v-card
          v-if="hovered"
          class="transition-fast-in-fast-out hover-trans"
      >
        <v-card-title v-text="project.title"></v-card-title>
        <v-card-text>
          <p>{{project.subtitle}}</p>
          <v-btn
            text
            color="real accent-4"
            @click="toProjectPage"
          >
            See More
          </v-btn>
        </v-card-text>
      </v-card>
    </v-expand-transition>
  </v-card>
</template>

<script>
import axios from "axios";
import PlaceHolder from "../../assets/PlaceHolder.png";

export default {
  name: "ProjectCard",
  props: [
      "projectId"
  ],
  data() {
    return {
      //place holder
      project : {
        name: "Loading...",
        projectId: -1,
        keyImage: PlaceHolder,
        description: ""
      },
      loading : true,
      hovered : false
    }
  },
  created() {
    axios
        .get("projectapi/project/" + this.projectId)
        .then((response) => {
          this.project = response.data;
          this.loading = false;
        })
        .catch(() => {
          //TODO:エラー処理
        });
  },
  methods:{
    toProjectPage() {
      this.$router.push({
        name:'Project',
        params: { projectId: this.project.id }
      })
    }
  }
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