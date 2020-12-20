<template>
  <v-menu
      bottom
      offset-y
  >
    <template v-slot:activator="{on}">
      <v-btn
        v-on="on"
        icon
      >
        <v-avatar>
          <img :src="user.icon">
        </v-avatar>
      </v-btn>
    </template>

    <v-card class="justify-center">
      <v-list-item-content>
        <v-card-text>
          <div class="mx-auto text-center">
            <v-avatar>
              <img :src="user.icon">
            </v-avatar>
            <v-card-title>{{user.name}}</v-card-title>
          </div>

          <div
            v-for="item in menuItems"
            :key="item"
          >
            <v-divider class="my-3"></v-divider>
            <v-btn
              text
              block
              depressed
              @click="item.func()"
            >
              {{item.name}}
            </v-btn>
          </div>
        </v-card-text>
      </v-list-item-content>
    </v-card>

  </v-menu>
</template>

<script>
import axios from "axios";

export default {
  name: "UserMenu",
  data(){
    return{
      menuItems: [
        {
          name: "Profile",
          func: () => {

          }
        },
        {
          name: "Logout",
          func: () => {
            axios.post("userapi/logout");
          }
        }

      ]
    }
  },
  computed:{
    user(){
      //TODO:ユーザの取得
      //仮置き
      return {
        name: "TestUser",
        icon: "https://gochiusa.com/core_sys/images/contents/00000022/base/l1.png"
      };
    }
  },
  methods: {
  }
}
</script>

<style scoped>

</style>