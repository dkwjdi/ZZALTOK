<template>
  <div id="container">
    <v-container>
      <v-container v-if="isTransfer">
        <div class="videoContainer" style="margin: auto">
          <my-video style="z-index: -1" :sources="video.sources" :options="video.options"></my-video>
        </div>
      </v-container>
      <v-container v-else style="text-align: center">
        <div>이 자리에는 사용법이 들어갈거임 그리고 동영상 변환하면 동영상으로 바뀜 이자리</div>
      </v-container>

      <div>
        <FileUpload type="image" v-on:fileUpload="deepFakeMovieUpload" content="다메다메 밈 이미지"></FileUpload>
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
import http from '@/util/http-common.js';
import FileUpload from '@/components/common/FileUpload.vue';
import ShareAndDownBtn from '@/components/common/ShareAndDownBtn.vue';
import AgreementToTerms from '../common/AgreementToTerms.vue';
import Swal from 'sweetalert2';

export default {
  components: {
    myVideo,
    FileUpload,
    ShareAndDownBtn,
    AgreementToTerms,
  },
  data() {
    return {
      isHide: true,
      btnHide: false,
      damedameImg: '',
      downloadLink: '',
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
    transfer() {
      let formData = new FormData();
      console.log(this.damedameImg);
      formData.append('image', this.damedameImg);

      let timerInterval;
      Swal.fire({
        title: '변환중',
        html: '약 30초~1분정도 소요됩니다.',
        timer: 10000000,
        timerProgressBar: true,
        didOpen: () => {
          Swal.showLoading();

          http
            .post('/v1/damedame', formData)
            .then((response) => {
              // alert('변환완료'); -> 이거 대신에 SWAL사용
              this.downloadLink = response.data.url;
              this.video.sources[0].src = this.downloadLink;

              console.log('성공요');
              console.log(this.downloadLink);
              console.log(response);
              Swal.close();
              // 여기서 새로운 SWAL창 띄어주기
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
              Swal.close();
              console.log(error.response);
            });
        },
        willClose: () => {
          clearInterval(timerInterval);
        },
      }).then((result) => {
        /* Read more about handling dismissals below */
        if (result.dismiss === Swal.DismissReason.timer) {
          console.log('I was closed by the timer');
        }
      });
    },
    deepFakeMovieUpload(file) {
      console.log('파일업로드완료');
      console.log(file);
      this.damedameImg = file;
    },
    showAgreement() {
      this.$store.commit('SET_IS_AGREEMENT_TO_TERMS', true);
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
