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

      <v-btn type="submit" :disabled="invalid">
        Send
      </v-btn>

    </form>
  </validation-observer>
</template>

<script>
import _ from "lodash"
import { required, max, regex  } from 'vee-validate/dist/rules'
import { extend, setInteractionMode, ValidationObserver, ValidationProvider } from 'vee-validate'

setInteractionMode('eager');

extend("required", {...required, message: '必須項目です'});
extend("regex", {...regex, message: '不正な入力内容です'});
extend("max", {...max, message: '文字数は{length}までです'});

export default {
  name: "ProjectInfoEdit",
  components : {ValidationObserver, ValidationProvider},
  props: {
    project : {type:Object}
  },

  data() {
    return {
      newProject: {}
    };
  },

  methods: {
    submit(){
      this.$refs.observer.validate();
    }
  },

  created() {
    this.newProject = _.cloneDeep(this.project);
  }
}
</script>

<style scoped>

</style>