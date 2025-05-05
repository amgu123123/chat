<template>
  <div class="member-list">
    <div v-for="member in members" :key="member.id" class="member-item">
      <img :src="member.avatar" class="avatar">
      <span>{{ member.name }}</span>
      <button
          v-if="canManage"
          @click="$emit('remove', member.id)"
          class="remove-btn"
      >
        移除
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  members: {
    type: Array,
    default: () => []
  },
  canManage: {
    type: Boolean,
    default: false
  }
})

defineEmits(['remove'])
</script>