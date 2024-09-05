import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '../views/LoginPage.vue'
import RegistrationPage from '../views/RegistrationPage.vue'
import HomePage from '@/views/HomePage.vue'
import LibrarianLogin from '@/views/LibrarianLogin.vue'
import LibrarianDashBpard from '@/views/LibrarianDashBoard.vue'
import ProfilePage from '@/views/ProfilePage.vue'
import viewBooks from '@/views/viewBooks.vue'
import AddBook from '@/views/AddBook.vue'
import MyRequests from '@/views/MyRequests.vue'
import editBook from '@/views/editBook.vue'
import viewSections from '@/views/viewSections.vue'
import section from '@/views/section.vue'
import editSection from '@/views/editSection.vue'
import createSection from '@/views/createSection.vue'
import IssuedBooks from '@/views/IssuedBooks.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: LoginPage
    },
    {
      path: '/Register',
      name: 'register',
      component: RegistrationPage
    },
    {
      path:'/Home',
      name:'HomePage',
      component:HomePage
    },
    {
      path:'/LibrarianLogin',
      name:'LibrarianLogin',
      component:LibrarianLogin
    },
    {
      path:'/LibrarianDashBoard',
      name:'LibrarianDashBoard',
      component:LibrarianDashBpard
    },
    {
      path:'/Profile',
      name:'ProfilePage',
      component:ProfilePage
    },
    {
      path:'/Requests',
      name:'Requests',
      component:MyRequests
    },
    {
      path:'/viewBooks',
      name:'viewBooks',
      component:viewBooks
    },
    {
      path:'/AddBook',
      name:'AddBook',
      component:AddBook
    },
    {
      path:'/editBook/:Bid',
      name:'editBook',
      component:editBook
    },
    {
      path:'/viewSections',
      name:'viewSections',
      component:viewSections
    },
    {
      path:'/section/:sid',
      name:'section',
      component:section
    },
    {
      path:'/section/:sid/edit',
      name:'editSection',
      component:editSection
    },
    {
      path:'/createSection',
      name:'createSection',
      component:createSection
    },
    {
      path:'/booksissued',
      name:'booksissued',
      component:IssuedBooks
    }
  ]
})

export default router
