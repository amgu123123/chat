import {defineStore} from 'pinia'
import {ref} from 'vue'
import http from '../utils/http.js'
import {io} from 'socket.io-client'

export const useChatStore = defineStore('chat', () => {
    const socket = ref(null)
    const messages = ref([])
    const onlineUsers = ref(JSON.parse(localStorage.getItem('cachedOnlineUsers')) || [])
    const isOnlineValid = ref(false) // 增加数据有效性校验标记 // 状态标记

    const connect = async () => {
        socket.value = io('http://localhost:8000', {
            transports: ["websocket"],  // 强制 WebSocket
            path: '/socket.io',
            auth: (cb) => {
                cb({token: localStorage.getItem('token')})
            },
            reconnection: true,
            reconnectionAttempts: 5,
            reconnectionDelay: 1000,
        })
        socket.value.on('connect', () => {
            console.log('已连接到 Socket.IO 服务器');
        })
        socket.value.on('disconnect', () => {
            console.log('断开 Socket.IO 服务器');
        })
        //监听新消息，若有新消息到达则push->messages
        socket.value.on('message:new', (message) => {
            messages.value.push(JSON.parse(message));
        })
        //监听在线用户
        socket.value.on('user_online', (users) => {
            const parsedUsers = users.map(item => JSON.parse(item))
            // 首次加载时直接替换
            if (!isOnlineValid.value) {
                isOnlineValid.value = true
                onlineUsers.value = parsedUsers
            } else {
                // 后续更新使用平滑过渡
                onlineUsers.value = smoothUpdate(onlineUsers.value, parsedUsers)
            }
            // 更新本地缓存
            localStorage.setItem('cachedOnlineUsers', JSON.stringify(onlineUsers.value))
        })
        socket.value.on('error', (message) => {
            console.log('[error]', message);
        })
    }


    // 添加平滑更新逻辑
    const smoothUpdate = (oldList, newList) => {
        const updateMap = new Map(newList.map(u => [u.id, u]))

        return oldList
            .filter(u => updateMap.has(u.id)) // 保留仍然在线的用户
            .map(u => updateMap.get(u.id) || u) // 更新用户数据
            .concat( // 添加新增用户
                newList.filter(nu => !oldList.some(u => u.id === nu.id))
            )
    }
    const getMessages = () => {
        if (messages.value.length === 0) {
            loadMessages()
        }

        return messages.value
    }

    const loadMessages = async () => {

        const response = await http.get(`/message`)
        console.log(response)
        messages.value = response.data.reverse()
    }

    const sendMessage = async (message) => {
        if (!socket.value) {
            console.log('Sending message socket.value is null')
        }
        socket.value.emit('message:send', message);
    }

    return {
        socket,
        messages,
        onlineUsers,
        connect,
        getMessages,
        sendMessage
    }
})