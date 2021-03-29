<template>
  <div id="container">
    <v-container>
      <v-container v-if="isTransfer">
        {{ video.sources.src }}
        <div class="videoContainer" style="margin: auto">
          <my-video :sources="video.sources" :options="video.options"></my-video>
        </div>
      </v-container>
      <v-container v-else style="text-align: center">
        <div>이 자리에는 사용법이 들어갈거임 그리고 동영상 변환하면 동영상으로 바뀜 이자리</div>
      </v-container>

      <div>
        <FileUpload type="image" v-on:fileUpload="removeBackImgUpload" content="배경 이미지"></FileUpload>
        <FileUpload type="video" v-on:fileUpload="removeBackVideoUpload" content="배경제거할 동영상"></FileUpload>
      </div>
      <div style="text-align: center">
        <div>
          <input type="checkbox" name="success" value="success" v-model="checkbox" class="mt-2 mb-5" />
          <span class="agreement-terms ml-2" @click="showAgreement">약관</span>에 동의하십니까?
          <agreement-to-terms />
        </div>
        <v-btn style="width: 30%" x-large color="primary" @click="transfer" :disabled="!checkbox"> 변환하기 </v-btn>
      </div>
      <div style="text-align: center; margin-top: 15px" v-if="btnHide">
        <ShareAndDownBtn :downloadLink="downloadLink" contentType="video"></ShareAndDownBtn>
      </div>
    </v-container>
  </div>
</template>

<script>
import myVideo from 'vue-video';
import FileUpload from '@/components/common/FileUpload.vue';
import ShareAndDownBtn from '@/components/common/ShareAndDownBtn.vue';
import http from '@/util/http-common.js';
import AgreementToTerms from '../common/AgreementToTerms.vue';
import Swal from 'sweetalert2';

export default {
  components: { myVideo, FileUpload, ShareAndDownBtn, AgreementToTerms },
  data() {
    return {
      isHide: true,
      btnHide: false,
      removeBackImg: '',
      removeBackVideo: '',
      downloadLink: '',
      btnHide: false,
      video: {
        sources: [
          {
            src: '',
            type: 'video/mp4',
          },
        ],
        options: {
          controls: true,
          muted: true,
          poster: '',
          autoplay: true,
        },
      },

      checkbox: false,
    };
  },

  methods: {
    async httpCall(formData) {
      await http
        .post('/v1/removeBg', formData)
        .then((response) => {
          this.downloadLink = response.data.url;
          this.video.sources[0].src = this.downloadLink;

          console.log('성공요');
          console.log(this.downloadLink);
          console.log(response);
          Swal.close();
          Swal.fire({
            icon: 'success',
            title: '변환완료',
            showConfirmButton: false,
            timer: 1000,
          });

          this.btnHide = true;
          this.isTransfer = true;
        })
        .catch((error) => {
          console.log('에러요');
          console.log(error);
          console.log(error.response);
        });

      return true;
    },
    async transfer() {
      console.log('배경교체 변환시작');
      let formData = new FormData();
      formData.append('video', this.removeBackVideo);
      formData.append('image', this.removeBackImg);

      await Swal.fire({
        title: '변환중',
        html: '약 10초~30초정도 소요됩니다.',
        timer: 10000000,
        timerProgressBar: true,
        didOpen: () => {
          Swal.showLoading();

          if (this.httpCall(formData)) {
            console.log('????');
          }
        },
        willClose: () => {
          clearInterval();
        },
      }).then((result) => {
        /* Read more about handling dismissals below */
        if (result.dismiss === Swal.DismissReason.timer) {
          console.log('I was closed by the timer');
        }
      });
    },
    removeBackImgUpload(file) {
      this.removeBackImg = file;
      console.log(file);
    },
    removeBackVideoUpload(file) {
      this.removeBackVideo = file;
      console.log(file);
    },
    showAgreement() {
      this.$store.commit('SET_IS_AGREEMENT_TO_TERMS', true);
    },
  },
  computed: {},
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

#fileInput.dragdrop .custom-file,
#fileInput.dragdrop .custom-file-input {
  height: 100px;
}

#fileInput.dragdrop .custom-file-label {
  border: 0;
  border: 5px solid skyblue;
  height: 100px;
  text-align: center;
  color: skyblue;
  padding: 0;
}

#fileInput.dragdrop .custom-file:hover .custom-file-label {
  background: rgb(75, 181, 225);
  color: #fff;
}

#fileInput.dragdrop .custom-file-label::after {
  display: none;
}

/****/
.dropZone {
  /* width: 50%; */
  height: 200px;
  position: relative;
  border: 2px dashed orange;
}

.dropZone:hover {
  border: 2px solid #2e94c4;
}

.dropZone:hover .dropZone-title {
  color: #1975a0;
  color: blue;
}

.dropZone-info {
  color: #a8a8a8;
  position: absolute;
  top: 50%;
  width: 100%;
  transform: translate(0, -50%);
  text-align: center;
}

.dropZone-title {
  color: blue;
}

.dropZone input {
  position: absolute;
  cursor: pointer;
  top: 0px;
  right: 0;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
}

.dropZone-upload-limit-info {
  display: flex;
  justify-content: flex-start;
  flex-direction: column;
}

.dropZone-over {
  background: #5c5c5c;
  opacity: 0.8;
}

.dropZone-uploaded {
  width: 100%;
  height: 200px;
  position: relative;
  border: 2px dashed red;
}

.dropZone-uploaded-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #a8a8a8;
  position: absolute;
  top: 50%;
  width: 100%;
  transform: translate(0, -50%);
  text-align: center;
}

.removeFile {
  width: 200px;
}
</style>
