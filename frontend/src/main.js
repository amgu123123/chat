import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './assets/main.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)


app.mount('#app')

// 在入口文件（如 main.js）中添加
window.addEventListener('unhandledrejection', (event) => {
    console.error('未处理的 Promise 异常:', event.reason);
});