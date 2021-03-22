import Vue from "vue";
import Vuex from "vuex";
import mainStore from "./modules/mainStore";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    //MenuBar OnOff 정보
    on_off_menu : false,
  },
  getters:{
    isOnOffMenu(state){
      return state.on_off_menu;
    } 
  },
  mutations: {
    SET_ON_OFF_MENU(state, check){
      state.on_off_menu = check;
    }
  },
  actions: {
    
  },
  modules: {
    mainStore : mainStore,
  },
});
