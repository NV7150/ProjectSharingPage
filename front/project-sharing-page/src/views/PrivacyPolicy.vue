<template>
  <v-main>
    <NavigationBar />
    <v-container>
      <v-row>
        <v-col>
          <PolicyCard />
        </v-col>
      </v-row>
    </v-container>
    <Footer />
  </v-main>
</template>

<script>
import PolicyCard from "@/components/PrivacyPolicy/PolicyCard";
import NavigationBar from "@/components/Navigation/NavigationBar";
import Footer from "@/components/Footer/Footer";
export default {
  name: "PrivacyPolicy",
  components: {Footer, NavigationBar, PolicyCard}
}
</script>

<style scoped>

</style>