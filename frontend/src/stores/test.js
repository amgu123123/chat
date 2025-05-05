import { defineStore } from 'pinia';
import { ref } from 'vue';
import http from '../utils/http.js';

export const useAuthStore = defineStore('auth', () => {
    const user = ref(null);
    let isRefreshing = false; // 刷新状态标记
    let requestsQueue = [];   // 请求队列

    // 处理队列中的请求
    const processQueue = (error, token = null) => {
        requestsQueue.forEach(cb => cb(error, token));
        requestsQueue = [];
    };

    // 修改拦截器逻辑
    http.interceptors.request.use(async (config) => {
        // 放行登录和刷新请求
        if (['/auth/login', '/auth/refresh'].some(path => config.url.includes(path))) {
            return config;
        }

        const expiresAt = localStorage.getItem('expires_at');
        if (!isTokenExpired(expiresAt)) return config;

        // 如果正在刷新，将请求加入队列
        if (isRefreshing) {
            return new Promise((resolve, reject) => {
                requestsQueue.push((error, newToken) => {
                    if (error) {
                        reject(error);
                    } else {
                        // ✅ 关键：更新当前请求的 Header
                        config.headers.Authorization = `Bearer ${newToken}`;
                        resolve(config);
                    }
                });
            });
        }

        isRefreshing = true;
        try {
            const newToken = await refresh_Token();
            // ✅ 更新全局 Header
            http.defaults.headers.common['Authorization'] = `Bearer ${newToken}`;
            processQueue(null, newToken); // 处理队列中的请求
            return config;
        } catch (error) {
            processQueue(error, null);
            throw error;
        } finally {
            isRefreshing = false;
        }
    });

    // 修改刷新 Token 方法
    const refresh_Token = async () => {
        const refreshToken = localStorage.getItem('refresh_token');
        if (!refreshToken) {
            logout();
            throw new Error('No refresh token available');
        }

        try {
            // ✅ 使用请求体而非 URL 参数
            const data = new URLSearchParams();
            data.append('grant_type', 'refresh_token');
            data.append('refresh_token', refreshToken);

            const response = await http.post('/auth/refresh', data, {
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
            });

            // 更新存储
            const { access_token, expires_in } = response.data;
            localStorage.setItem('token', access_token);
            localStorage.setItem('expires_at', Date.now() + expires_in * 1000);

            return access_token;
        } catch (error) {
            console.error('刷新 Token 失败:', error);
            logout();
            throw error;
        }
    };

    // 其他方法保持不变...
});