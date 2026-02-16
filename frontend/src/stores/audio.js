import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAudioStore = defineStore('audio', () => {
  const audioEl = ref(null)
  const isPlaying = ref(false)
  const currentTime = ref(0)
  const duration = ref(0)
  const currentGuide = ref(null)

  // 使用 requestAnimationFrame 实现平滑进度更新，替代 timeupdate 事件（约 250ms 一次太卡顿）
  let rafId = null

  function startRaf() {
    cancelAnimationFrame(rafId)
    const tick = () => {
      if (audioEl.value && !audioEl.value.paused) {
        currentTime.value = audioEl.value.currentTime
      }
      rafId = requestAnimationFrame(tick)
    }
    rafId = requestAnimationFrame(tick)
  }

  function stopRaf() {
    cancelAnimationFrame(rafId)
    rafId = null
  }

  function play(guide) {
    if (!audioEl.value) {
      audioEl.value = new Audio()
      audioEl.value.addEventListener('loadedmetadata', () => {
        duration.value = audioEl.value.duration
      })
      audioEl.value.addEventListener('ended', () => {
        isPlaying.value = false
        stopRaf()
      })
    }

    if (currentGuide.value?.id !== guide.id) {
      audioEl.value.src = guide.audio_url
      currentGuide.value = guide
    }

    audioEl.value.play()
    isPlaying.value = true
    startRaf()
  }

  function pause() {
    audioEl.value?.pause()
    isPlaying.value = false
    stopRaf()
  }

  function stop() {
    if (audioEl.value) {
      audioEl.value.pause()
      audioEl.value.currentTime = 0
    }
    isPlaying.value = false
    currentTime.value = 0
    currentGuide.value = null
    stopRaf()
  }

  function toggle(guide) {
    if (isPlaying.value && currentGuide.value?.id === guide.id) {
      pause()
    } else {
      play(guide)
    }
  }

  function seek(time) {
    if (audioEl.value) {
      audioEl.value.currentTime = time
    }
  }

  const progress = computed(() => {
    if (!duration.value) return 0
    return (currentTime.value / duration.value) * 100
  })

  return { isPlaying, currentTime, duration, currentGuide, progress, play, pause, stop, toggle, seek }
})
