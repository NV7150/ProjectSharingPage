<template>
  <v-card>
    <v-card-text>
      <v-row>
        <v-col cols="11">
          <v-text-field
            label="Message"
          ></v-text-field>
        </v-col>
        <v-col cols="1">
          <v-btn
            color="primary"
          >
            Send
          </v-btn>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
name: "ChatInput"
}
</script>

<style scoped>

</style>