<template>
  <div ref="messageContainer" class="flex-1 overflow-auto p-4 space-y-4">

    <div v-if="messages.length === 0" class="text-center py-10 text-gray-500">
      暂无消息，开始聊天吧！
    </div>

    <div
        v-for="message in messages"
        :key="message.id"
        class="flex"
        :class="alignmentClass(message.user_id)"
    >
      <div
          class="max-w-[75%] rounded-lg p-3 relative transition-colors duration-200"
          :class="messageClasses(message.user_id)"
      >
        <div v-if="!isCurrentUser(message.user_id)" class="text-sm font-semibold mb-1">
          {{ message.username }}
        </div>

        <!-- 文本消息 -->
        <div v-if="message.content" class="break-words">
          {{ message.content }}
        </div>

        <!--        &lt;!&ndash; 文件消息 &ndash;&gt;-->
        <!--        <div v-if="message.file" class="mt-2">-->
        <!--          <a-->
        <!--              :href="message.file.url"-->
        <!--              target="_blank"-->
        <!--              class="flex items-center text-blue-500 hover:underline"-->
        <!--          >-->
        <!--            <span class="mr-2">📎</span>-->
        <!--            {{ message.file.name }}-->
        <!--          </a>-->
        <!--        </div>-->

        <div class="text-xs mt-1 opacity-70 flex justify-end items-center">
          <span>{{ formatTime(message.created_at) }}</span>
          <!-- 修改已读状态显示 -->
          <!--          <span-->
          <!--              v-if="isCurrentUser(message.user_id) && message.read"-->
          <!--              class="ml-1 text-white opacity-80"-->
          <!--          >-->
          <!--          <i class="fas fa-check-double text-xs"></i>-->
          <!--          </span>-->
          <!--          <span-->
          <!--              v-else="isCurrentUser(message.user_id)"-->
          <!--              class="ml-1 text-white opacity-50"-->
          <!--          >-->
          <!--          <i class="fas fa-check text-xs"></i>-->
          <!--          </span>-->
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref, onMounted, watch, nextTick, computed} from 'vue'
import {useAuthStore} from '../stores/auth'
import {useChatStore} from '../stores/chat'
import {storeToRefs} from 'pinia'
import {throttle} from 'lodash'
import {onBeforeUnmount} from 'vue'

const authStore = useAuthStore()
const chatStore = useChatStore()
const {user: currentUser} = storeToRefs(authStore)
const {messages} = storeToRefs(chatStore)
const messageContainer = ref(null)

const isCurrentUser = (sender) => {
  return sender === currentUser.value?.id
}

const messageClasses = computed(() => (userId) => {
  return isCurrentUser(userId)
      ? 'bg-blue-500 text-white rounded-br-none'
      : 'bg-white border rounded-bl-none'
})

const alignmentClass = computed(() => (userId) => {
  return isCurrentUser(userId) ? 'justify-end' : 'justify-start'
})

// 修改 时间格式函数
const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  const now = new Date()

  // 如果是当天只显示时间
  if (date.toDateString() === now.toDateString()) {
    return date.toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'})
  }
  // 否则显示日期和时间
  return date.toLocaleString([], {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 自动滚动到底部
const scrollToBottom = throttle(() => {
  nextTick(() => {
    if (messageContainer.value) {
      messageContainer.value.scrollTop = messageContainer.value.scrollHeight
    }
  })
}, 200)

// 监听消息变化
// 消息变化时自动滚动到底部
watch(
    () => messages.value.length,
    async () => {
      await nextTick()
      messageContainer.value?.scrollTo({
        top: messageContainer.value.scrollHeight,
        behavior: 'smooth'
      })
    }
)


onMounted(() => {
  // todo
  chatStore.connect()
  chatStore.getMessages()
  scrollToBottom()
})

onBeforeUnmount(() => {
  scrollToBottom.cancel()
})
</script>