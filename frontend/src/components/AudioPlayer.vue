<template>
  <div class="audio-player bg-white rounded-xl border border-gray-100 p-3 shadow-sm">
    <div class="flex items-center gap-3">
      <!-- 播放/暂停按钮 -->
      <button
        class="w-10 h-10 rounded-full bg-red-primary flex items-center justify-center text-white shadow shrink-0"
        @click="audioStore.toggle(guide)"
      >
        <svg v-if="isCurrentPlaying" class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
          <rect x="6" y="4" width="4" height="16" rx="1"/><rect x="14" y="4" width="4" height="16" rx="1"/>
        </svg>
        <svg v-else class="w-4 h-4 ml-0.5" fill="currentColor" viewBox="0 0 24 24">
          <path d="M8 5v14l11-7z"/>
        </svg>
      </button>

      <div class="flex-1 min-w-0">
        <div class="font-medium text-sm text-gray-800 mb-2">{{ guide.title }}</div>
        <!-- 进度条 -->
        <div
          class="progress-track"
          ref="trackRef"
          @click="onSeek"
        >
          <div class="progress-fill" :style="{ width: currentProgress + '%' }"></div>
          <!-- 黄星指示器（红色圆圈背景 + 动态光效和拖影） -->
          <div class="progress-star" :class="{ 'is-playing': isCurrentPlaying }" :style="{ left: currentProgress + '%' }">
            <span class="star-circle">★</span>
          </div>
        </div>
        <!-- 时间显示 -->
        <div class="flex justify-between mt-1">
          <span class="text-[10px] text-gray-400">{{ formatTime(currentTimeVal) }}</span>
          <span class="text-[10px] text-gray-400">{{ formatTime(durationVal) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useAudioStore } from '@/stores/audio'

const props = defineProps({
  guide: { type: Object, required: true },
})

const audioStore = useAudioStore()
const trackRef = ref(null)

// 预加载音频元数据，获取真实时长（不依赖种子数据中的固定值）
const realDuration = ref(0)
onMounted(() => {
  if (props.guide.audio_url) {
    const tempAudio = new Audio()
    tempAudio.preload = 'metadata'
    tempAudio.src = props.guide.audio_url
    tempAudio.addEventListener('loadedmetadata', () => {
      realDuration.value = tempAudio.duration
    })
  }
})

const isCurrentPlaying = computed(() => {
  return audioStore.isPlaying && audioStore.currentGuide?.id === props.guide.id
})

const isCurrent = computed(() => {
  return audioStore.currentGuide?.id === props.guide.id
})

const currentProgress = computed(() => {
  return isCurrent.value ? audioStore.progress : 0
})

const currentTimeVal = computed(() => {
  return isCurrent.value ? audioStore.currentTime : 0
})

const durationVal = computed(() => {
  // 优先使用 audioStore 中的实际时长（正在播放时），其次用预加载获取的真实时长
  if (isCurrent.value && audioStore.duration) return audioStore.duration
  return realDuration.value || props.guide.duration || 0
})

function formatTime(sec) {
  const m = Math.floor(sec / 60)
  const s = Math.floor(sec % 60)
  return `${m}:${s.toString().padStart(2, '0')}`
}

function onSeek(e) {
  if (!trackRef.value) return
  const rect = trackRef.value.getBoundingClientRect()
  const ratio = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width))
  // 如果当前没在播放这首，先开始播放
  if (!isCurrent.value) {
    audioStore.play(props.guide)
  }
  const targetTime = ratio * (audioStore.duration || props.guide.duration || 0)
  audioStore.seek(targetTime)
}
</script>

<style scoped>
.progress-track {
  position: relative;
  height: 14px;
  background: #e5e7eb;
  border-radius: 7px;
  border: 2.5px solid #fff;
  box-shadow: 0 0 0 1px #d1d5db;
  cursor: pointer;
  overflow: visible;
}

.progress-fill {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  background: linear-gradient(90deg, #C41E24, #e74c3c);
  border-radius: 5px;
  /* 不用 transition，靠 RAF 高频更新实现平滑 */
}

.progress-star {
  position: absolute;
  top: 50%;
  transform: translate(-50%, -50%);
  pointer-events: none;
  z-index: 1;
  /* 静态时的基础光效 */
  filter: drop-shadow(0 0 3px rgba(212, 168, 67, 0.6));
}

/* 红色圆圈背景 + 黄星 */
.star-circle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  border-radius: 30%;
  background: #C41E24;
  font-size: 16px;
  line-height: 1;
  color: #D4A843;
}

/* 播放中：动态脉冲光效 + 拖影 */
.progress-star.is-playing {
  animation: starGlow 1.2s ease-in-out infinite;
  /* 拖影：多层 drop-shadow 模拟向左扩散的尾迹 */
  filter:
    drop-shadow(0 0 4px rgba(212, 168, 67, 0.9))
    drop-shadow(-4px 0 6px rgba(212, 168, 67, 0.5))
    drop-shadow(-8px 0 8px rgba(212, 168, 67, 0.3))
    drop-shadow(-14px 0 10px rgba(212, 168, 67, 0.15));
}

@keyframes starGlow {
  0%, 100% {
    filter:
      drop-shadow(0 0 4px rgba(212, 168, 67, 0.9))
      drop-shadow(-4px 0 6px rgba(212, 168, 67, 0.5))
      drop-shadow(-8px 0 8px rgba(212, 168, 67, 0.3))
      drop-shadow(-14px 0 10px rgba(212, 168, 67, 0.15));
    transform: translate(-50%, -50%) scale(1);
  }
  50% {
    filter:
      drop-shadow(0 0 8px rgba(212, 168, 67, 1))
      drop-shadow(-6px 0 10px rgba(212, 168, 67, 0.7))
      drop-shadow(-12px 0 14px rgba(212, 168, 67, 0.4))
      drop-shadow(-20px 0 16px rgba(212, 168, 67, 0.2));
    transform: translate(-50%, -50%) scale(1.15);
  }
}
</style>
