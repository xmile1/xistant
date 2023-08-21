import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import { createAuth0 } from "@auth0/auth0-vue";
import router from './router';


const app = createApp(App)

app.use(
  createAuth0({
    domain: import.meta.env.VITE_AUTH0_DOMAIN,
    clientId: import.meta.env.VITE_AUTH0_CLIENT_ID,
    authorizationParams: {
      redirect_uri: import.meta.env.VITE_AUTH0_CALLBACK_URL,
      audience: import.meta.env.VITE_AUTH0_AUDIENCE,
    },
  })
);

app.use(router)

app.mount('#app')
