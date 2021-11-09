import Vue from 'vue';
import Router from 'vue-router';
import Ping from '../components/Ping.vue';
import Terminal from '../components/Terminal.vue';
Vue.use(Router);

export default new Router({
  mode: 'history',
  base: 'vis636-baltcity-police.herokuapp.com',
  routes: [
    {
      path: '/ping',
      name: 'Ping',
      component: Ping,
    },
    {
      path: '/*',
      name: 'Home',
      component: Terminal
    }
  ],
});