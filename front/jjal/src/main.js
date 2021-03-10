import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import vuetify from "./plugins/vuetify";
import VueHtml2Canvas from 'vue-html2canvas';
import 'regenerator-runtime/runtime'
Vue.use(VueHtml2Canvas);
Vue.use(vuetify);
Vue.config.productionTip = false;

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount("#app");
