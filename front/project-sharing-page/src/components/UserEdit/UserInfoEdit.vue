<template>
  <validation-observer ref="observer">
    <form @submit.prevent="validate">
      <validation-provider
          v-slot="{ errors }"
          name="title"
          :rules="{required: true, max:20}"
      >
        <v-text-field
            v-model="displayName"
            :counter="20"
            :error-messages="errors"
            label="表示名"
            required
            class="mb-3"
        />
      </validation-provider>

      <validation-provider
          v-slot="{ errors }"
          name="bio"
          :rules="{required: true, max:500}"
      >
        <v-textarea
            v-model="bio"
            :counter="500"
            :error-messages="errors"
            label="プロフィール"
            required
            class="mb-3"
        />
      </validation-provider>
    </form>
  </validation-observer>
</template>

<script>
import { required, max, regex  } from 'vee-validate/dist/rules';
import { extend, setInteractionMode, ValidationObserver, ValidationProvider } from 'vee-validate';

setInteractionMode('eager');

extend("required", {...required, message: '必須項目です'});
extend("regex", {...regex, message: '不正な入力内容です'});
extend("max", {...max, message: '文字数は{length}までです'});


export default {
  name: "UserInfoEdit",
  components: {ValidationObserver, ValidationProvider},

  props: {
    user : {type: Object, required: true},
    fieldUpdated: {type:Function, required: true}
  },

  data(){
    return{
      displayName: "",
      bio: ""
    }
  },

  methods : {
    async validate(){
      return await this.$refs.observer.validate();
    },
  },


  created() {
    this.displayName = this.user.display_name;
    this.bio = this.user.bio;
  },

  watch: {
    displayName: function (){
      this.fieldUpdated("display_name", this.displayName);
    },
    bio: function (){
      this.fieldUpdated("bio", this.bio);
    }
  }
}
</script>

<style scoped>

</style>