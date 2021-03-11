<template>
  <v-navigation-drawer
    v-model="getDrawer"
    absolute
    temporary
    right
    width="30vh"
  >
    <v-list-item>
      <v-list-item-content>
        <v-list-item-title>{{ nickname }}</v-list-item-title>
      </v-list-item-content>
    </v-list-item>

    <v-divider></v-divider>

    <v-list dense>
      <v-list-item v-for="item in items" :key="item.title" link>
        <v-list-item-icon>
          <v-icon>{{ item.icon }}</v-icon>
        </v-list-item-icon>

        <v-list-item-content>
          <v-list-item-title>{{ item.title }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
    <button style="display:none" id="chagemenu" @click="OnOffMenu">ddd</button>
  </v-navigation-drawer>
</template>

<script>
import $ from 'jquery';

export default {
  computed: {
    getDrawer: {
      get: function() {
        return this.$store.getters.isOnOffMenu;
      },
      set: function() {},
    },
  },
  data() {
    return {
      items: [
        { title: 'Home', icon: 'mdi-view-dashboard' },
        { title: 'About', icon: 'mdi-forum' },
      ],
      nickname: '',
    };
  },
  updated() {
    // 바탕화면 누르면 vuex 값을 바꿔주기 위해
    $(document).ready(function() {
      $('.v-overlay').on('click', function() {
        $('#chagemenu').trigger('click');
      });
    });
  },
  methods: {
    OnOffMenu: function() {
      this.$store.commit('SET_ON_OFF_MENU', false);
    },
  },
};
</script>
