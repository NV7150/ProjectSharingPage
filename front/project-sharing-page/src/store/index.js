import Vue from 'vue'
import Vuex from 'vuex'
import UserStore from "@/store/module/UserStore";

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
  },
  mutations: {
  },
  actions: {
  },
  modules: {
    userStore : UserStore
  }
})
