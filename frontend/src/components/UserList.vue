<template>
  <div class="p-4">
    <!-- 添加过渡动画 -->
    <h3 class="font-semibold mb-4 text-gray-700 transition-opacity duration-200">
      在线用户 ({{ onlineUsers.length }})
    </h3>
    <!-- 添加最大高度和滚动 -->
    <div class="space-y-2 max-h-[60vh] overflow-y-auto">
      <div
          v-for="user in onlineUsers"
          :key="user.id"
          class="flex items-center p-2 hover:bg-gray-100 rounded-lg cursor-pointer transition-all duration-200 hover:shadow-sm"
          role="button"
          tabindex="0"
      >

        <!-- 头像容器 -->
        <div class="relative flex-shrink-0">
          <!-- 支持头像图片显示 -->
          <div
              class="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center overflow-hidden"
              :style="avatarBackground(user)"
          >
            <img
                v-if="user.avatar"
                :src="user.avatar"
                class="w-full h-full object-cover"
                alt="用户头像"
            >
            <span v-else class="text-gray-600 font-medium text-sm">
              {{ getInitials(user.username) }}
            </span>
          </div>
          <div class="absolute bottom-0 right-0 w-3 h-3 rounded-full bg-green-500 border-2 border-white"></div>
        </div>
        <!-- 用户信息 -->
        <div class="ml-3 min-w-0">
          <p class="text-sm font-medium truncate">{{ user.username }}</p>
          <p
              v-if="user.status"
              class="text-xs text-gray-500 truncate"
          >{{ user.status }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {useChatStore} from '../stores/chat'
import {storeToRefs} from 'pinia'

const chatStore = useChatStore()
const {onlineUsers,hasInitialOnlineData } = storeToRefs(chatStore)

// 根据用户名生成固定背景色
const avatarBackground = (user) => {
  if (user.avatar) return ''
  const colors = ['#FFB399', '#FFD699', '#99FFB3', '#99D6FF', '#D699FF']
  const index = user.username.length % colors.length
  return { backgroundColor: colors[index] }
}
const getInitials = (name) => {
  return name.split(' ').map(part => part[0].toUpperCase()).join('')
}
</script>