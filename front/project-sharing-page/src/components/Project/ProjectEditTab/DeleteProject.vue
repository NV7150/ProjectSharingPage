<template>
  <v-card class="pa-3">
    <v-row justify="center">
      <v-dialog
          v-model="dialog"
      >
        <template v-slot:activator="{on, attrs}">
          <v-btn
              color="red"
              v-bind="attrs"
              v-on="on"
          >
            DELETE PROJECT
          </v-btn>
        </template>

        <v-card class="pa-3">
          <v-card-text class="text-center">
            プロジェクトを削除します。本当によろしいですか？
          </v-card-text>
          <v-card-actions>
            <v-row justify="center">
              <v-btn
                class="mr-2"
                color="red"
                @click="deleteProject"
              >
                削除
              </v-btn>

              <v-btn
                class="mr-2"
                @click="() => {this.dialog = false;}"
              >
                やめる
              </v-btn>
            </v-row>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-row>
  </v-card>
</template>

<script>
import axios from "axios";

import ErrorResolver from "@/assets/scripts/ErrorResolver";

export default {
  name: "DeleteProject",
  props: {
    project: {
      type: Object,
      required: true
    }
  },
  data(){
    return{
      dialog : false
    };
  },
  methods: {
    deleteProject(){
      axios
          .delete("/proejctapi/project/" + this.project.id)
          .then(() => {
            this.$router.push({name: "Home"});
          })
          .catch(() => {
            ErrorResolver.resolve(this.$router);
          });
    }
  }
}
</script>

<style scoped>

</style>