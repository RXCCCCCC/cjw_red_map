<template>
  <div class="site-list-page min-h-screen bg-gray-50">
    <NavBar title="红色地标" />

    <div v-if="loading" class="flex items-center justify-center h-64">
      <van-loading type="spinner" color="#C41E24" />
    </div>

    <div v-else class="px-4 py-4 space-y-3">
      <div
        v-for="site in sites"
        :key="site.id"
        class="site-item flex items-center gap-3 bg-white rounded-xl p-3 shadow-sm border border-gray-100 active:bg-gray-50 cursor-pointer"
        @click="goDetail(site)"
      >
        <!-- 封面 -->
        <div class="w-16 h-16 rounded-lg overflow-hidden bg-gray-200 shrink-0 flex items-center justify-center">
          <img
            v-if="site.cover_image"
            :src="site.cover_image"
            class="w-full h-full object-cover"
            :alt="site.name"
          />
          <span v-else class="text-2xl">{{ getCategoryIcon(site.category) }}</span>
        </div>
        <!-- 信息 -->
        <div class="flex-1 min-w-0">
          <div class="font-semibold text-sm text-gray-800 truncate">{{ site.name }}</div>
          <div class="text-xs text-red-primary mt-0.5">{{ site.category }}</div>
          <div class="text-xs text-gray-400 mt-1 line-clamp-2">
            {{ (site.description || '').substring(0, 50) }}...
          </div>
        </div>
        <!-- 箭头 -->
        <svg class="w-4 h-4 text-gray-300 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
        </svg>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useSiteStore } from '@/stores/site'
import { storeToRefs } from 'pinia'
import NavBar from '@/components/NavBar.vue'

const router = useRouter()
const siteStore = useSiteStore()
const { sites, loading } = storeToRefs(siteStore)

onMounted(() => {
  siteStore.fetchSites()
})

function goDetail(site) {
  router.push({ name: 'SiteDetail', params: { id: site.id } })
}

function getCategoryIcon(category) {
  const map = { '居民生活': '🏠', '军事遗址': '🏛️', '革命旧址': '🏛️', '纪念设施': '🏛️', '公共设施': '🏛️' }
  return map[category] || '📍'
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
