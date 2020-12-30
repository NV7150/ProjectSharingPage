import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import router from './router'
import store from './store'

Vue.config.productionTip = false

Vue.config.errorHandler = (err, vm, info) => {
  console.log(`Captured in Vue.config.errorHandler: ${info}`, err);
};
window.addEventListener("error", event => {
  console.log("Captured in error EventListener", event.error);
});
window.addEventListener("unhandledrejection", event => {
  console.log("Captured in unhandledrejection EventListener", event.reason);
});

new Vue({
  vuetify,
  router,
  store,
  render: h => h(App)
}).$mount('#app')
