<template>
  <validation-observer ref="observer">
    <form @submit.prevent="validate">
      <validation-provider
          v-slot="{ errors }"
          name="title"
          :rules="{required: true, max:10}"
      >
        <v-text-field
            v-model="title"
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
            v-model="subtitle"
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
            v-model="description"
            :counter="500"
            :error-messages="errors"
            label="説明"
            required
            class="mb-3"
        />
      </validation-provider>
    </form>
  </validation-observer>
</template>

<script>
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
    project : {type:Object, required: true},
    fieldUpdated: {type: Function, required: true}
  },

  data() {
    return {
      title: "",
      subtitle: "",
      description: "",
      isLoading : false
    };
  },

  methods: {
    async validate(){
      return await this.$refs.observer.validate();
    }
  },

  created() {
      this.title = this.project.title;
      this.subtitle = this.project.subtitle;
      this.description = this.project.description;
  },

  watch: {
    title: function(){
      this.fieldUpdated("title", this.title);
    },
    subtitle: function (){
      this.fieldUpdated("subtitle", this.subtitle);
    },
    description: function (){
      this.fieldUpdated("description", this.description);
    }
  }
}
</script>

<style scoped>

</style>