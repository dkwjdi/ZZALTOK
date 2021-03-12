<template>
  <div>
    <div class="videoContainer">
      <my-video :sources="video.sources" :options="video.options"></my-video>
    </div>
  </div>
</template>

<script>
import myVideo from 'vue-video';

export default {
  components: myVideo,
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
};
</script>

<style scoped>
.videoContainer {
  width: 50%;
  min-width: 600px;

  height: 100%;
}
</style>
