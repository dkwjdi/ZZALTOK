import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import vuetify from './plugins/vuetify';
import VueHtml2Canvas from 'vue-html2canvas';
import 'regenerator-runtime/runtime';
import AOS from 'aos';
import 'aos/dist/aos.css';

Vue.use(VueHtml2Canvas);
Vue.use(vuetify);
Vue.config.productionTip = false;
Vue.AOS = new AOS.init({ disable: 'phone' });

new Vue({
  router,
  store,
  vuetify,
  render: (h) => h(App),
}).$mount('#app');
