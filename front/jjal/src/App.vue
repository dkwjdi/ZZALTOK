<template>
  <v-app>
    <navigation />
    <menuBar />

    <v-main>
      <div class="videoContainer">
        <my-video :sources="video.sources" :options="video.options"></my-video>
      </div>
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
import Navigation from './components/common/Navigation.vue';
import MenuBar from './components/common/MenuBar.vue';
import myVideo from 'vue-video';

export default {
  name: 'App',
  components: { Navigation, MenuBar, myVideo },
  data() {
    return {
      video: {
        sources: [
          {
            src: 'https://www.w3schools.com/tags/movie.mp4',
            type: 'video/mp4',
          },
        ],
        options: {
          autoplay: true,
          controls: true,
          muted: true,
          poster: 'http://covteam.u.qiniudn.com/poster.png',
        },
      },
    };
  },

  created() {},
};
</script>

<style scoped>
.videoContainer {
  width: 50%;
  min-width: 600px;

  height: 100%;
}
</style>
