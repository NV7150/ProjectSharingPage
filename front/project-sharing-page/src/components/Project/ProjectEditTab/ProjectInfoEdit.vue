<template>
  <validation-observer ref="observer" v-slot="{ invalid }">
    <form @submit.prevent="submit">
      <validation-provider
          v-slot="{ errors }"
          name="title"
          :rules="{required: true, max:10}"
      >
        <v-text-field
            v-model="newProject.title"
            :counter="10"
            :error-messages="errors"
            label="タイトル"
            required
            class="mb-3"
        />
      </validation-provider>

      <validation-provider
          v-slot="{ errors }"
          name="about"
          :rules="{required: true, max:60}"
      >
        <v-text-field
            name="about"
            v-model="newProject.subtitle"
            :counter="60"
            :error-messages="errors"
            label="概要"
            required
            class="mb-3"
        />
      </validation-provider>

      <validation-provider
          v-slot="{ errors }"
          name="description"
          :rules="{required: true, max:500}"
      >
        <v-textarea
            v-model="newProject.description"
            :counter="500"
            :error-messages="errors"
            label="説明"
            required
            class="mb-3"
        />
      </validation-provider>

      <v-btn type="submit" :disabled="invalid" @click="send">
        Send
      </v-btn>

    </form>
  </validation-observer>
</template>

<script>
import { required, max, regex  } from 'vee-validate/dist/rules'
import { extend, setInteractionMode, ValidationObserver, ValidationProvider } from 'vee-validate'
import axios from "axios";

setInteractionMode('eager');

extend("required", {...required, message: '必須項目です'});
extend("regex", {...regex, message: '不正な入力内容です'});
extend("max", {...max, message: '文字数は{length}までです'});

export default {
  name: "ProjectInfoEdit",
  components : {ValidationObserver, ValidationProvider},
  props: {
    project : {type:Object},
    loadingStateUpdated: {type:Function}
  },

  data() {
    return {
      newProject: {},
      isLoading: false
    };
  },

  methods: {
    submit(){
      this.$refs.observer.validate();
    },

    send(){
      this.isLoading = true;
      axios
          .patch("/projectapi/project/" + this.project.id + "?update_fields=" + JSON.stringify(this.newProject))
          .then(() => {
            this.isLoading = false;
          })
          .catch(() => {
            //TODO:エラー処理
          })
    }
  },

  created() {
    this.newProject = {
      "title": this.project.title,
      "subtitle": this.project.subtitle,
      "description": this.project.description
    };
  },

  watch: {
    isLoading: function (){
      this.loadingStateUpdated(this.isLoading);
    }
  }
}
</script>

<style scoped>

</style>