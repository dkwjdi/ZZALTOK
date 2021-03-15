<template>
  <v-app>
    <navigation />
    <menuBar />

    <v-main>
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
.font-we {
  font-weight: 600;
}

.cur-point {
  cursor: pointer;
}
</style>
