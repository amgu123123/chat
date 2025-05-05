<template>
  <div class="border-b border-gray-200 p-4 flex items-center justify-between">
    <div>
<!--      <h2 class="text-xl font-semibold"># {{ channel.name }}</h2>-->
<!--      todo 频道名-->
<!--      <h2 class="text-xl font-semibold">"测试频道"</h2>-->
<!--      <p class="text-sm text-gray-500">{{ userCount }} 人在线</p>-->
    </div>
    <div class="flex space-x-3">
      <button class="p-2 rounded-full hover:bg-gray-100">
        <SearchIcon class="h-5 w-5 text-gray-500" />
      </button>
      <button class="p-2 rounded-full hover:bg-gray-100">
        <CogIcon class="h-5 w-5 text-gray-500" />
      </button>
    </div>
  </div>
</template>

<script setup>
import { SearchIcon, CogIcon } from '@heroicons/vue/outline'

defineProps({
  channel: Object,
  userCount: Number
})
</script>