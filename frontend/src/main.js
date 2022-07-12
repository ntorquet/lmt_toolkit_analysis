import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from "axios"
import BootstrapVue3 from 'bootstrap-vue-3'
import { BootstrapIconsPlugin } from 'bootstrap-icons-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css'
import Popper from "vue3-popper"
import Toaster from '@meforma/vue-toaster'
import {nextTick} from 'vue';



axios.defaults.baseURL = 'http://127.0.0.1:8000'

createApp(App).use(store).use(router, axios).use(BootstrapVue3, BootstrapIconsPlugin).use(Toaster).component("Popper", Popper).mount('#app')

const DEFAULT_TITLE = "Default Title";
router.afterEach((to) => {
    nextTick(() => {
        document.title = to.meta.title || DEFAULT_TITLE;
    });
});