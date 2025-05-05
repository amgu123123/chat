import {defineStore} from 'pinia'
import {ref} from 'vue'
import http from '../utils/http.js'

export const useAuthStore = defineStore('auth', () => {
    const user = ref(null) //// 存储用户信息
    let isRefreshing = false; // 刷新状态标记
    let requestsQueue = [];

    // 处理队列中的请求
    const processQueue = (error, token = null) => {
        requestsQueue.forEach(cb => cb(error, token));
        requestsQueue = [];
    }
    const login = async (credentials) => {
        const data = new URLSearchParams();
        data.append('username', credentials.username); // 字段名必须为 username
        data.append('password', credentials.password); // 字段名必须为 password
        data.append('grant_type', 'password');      // 必须添加 grant_type // OAuth2 密码授权模式
        const response = await http.post(
            '/auth/login',
            data, // 直接传递 FormData
            {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            }
        );
        const token = response.data.access_token
        const refreshToken = response.data.refresh_token; // 假设后端返回 refresh_token
        const expiresIn = response.data.expires_in; // 假设返回有效期（秒）

        localStorage.setItem('token', token);
        localStorage.setItem('refresh_token', refreshToken);
        localStorage.setItem('expires_at', Date.now() + expiresIn * 1000); // 计算过期时间戳

        http.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    }

    const logout = () => {
        user.value = null
        localStorage.removeItem('token')
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('expires_at'); // 计算过期时间戳
        delete http.defaults.headers.common['Authorization']
    }

    const checkAuth = async () => {
        const storedToken = localStorage.getItem('token')
        if (!storedToken) return;

        try {
            http.defaults.headers.common['Authorization'] = `Bearer ${storedToken}`
            const response = await http.get('/auth/me')
            user.value = response.data
        } catch (error) {
            logout()
        }

    }
    http.interceptors.request.use(async config => {
        console.log('拦截请求:', config.url)
        // 放行登录和刷新请求
        if (['/auth/login', '/auth/refresh'].some(path => config.url.includes(path))) {
            return config;
        }
        const expires_at = localStorage.getItem('expires_at');
        console.log('拦截请求:', config.url, '过期时间:', expires_at);
        if (!isTokenExpired(expires_at)) {
            return config;
        }
        // 如果正在刷新，将请求加入队列
        if (isRefreshing) {
            console.log("正在刷新")
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
            console.log('触发刷新');
            const new_access_token = await refresh_Token()
            // ✅ 更新全局 Header
            http.defaults.headers.common['Authorization'] = `Bearer ${new_access_token}`;
            processQueue(null, new_access_token); // 处理队列中的请求
            // 继续当前请求 重要****
            config.headers.Authorization = `Bearer ${new_access_token}`;
            return config;
        } catch (error) {
            processQueue(error, null);
            throw error;
        } finally {
            isRefreshing = false;
        }
    }, error => {
        return Promise.reject(error);
    });

    const refresh_Token = async () => {
        const refreshtoken = localStorage.getItem('refresh_token')
        if (!refreshtoken) {
            logout();
            throw new Error('No refresh token available');
        }


        const params = new URLSearchParams();
        params.append('grant_type', 'refresh_token');
        params.append('refresh_token', refreshtoken);
        // 可选：添加scope参数（如果后端需要）
        // params.append('scope', 'read write');

        try {
            // 2. 发送符合规范的请求
            const response = await http.post('/auth/refresh', params, {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            });

            // 3. 处理响应（符合规范应返回）
            const {
                access_token,
                refresh_token,
                expires_in,
                token_type = 'Bearer'
            } = response.data;

            // 更新存储
            const newAccessToken = response.data.access_token;
            const newExpiresIn = response.data.expires_in;
            const newrefreshToken = response.data.refresh_token;
            localStorage.setItem('token', newAccessToken);
            localStorage.setItem('refresh_token', newrefreshToken);
            localStorage.setItem('expires_at', Date.now() + newExpiresIn * 1000);
            return newAccessToken;
        } catch (error) {
            logout();
            throw error;
        }
    }

    function isTokenExpired(expiresAt) {
        // 处理无效输入（null/undefined/空值）
        if (!expiresAt) return true;

        // 转换数字类型（应对 localStorage 存储的字符串情况）
        const expirationTime = Number(expiresAt);

        // 处理非数字情况（例如无效字符串）
        if (isNaN(expirationTime)) return true;
        // 返回是否过期

        return Date.now() > expirationTime;
    }


    return {user, login, logout, checkAuth}
})