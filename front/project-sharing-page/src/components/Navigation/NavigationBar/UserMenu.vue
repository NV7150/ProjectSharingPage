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
            <v-card-title>{{user.display_name}}</v-card-title>
          </div>

          <div
            v-for="(item, i) in menuItems"
            :key="i"
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
import PlaceHolder from "../../../assets/img/PlaceHolder.png";

export default {
  name: "UserMenu",
  props: {
    'user': {
      type: Object,
      default:function(){
        return {
          username: '',
          display_name: 'Loading...',
          icon: PlaceHolder
        };
      }
    }
  },
  data(){
    let _this = this;
    return{
      menuItems: [
        {
          name: "Profile",
          func: () => {
            _this.$router.push({
              name:'UserPage',
              params: {
                userName: _this.user.username
              }
            });
            this.$router.go({path: this.$router.currentRoute.path, force: true});
          }
        },
        {
          name: "Logout",
          func: () => {
            _this.$emit('logout');
          }
        }
      ]
    }
  }
}
</script>

<style scoped>

</style>