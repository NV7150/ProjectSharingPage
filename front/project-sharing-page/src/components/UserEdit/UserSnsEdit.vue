<template>
  <div>
    <validation-observer ref="observer" v-slot="{invalid}">
      <validation-provider
          v-slot="{ errors }"
          name="SnsType"
          rules="required"
      >
        <v-select
            v-model="selectingSns"
            :items="getSns"
            :error-messages="errors"
            label="SNS"
            data-vv-name="selectingSns"
            required
        />
      </validation-provider>

      <validation-provider
          v-slot="{ errors }"
          name="SnsLink"
          :rules="getLinkRule"
      >
        <v-text-field
            v-model="selectingLink"
            label="SNSへのリンク"
            :error-messages="errors"
            required
        />
      </validation-provider>

      <v-btn type="submit" :disabled="invalid" @click="send">
        追加
      </v-btn>
    </validation-observer>

    <div class="d-flex flex-row flex-wrap pa-3">
      <div
          v-for="(name, i) in Object.keys(newSns)"
          :key="i"
      >
        <v-chip
            close
            v-if="newSns[name]"
            @click:close="remove(name)"
            class="mr-2 mb-4"
        >
          {{name}}
        </v-chip>
      </div>
    </div>
  </div>
</template>

<script>
import _ from "lodash";

import { required, max, regex  } from 'vee-validate/dist/rules';
import { extend, setInteractionMode, ValidationObserver, ValidationProvider } from 'vee-validate';
import SnsConstants from "@/assets/scripts/SnsConstants";


setInteractionMode('eager');

extend("required", {...required, message: '必須項目です'});
extend("regex", {...regex, message: '不正な入力内容です'});
extend("max", {...max, message: '文字数は{length}までです'});

export default {
  name: "UserSnsEdit",
  components: {ValidationObserver, ValidationProvider},

  props: {
    user : {type: Object, required: true},
    fieldUpdated: {type:Function, required: true}
  },
  data(){
    return {
      newSns: [],
      keysDict : [],
      selectingSns : SnsConstants.defaultSelect,
      selectingLink : ""
    }
  },

  methods : {
    send(){
      this.newSns[this.keysDict[this.selectingSns]] = this.selectingLink;
      this.fieldUpdated("sns", this.newSns);
    },
    submit(){
      this.$refs.observer.validate();
    },
    remove(name){
      this.newSns[name] = "";
      this.fieldUpdated("sns", this.newSns);
    }
  },

  computed :{
    getSns(){
      let snsArr = [];
      let keys = Object.keys(SnsConstants.sns);
      for(let i = 0; i < keys.length; i++){
        snsArr.push(SnsConstants.sns[keys[i]].display);
      }
      return snsArr;
    },

    getLinkRule(){
      return {
        required : true,
        regex : SnsConstants.sns[this.keysDict[this.selectingSns]].link
      };
    }
  },

  created() {
    let keys = Object.keys(SnsConstants.sns);
    for(let i = 0; i < keys.length; i++){
      this.keysDict[SnsConstants.sns[keys[i]].display] = keys[i];
    }
    this.newSns = _.cloneDeep(this.user.sns);
  }
}
</script>

<style scoped>

</style>