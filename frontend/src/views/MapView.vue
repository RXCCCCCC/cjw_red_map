<template>
  <div class="map-page h-screen flex flex-col">
    <!-- 顶部栏 -->
    <NavBar title="红色地图" />

    <!-- 地图容器 -->
    <div class="flex-1 relative">
      <MapContainer :sites="sites" @marker-click="onMarkerClick" />

      <!-- 底部地标列表（可滑出） -->
      <div class="absolute bottom-0 left-0 right-0 z-[1000]">
        <div
          class="bg-white rounded-t-2xl shadow-lg px-4 pt-3 pb-4 max-h-[40vh] overflow-y-auto"
          :class="{ 'translate-y-[calc(100%-48px)]': !listOpen }"
          style="transition: transform 0.3s ease"
        >
          <div class="flex items-center justify-center mb-3" @click="listOpen = !listOpen">
            <div class="w-10 h-1 rounded bg-gray-300"></div>
          </div>
          <h3 class="text-red-primary font-semibold text-sm mb-3">红色地标列表</h3>
          <div v-if="loading" class="text-center text-gray-400 py-6">加载中...</div>
          <div v-else class="space-y-3">
            <SiteCard
              v-for="site in sites"
              :key="site.id"
              :site="site"
              @click="goDetail(site)"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useSiteStore } from '@/stores/site'
import { storeToRefs } from 'pinia'
import NavBar from '@/components/NavBar.vue'
import MapContainer from '@/components/MapContainer.vue'
import SiteCard from '@/components/SiteCard.vue'

const router = useRouter()
const siteStore = useSiteStore()
const { sites, loading } = storeToRefs(siteStore)
const listOpen = ref(false)

onMounted(() => {
  siteStore.fetchSites()
})

function onMarkerClick(site) {
  goDetail(site)
}

function goDetail(site) {
  router.push({ name: 'SiteDetail', params: { id: site.id } })
}
</script>
