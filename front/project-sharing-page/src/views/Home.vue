<template>
  <v-main>
    <NavigationBar></NavigationBar>
    <Projects></Projects>
    <Footer />
  </v-main>
</template>

<script>
import Projects from "../components/Home/Projects";
import NavigationBar from "../components/Navigation/NavigationBar";
import Footer from "@/components/Footer/Footer";

export default {
  name: 'Home',
  components: {
    Footer,
    NavigationBar,
    Projects
  }
}
</script>
