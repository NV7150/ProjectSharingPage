<template>
  <v-main>
    <v-container>
      <v-row>
        <v-col>
          <PolicyCard />
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script>
import PolicyCard from "@/components/PrivacyPolicy/PolicyCard";
export default {
  name: "PrivacyPolicy",
  components: {PolicyCard}
}
</script>

<style scoped>

</style>