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
import CreateProject from "@/views/CreateProject";
import ErrorPage from "@/views/ErrorPage";

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
    component: Project,
    props: (route) => {
      let tab = (Number)((!isNaN(route.query.tab)) ? route.query.tab : 0);
      let channel = (Number)((!isNaN(route.query.channel)) ? route.query.channel : -1);
      let thread = (Number)((!isNaN(route.query.thread)) ? route.query.thread : -1);
      return{
        initTab: tab ,
        initChannel : channel,
        initThread : thread
      }
    }
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
    path: '/search/:keyword',
    name: 'Search',
    component: Search,
  },
  {
    path: '/newProject',
    name: 'newProject',
    component: CreateProject
  },
  {
    path: "/Error",
    name: "Error",
    component: ErrorPage
  },


  {
    path: '*',
    name: '404',
    component: NotFound
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
