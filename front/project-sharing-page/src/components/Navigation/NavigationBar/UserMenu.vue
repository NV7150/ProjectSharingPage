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
          <v-img :src="user.icon" />
        </v-avatar>
      </v-btn>
    </template>

    <v-card class="justify-center" max-width="30vw">
      <v-card-text>
        <v-list-item class="text-center justify-center">
          <v-avatar>
            <v-img :src="user.icon" />
          </v-avatar>
        </v-list-item>

        <v-list-item class="text-center justify-center">
          <v-card-title>
            {{user.display_name}}
          </v-card-title>
        </v-list-item>

        <v-divider class="my-3"></v-divider>

        <v-list-item
          v-for="(item, i) in menuItems"
          :key="i"
        >
          <v-btn
            text
            block
            depressed
            @click="item.func()"
          >
            {{item.name}}
          </v-btn>
        </v-list-item>
      </v-card-text>
    </v-card>

  </v-menu>
</template>

<script>
import PlaceHolder from "@/assets/img/PlaceHolder.png";

export default {
  name: "UserMenu",
  props: {
    'user': {
      type: Object,
      default:function(){
        return {
          username: 'aaaaaa',
          display_name: 'Loading...',
          icon: PlaceHolder
        };
      }
    }
  },
  data(){
    return{
      menuItems: [
        {
          name: "Profile",
          func: () => {
            this.$router.push({
              name:'UserPage',
              params: {
                userName: this.user.username
              }
            });
            this.$router.go({path: this.$router.currentRoute.path, force: true});
          }
        },
        {
          name: "Edit",
          func: () =>{
            this.$router.push({
              name: "UserEdit"
            });
          }
        },
        {
          name: "Change Password",
          func: () => {
            this.$router.push({
              name: "PassEdit"
            });
          }
        },
        {
          name: "New project",
          func: () => {
            this.$router.push({
              name: "newProject"
            });
          }
        },
        {
          name: "Logout",
          func: () => {
            this.$emit('logout');
          }
        }
      ],
    }
  }
}
</script>

<style scoped>

</style>