<template>
  <v-parallax
      :src="project.bg_image"
  >
    <v-container
        justify="center"

    >
      <v-row justify="center">
        <v-col cols="12" md="6" class="project-about rounded-xl">

          <v-row
              align="center"
              justify="center"
              class="text-center text--primary"
          >
            <v-col cols="8">
              <h1
                  v-bind:style="headStyle"
                  class="text-h1"
              >
                {{project.title}}
              </h1>
            </v-col>
          </v-row>
          <v-divider class="my-3"></v-divider>
          <v-row
              align="center"
              justify="center"
              class="text-center text--secondary"
          >
            <v-col
                cols="8"
                class="rounded"
            >
              <p class="font-weight-light">
                {{project.subtitle}}
              </p>
            </v-col>
          </v-row>

        </v-col>
      </v-row>
    </v-container>
  </v-parallax>

</template>

<script>
export default {
  name: "ProjectTop",
  props: ["project"],

  computed: {
    headStyle(){
      return {
        color: this.project.titleColor
      }
    }
  }
}
</script>

<style scoped>
.project-about{
  background-color: rgba(255, 255, 255, 0.75);
  color: dimgrey;
}
</style>