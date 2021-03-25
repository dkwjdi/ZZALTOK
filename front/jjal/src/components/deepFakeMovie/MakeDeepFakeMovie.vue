<template>
  <div id="container">
    <v-container>
      <v-container>
        <div class="videoContainer" style="margin: auto">
          <my-video :sources="video.sources" :options="video.options"></my-video>
        </div>
      </v-container>

      <div>
        <FileUpload type="image" v-on:fileUpload="deepFakeMovieUpload" content="다메다메 밈 이미지"></FileUpload>

        <div class="uploadedFile-info">
          <div>fileName: {{ damedameImg.name }}</div>
          <div>fileZise(bytes): {{ damedameImg.size }}</div>
          <!-- <div>extension：{{ extension }}</div> -->
        </div>
      </div>
      <v-row no-gutters justify="center">
        <v-col cols="auto">
          <div class="my-2">
            <v-btn @click="transfer" x-large color="primary" dark>변환하기</v-btn>
          </div>
          <v-btn>
            <a :href="downloadLink" target="_blank" download="file.mp4">Download</a>
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
    <ShareAndDownBtn :downloadLink="downloadLink" contentType="video"></ShareAndDownBtn>
  </div>
</template>

<script>
import myVideo from 'vue-video';
import http from '@/util/http-common.js';
import FileUpload from '@/components/common/FileUpload.vue';
import ShareAndDownBtn from '@/components/common/ShareAndDownBtn.vue';
export default {
  components: {
    myVideo,
    FileUpload,
    ShareAndDownBtn,
  },
  data() {
    return {
      damedameImg: '',
      downloadLink: '',
      video: {
        sources: [
          {
            src: 'https://www.w3schools.com/tags/movie.mp4',
            type: 'video/mp4',
          },
        ],
        options: {
          controls: true,
          muted: true,
          poster: 'https://ifh.cc/g/fP091M.jpg',
        },
      },
    };
  },

  methods: {
    transfer() {
      console.log('다메다메 변환시작');
      let formData = new FormData();
      console.log(this.damedameImg);
      formData.append('image', this.damedameImg);
      http
        .post('/v1/damedame', formData)
        .then((response) => {
          alert('변환완료');
          this.downloadLink = response.data.url;

          console.log('성공요');
          console.log(this.downloadLink);
          console.log(response);
        })
        .catch((error) => {
          console.log('에러요');
          console.log(error);
          console.log(error.response);
        });
    },
    deepFakeMovieUpload(file) {
      console.log('파일업로드완료');
      console.log(file);
      this.damedameImg = file;
    },
  },
};
</script>

<style scoped>
.videoContainer {
  width: 50%;
  /* min-width: 600px; */
  height: 80%;
}

.input-file-button {
  padding: 6px 25px;
  background-color: #ff6600;
  border-radius: 10px;
  color: white;
  cursor: pointer;
}

#preview img {
  max-width: 100%;
}
</style>
