import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getSites, getSite } from '@/api'

export const useSiteStore = defineStore('site', () => {
  const sites = ref([])
  const currentSite = ref(null)
  const loading = ref(false)

  async function fetchSites() {
    loading.value = true
    try {
      const { data } = await getSites()
      sites.value = data.data || []
    } finally {
      loading.value = false
    }
  }

  async function fetchSite(id) {
    loading.value = true
    try {
      const { data } = await getSite(id)
      currentSite.value = data.data || null
    } finally {
      loading.value = false
    }
  }

  return { sites, currentSite, loading, fetchSites, fetchSite }
})
