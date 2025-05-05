import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import ChatView from '../views/ChatView.vue'
import { useAuthStore } from '../stores/auth'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            redirect: '/chat'
        },
        {
            path: '/login',
            name: 'login',
            component: LoginView,
            meta: { guestOnly: true }
        },
        {
            path: '/chat',
            name: 'chat',
            component: ChatView,
            meta: { requiresAuth: true }
        },
    ]
})

router.beforeEach(async (to, from, next) => {
    const authStore = useAuthStore()
    // 需要认证的路由
    if (to.meta.requiresAuth) {  // 检查目标路由是否需要认证
        if (!authStore.user) {
            await authStore.checkAuth()
        }
        return authStore.user ? next() : next('/login')
    }
    // 仅允许未登录用户访问的路由（如登录页）
    // 仅允许未登录用户访问的路由
    if (to.meta.guestOnly) {
        if (!authStore.user) {
            await authStore.checkAuth()
        }
        return authStore.user ? next('/chat') : next()
    }
    // 其他路由直接放行
    next()
})

export default router