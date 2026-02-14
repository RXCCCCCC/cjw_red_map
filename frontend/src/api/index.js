import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || '/api',
  timeout: 10000,
})

// ─── 红色地标 ───
export const getSites = () => api.get('/sites')
export const getSite = (id) => api.get(`/sites/${id}`)
export const createSite = (data) => api.post('/sites', data)
export const updateSite = (id, data) => api.put(`/sites/${id}`, data)
export const deleteSite = (id) => api.delete(`/sites/${id}`)

// ─── 用户绘制路径 ───
export const getRoutes = () => api.get('/routes')
export const createRoute = (data) => api.post('/routes', data)
export const deleteRoute = (id) => api.delete(`/routes/${id}`)

// ─── 媒体 ───
export const getSiteMedia = (siteId) => api.get(`/sites/${siteId}/media`)
export const createMedia = (data) => api.post('/media', data)
export const deleteMedia = (id) => api.delete(`/media/${id}`)

// ─── 语音导览 ───
export const getSiteAudioGuides = (siteId) => api.get(`/sites/${siteId}/audio-guides`)
export const createAudioGuide = (data) => api.post('/audio-guides', data)
export const deleteAudioGuide = (id) => api.delete(`/audio-guides/${id}`)

// ─── 文件上传 ───
export const uploadFile = (file, title = '') => {
  const formData = new FormData()
  formData.append('file', file)
  if (title) formData.append('title', title)
  return api.post('/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    timeout: 60000, // 大文件给更长超时
  })
}

export default api
