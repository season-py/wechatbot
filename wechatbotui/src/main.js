import Vue from 'vue'
import VueRouter from 'vue-router'
import store from './store'
import App from './App'
import Home from './components/Home'
import TimeEntries from './components/TimeEntries.vue'
import LogTime from './components/LogTime.vue'
import NotFound from './components/404'
import VueResource from 'vue-resource'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-default/index.css'

Vue.use(VueRouter)
Vue.use(VueResource)
Vue.use(ElementUI)

const routes = [
  {
    path : '/',
    component : Home
  },
  {
    path : '/home',
    component : Home
  },
  {
    path : '/time-entries',
    component : TimeEntries,
    children : [
      {
        path : 'log-time',
        component : LogTime,
      }
    ]
  },
  {
    path : '*',
    component : NotFound
  }
]

const router = new VueRouter({
  routes
})

var app = new Vue({
  el: '#app',
  router,
  store,
  ...App
})
