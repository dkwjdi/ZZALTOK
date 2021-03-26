<template>
  <v-app id="app">
    <navigation />
    <menuBar />

    <v-main class="main-back">
      <router-view />
    </v-main>

    <footerBar />
  </v-app>
</template>

<script>
import Navigation from "./components/common/Navigation.vue";
import MenuBar from "./components/common/MenuBar.vue";
import FooterBar from "./components/common/Footer.vue";
import $ from 'jquery';

export default {
  name: "App",
  components: { Navigation, MenuBar, FooterBar },
  created() {
    $(window).scroll(function (e) {
      if ($(document).scrollTop() !== 0) {
        $('.v-toolbar__content').css('box-shadow','0 0 6px 2px rgb(0 0 0 / 16%)');
      } else {
        console.log("정지!")
        $('.v-toolbar__content').css('box-shadow','');
      }
    });
  },
};
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=Nanum+Gothic+Coding&display=swap");

.font-we {
  font-weight: 600;
}

.cur-point {
  cursor: pointer;
}

.shadow{
  box-shadow: 0 1px 6px 0 rgb(32 33 36 / 28%);
}

#app,
span {
  font-family: "Nanum Gothic Coding", monospace;
}
</style>
