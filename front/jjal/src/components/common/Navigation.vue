<template>
  <v-app-bar app color="white" flat id="navbar" height="80vh">
    <img
      :src="require('../../assets/Nav_Logo.png')"
      class="nav-choice ml-5"
      @click="movePage('Main')"
      style="height: 80px"
    />

    <ul class="nav_mian hidden-sm-and-down">
      <li class="nav_title nav-choice" @click="movePage('DeepFakeImage')">명언생성</li>
      <li class="nav_title nav-choice" @click="movePage('DeepFakeMovie')">다메다메</li>
      <li class="nav_title nav-choice" @click="movePage('RemoveBack')">나만의 배경</li>
    </ul>

    <v-spacer></v-spacer>

    <v-app-bar-nav-icon class="hidden-md-and-up" @click="OnOffMenu"></v-app-bar-nav-icon>
  </v-app-bar>
</template>

<script>
export default {
  data() {
    return { drawer: null };
  },
  created() {},
  methods: {
    movePage: function (move) {
      this.$router.push({ name: move });
      this.$store.commit('SET_ON_OFF_MENU', false);
    },
    OnOffMenu() {
      this.$store.commit('SET_ON_OFF_MENU', true);
    },
  },
};
</script>

<style>
#navbar {
  outline: 1px solid rgb(225, 225, 225);
}

ul li {
  list-style-type: none;
  float: left;
  margin: 20px;
  font-weight: 600;
}

.nav-choice:hover {
  cursor: pointer;
  color: #3395f4;
}
</style>
