<template>
  <div class="h-screen flex">
    <Sidebar class="w-64 border-r" />
    <div class="flex-1 flex flex-col">
      <ChatHeader />
      <MessageList class="flex-1 overflow-auto p-4 bg-gray-50" />
      <MessageInput class="border-t p-4" />
    </div>
  </div>
</template>

<script setup>
import Sidebar from '../components/Sidebar.vue'
import ChatHeader from '../components/ChatHeader.vue'
import MessageList from '../components/MessageList.vue'
import MessageInput from '../components/MessageInput.vue'
</script>