import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/HomeView.vue'),
    meta: { title: '程家湾红色资源数字地图' },
  },
  {
    path: '/model3d',
    name: 'Model3D',
    component: () => import('@/views/Model3DView.vue'),
    meta: { title: '三维模型' },
  },
  {
    path: '/site/:id',
    name: 'SiteDetail',
    component: () => import('@/views/SiteDetail.vue'),
    meta: { title: '地标详情' },
    props: true,
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('@/views/AboutView.vue'),
    meta: { title: '关于项目' },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  document.title = to.meta.title || '程家湾红色资源数字地图'
})

export default router
