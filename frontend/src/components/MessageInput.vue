<template>
  <div class="p-4 border-t">
    <div class="flex items-center mb-2">
      <button
          @click="toggleEmojiPicker"
          class="p-2 text-gray-500 hover:text-gray-700"
      >
        😊
      </button>
      <input
          type="file"
          ref="fileInput"
          @change="handleFileUpload"
          class="hidden"
          accept="image/*, .pdf, .doc, .docx"
      />
      <button
          @click="$refs.fileInput.click()"
          class="p-2 text-gray-500 hover:text-gray-700"
      >
        📎
      </button>
    </div>
    <div class="flex gap-2">
      <input
          v-model="message"
          @keyup.enter="sendMessage"
          placeholder="输入消息..."
          class="flex-1 border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <button
          @click="sendMessage"
          class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50"
          :disabled="!message.trim() && !file"
      >
        发送
      </button>
    </div>
    <div v-if="file" class="mt-2 flex items-center">
      <span class="text-sm text-gray-500 mr-2">{{ file.name }}</span>
      <button @click="removeFile" class="text-red-500">×</button>
    </div>
  </div>
</template>

<script setup>
import {ref} from 'vue'
import {useChatStore} from '../stores/chat'

const message = ref('')
const file = ref(null)
const fileInput = ref(null)
const chatStore = useChatStore()

const sendMessage = async () => {
  if (!message.value.trim() && !file.value) return
  let content = '';
  try {
    if (message.value.trim()) {
      content = message.value
    }

    //todo
    // if (file.value) {
    //   formData.append('file', file.value)
    // }
    await chatStore.sendMessage(content)
    message.value = ''
    file.value = null
  } catch (error) {
    console.error('发送消息失败:', error)
  }
}

const handleFileUpload = (e) => {
  const selectedFile = e.target.files[0]
  if (selectedFile) {
    file.value = selectedFile
  }
}

const removeFile = () => {
  file.value = null
  fileInput.value.value = ''
}

const toggleEmojiPicker = () => {
  // 实现表情选择器
  console.log('打开表情选择器')
}
</script>