<template>
  <v-footer padless>
    <v-row justify="center">
      <v-btn
          text
          rounded
          class="my-2"
          @click="toPrivacyPolicy"
      >
        プライバシーポリシー
      </v-btn>
    </v-row>
    <v-col
      class="text-center"
      cols="12"
    >
      &copy;2021 dango, kekeho.
    </v-col>
  </v-footer>
</template>

<script>
export default {
  name: "Footer",
  methods: {
    toPrivacyPolicy(){
      this.$router.push(({name: "Privacy"}));
    }
  }
}
</script>

<style scoped>

</style>