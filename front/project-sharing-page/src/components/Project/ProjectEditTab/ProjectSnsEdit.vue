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
          v-for="(name, i) in Object.keys(newProject.sns)"
          :key="i"
      >
        <v-chip
            close
            v-if="newProject.sns[name]"
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
import _ from "lodash"

import { required, max, regex} from 'vee-validate/dist/rules'
import { extend, ValidationObserver, ValidationProvider, setInteractionMode } from 'vee-validate'
import SnsConstants from "@/assets/scripts/SnsConstants";

setInteractionMode('eager')

extend("required", required);
extend("regex", regex);
extend("max", max);

export default {
  name: "ProjectSnsEdit",
  components : {ValidationProvider, ValidationObserver},

  props : {
    project: {type:Object}
  },

  data(){
    return {
      selectingSns : "Twitter",
      selectingLink : "",
      keysDict : {},
      newProject: {}
    }
  },

  methods : {
    send(){
      this.newProject.sns[this.keysDict[this.selectingSns]] = this.selectingLink;
      //TODO:送信
    },
    submit(){
      this.$refs.observer.validate();
    },
    remove(name){
      this.newProject.sns[name] = "";
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
    this.newProject = _.cloneDeep(this.project);
  }
}
</script>

<style scoped>

</style>