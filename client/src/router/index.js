import Vue from 'vue';
import Router from 'vue-router';
import InstaHash from '../components/InstaHash.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'InstaHash',
      component: InstaHash,
    },
  ],
});
