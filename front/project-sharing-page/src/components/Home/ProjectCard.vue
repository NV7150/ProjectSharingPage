<template>
  <v-card
      :loading="loading"
      @mouseover="hovered = true"
      @mouseleave="hovered = false"
      :height="height"
  >
    <template slot="progress">
      <v-progress-linear
          color="deep-purple"
          height="10"
          indeterminate
      >
      </v-progress-linear>
      <v-skeleton-loader
        class="mx-auto"
        type="card"
      />
    </template>

    <v-img
        height="80%"
        :src="project.bg_image"
        :lazy-src="placeHolder"
        class="align-end"
        gradient="to bottom, rgba(0,0,0,0.1), rgba(0,0,0,0.5)"
    >
      <template v-slot:placeholder>
        <v-row
            class="fill-height ma-0"
            align="center"
            justify="center"
        >
          <v-progress-circular
            indeterminate
            color="white"
          />
        </v-row>
      </template>
      <v-card-title>
        <div class="white--text rounded pl-1 pr-1">{{project.title}}</div>
        <v-spacer />
      </v-card-title>
    </v-img>

    <v-responsive height="20%" class="align-center">
      <v-card-actions>
        <v-icon color="pink" class="mr-1">mdi-heart</v-icon>
        {{project.likes}}
      </v-card-actions>
    </v-responsive>

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
            :disabled="loading || failed"
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
import ProjectPageSettings from "@/assets/scripts/ProjectConsts";
import PlaceHolder from "@/assets/img/PlaceHolder.png"

export default {
  name: "ProjectCard",
  props: {
    projectId : {
      type: Number,
      require: true
    },
    height: {
      type: String,
      require: false,
      "default": () => ('40vh')
    },
    user: {
      type: Object,
      require: true
    }
  },
  data() {
    return {
      //place holder
      project : ProjectPageSettings.defaultProject,
      loading : true,
      hovered : false,
      failed : false,
      placeHolder: PlaceHolder
    }
  },
  methods:{
    toProjectPage() {
      this.$router.push({
        name:'Project',
        params: { projectId: this.project.id, tab: 0 }
      })
    }
  },
  created() {
    //GET projects
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
  },
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

  .bg-title-text{
    background-color: rgba(0, 0, 0, 0.3);
  }
</style>