import axios from "axios";

export default {
    state : () => ({
        user: null,
        isLoggedIn : false
    }),
    mutations: {
        setUser(state, user){
            state.user = user;
            state.isLoggedIn = true;
        },
        removeUser(state){
            state.user = null;
            state.isLoggedIn = false;
        }
    },
    actions: {
        checkLogin(context){
            return new Promise((resolve) => {
                axios
                    .get('/userapi/user')
                    .then((response) => {
                        context.commit('setUser', response.data);
                        resolve();
                    })
                    .catch(() => {
                        context.commit('removeUser');
                        resolve();
                    });
            });
        }
    },
    getters: {
        getUser : (state) => {return state.user;},
        getIsLoggedIn : (state) =>{return state.isLoggedIn;}
    }
}