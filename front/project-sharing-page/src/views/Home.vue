<template>
  <v-main>
    <NavigationBar></NavigationBar>
    <Projects></Projects>
  </v-main>
</template>

<script>
import Projects from "../components/Home/Projects";
import NavigationBar from "../components/Navigation/NavigationBar";

export default {
  name: 'Home',
  components: {
    NavigationBar,
    Projects
  }
}
</script>
