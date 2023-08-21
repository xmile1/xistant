import CallbackPage from "./Callback.vue";
import Home from "./Home.vue";
import { authGuard } from "@auth0/auth0-vue";
import { createRouter, createWebHistory } from "vue-router"

const routes = [
  {
    path: "/",
    name: "home",
    component: Home,
    beforeEnter: authGuard,
  },
  {
    path: "/callback",
    name: "callback",
    component: CallbackPage,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
