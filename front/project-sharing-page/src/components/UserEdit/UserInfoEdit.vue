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

      <v-btn type="submit" :disabled="invalid" @click="send">
        Send
      </v-btn>

    </form>
  </validation-observer>
</template>

<script>
import axios from "axios";
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
    user : {type: Object},
    loadingStateUpdated : {type: Function}
  },
  data(){
    return{
      newUser : {},
      isLoading : false
    }
  },

  methods : {
    submit(){
      this.$refs.observer.validate();
    },
    send(){
      axios.interceptors.request.use(request => {
        console.log('Starting Request: ', request)
        return request
      });
      this.isLoading = true;
      console.log(JSON.stringify(this.newUser));
      axios
          .patch("/userapi/user?json_data=" + JSON.stringify(this.newUser))
          .then(() => {
            this.isLoading = false;
          });
    }
  },

  watch: {
    isLoading : function() {
      this.loadingStateUpdated(this.isLoading);
    }
  },

  created() {
    this.newUser =  {
      "display_name" : this.user.display_name,
      "bio" : this.user.bio
    }
  }
}
</script>

<style scoped>

</style>