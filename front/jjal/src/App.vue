<template>
  <v-app>
    <navigation />
    <menuBar />

    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
import Navigation from "./components/common/Navigation.vue";
import MenuBar from "./components/common/MenuBar.vue";

export default {
  name: "App",
  components: { Navigation, MenuBar },
  data: () => ({}),
};
</script>
