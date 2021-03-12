import Vue from 'vue';
import VueRouter from 'vue-router';
import Main from '../views/main/Main.vue';
import DeepFakeImage from '../views/deepFakeImage/DeepFakeImage.vue';
import DeepFakeMovie from '../views/deepFakeMovie/DeepFakeMovie.vue';
import RemoveBack from '../views/removeBack/RemoveBack.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Main',
    component: Main,
  },
  {
    path: '/deepFakeImage',
    name: 'DeepFakeImage',
    component: DeepFakeImage,
  },
  {
    path: '/deepFakeMovie',
    name: 'DeepFakeMovie',
    component: DeepFakeMovie,
  },
  {
    path: '/removeBack',
    name: 'RemoveBack',
    component: RemoveBack,
  },
];

const router = new VueRouter({
  routes,
});

export default router;
