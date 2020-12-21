<template>
  <v-main>
    <Navigation></Navigation>
    <Projects></Projects>
  </v-main>
</template>

<script>
import Projects from "../components/Home/Projects";
import Navigation from "../components/Navigation/Navigation";

export default {
  name: 'Home',
  components: {
    Navigation,
    Projects
  }
}
</script>
