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
import Navigation from './components/common/Navigation.vue';
import MenuBar from './components/common/MenuBar.vue';
import FooterBar from './components/common/Footer.vue';

export default {
  name: 'App',
  components: { Navigation, MenuBar, FooterBar },
};
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic+Coding&display=swap');

.font-we {
  font-weight: 600;
}

.cur-point {
  cursor: pointer;
}

#app, span {
  font-family: 'Nanum Gothic Coding', monospace;
}

</style>
