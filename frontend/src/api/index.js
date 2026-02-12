import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || '/api',
  timeout: 10000,
})

// ─── 遗址 ───
export const getSites = () => api.get('/sites')
export const getSite = (id) => api.get(`/sites/${id}`)
export const createSite = (data) => api.post('/sites', data)
export const updateSite = (id, data) => api.put(`/sites/${id}`, data)
export const deleteSite = (id) => api.delete(`/sites/${id}`)

// ─── 媒体 ───
export const getSiteMedia = (siteId) => api.get(`/sites/${siteId}/media`)
export const createMedia = (data) => api.post('/media', data)
export const deleteMedia = (id) => api.delete(`/media/${id}`)

// ─── 语音导览 ───
export const getSiteAudioGuides = (siteId) => api.get(`/sites/${siteId}/audio-guides`)
export const createAudioGuide = (data) => api.post('/audio-guides', data)
export const deleteAudioGuide = (id) => api.delete(`/audio-guides/${id}`)

export default api
