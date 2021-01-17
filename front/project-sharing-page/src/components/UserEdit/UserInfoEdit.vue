<template>
  <validation-observer ref="observer" v-slot="{ invalid }">
    <form @submit.prevent="submit">
      <validation-provider
          v-slot="{ errors }"
          name="title"
          :rules="{required: true, max:10}"
      >
        <v-text-field
            v-model="newUser.display_name"
            :counter="10"
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
            v-model="newUser.bio"
            :counter="500"
            :error-messages="errors"
            label="プロフィール"
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
  name: "UserInfoEdit",
  components: {ValidationObserver, ValidationProvider},

  props: {
    user : {type: Object}
  },
  data(){
    return{
      newUser : {}
    }
  },

  methods : {
    submit(){
      this.$refs.observer.validate();
    }
  },

  created() {
    this.newUser = _.cloneDeep(this.user);
  }
}
</script>

<style scoped>

</style>