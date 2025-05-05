<template>
  <div class="w-64 h-full flex flex-col border-r bg-white">
    <div class="p-4 border-b">
      <h2 class="text-xl font-semibold">聊天室</h2>
    </div>
    <div class="flex-1 overflow-auto">
      <UserList />
    </div>
    <div class="p-4 border-t">
      <div class="flex items-center">
        <div class="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center text-white mr-2">
          {{ currentUser.username.charAt(0).toUpperCase() }}
        </div>
        <div>
          <p class="font-medium">{{ currentUser.name }}</p>
          <p class="text-xs text-gray-500">在线</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '../stores/auth'
import { storeToRefs } from 'pinia'
import UserList from './UserList.vue'

const authStore = useAuthStore()
const { user: currentUser } = storeToRefs(authStore)
</script>