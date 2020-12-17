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
        :src="project.keyImage"
        class="align-end"
    >
      <v-card-title v-text="project.name"></v-card-title>
    </v-img>

    <v-expand-transition>
      <v-card
          v-if="hovered"
          class="transition-fast-in-fast-out hover-trans"
      >
        <v-card-title v-text="project.name"></v-card-title>
        <v-card-text>
          <p>{{project.description}}</p>
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
import PlaceHolder from "../../assets/PlaceHolder.png";
import logo from "../../assets/logo.png"

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
  mounted() {
    //TODO:projectIdを使ってAPIからプロジェクトデータを取得(axios)
    //仮置き
    this.project = {
      name: "Foo" + this.projectId,
      projectId: this.projectId,
      keyImage: logo,
      description: "This is " + this.projectId + "th demo"
    };
    this.loading = false;
    //仮置きここまで
  },
  methods:{
    toProjectPage() {
      // this.$router.push({path:'/project'});
      this.$router.push({
        name:'Project',
        params: { projectId: this.project.projectId }
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