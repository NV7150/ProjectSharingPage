import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Project from "../views/Project";
import Login from "../views/Login";
import User from "../views/User";
import Chat from "../views/Chat";
import NotFound from "@/views/NotFound";
import Search from "@/views/Search";
import UserEdit from "@/views/UserEdit";

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/project/:projectId',
    name: 'Project',
    component: Project
  },
  {
    path: '/project/:projectId/chat/:threadId',
    name: "Chat",
    component: Chat
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/user/:userName',
    name: 'UserPage',
    component: User
  },
  {
    path: '/user/edit',
    name: 'UserEdit',
    component: UserEdit
  },
  {
    path: '/404',
    name: '404',
    component: NotFound
  },
  {
    path: '/search/:keyword',
    name: 'Search',
    component: Search
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
