import Vue from 'vue'
import App from './App.vue'

Vue.config.productionTip = false

import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import '../theme/index.css'
Vue.use(ElementUI);

//引入路由器
import VueRouter from 'vue-router'
import router from './router/index'
Vue.use(VueRouter)

//引入vuex
import store from "./store/index"

import axios from "axios";

import Viewer from 'v-viewer'
import 'viewerjs/dist/viewer.css'



//应用elementUi
Vue.use(ElementUI);
//应用axios
Vue.prototype.$axios = axios;

Vue.use(Viewer)
Viewer.setDefaults({
  'inline': false, // 启用 inline 模式
  'button': true, // 显示右上角关闭按钮
  'navbar': true, // 显示缩略图导航
  'title': false, // 显示当前图片的标题
  'toolbar': true, // 显示工具栏
  'tooltip': true, // 显示缩放百分比
  'movable': false, // 图片是否可移动
  'zoomable': true, // 图片是否可缩放
  'rotatable': false, // 图片是否可旋转
  'scalable': false, // 图片是否可翻转
  'transition': true, // 使用 CSS3 过度
  'fullscreen': true, // 播放时是否全屏
  'keyboard': true, // 是否支持键盘
})


new Vue({
  render: h => h(App),
  router,
  store,
  beforeCreate() {
    Vue.prototype.$bus = this
  }
}).$mount('#app')
