<template>
  <v-app>
    <div>
      <div>
        <div :class="{ hide: isHide }">
          <v-container>
            <!-- <img :src="previewImgUrl" alt="" /> -->
            <v-row no-gutters justify="center" ref="printMe" style="margin-right: 50px; margin-left: 50px">
              <v-col cols="3"></v-col>

              <v-col> <img :src="previewImgUrl" alt="" style="width: 100%; height: 100%" /> </v-col>
              <v-col class="font-change" style="background: black; text-align: center">
                <div style="color: white"><p v-html="OutProverbContent"></p></div>
                <div style="color: white"><p v-html="OutProverbName"></p></div>
              </v-col>

              <v-col cols="3"></v-col>
            </v-row>
          </v-container>
        </div>

        <FileUpload type="image" v-on:fileUpload="originUpload" content="배경 사진"></FileUpload>
        <FileUpload type="image" v-on:fileUpload="targetUpload" content="합성 할 사진"></FileUpload>

        <v-container>
          <v-row no-gutters justify="center">
            <v-col></v-col>
            <v-col>
              명언
              <textarea
                label="명언입력"
                hide-details="auto"
                v-model="proverb.proverbContent"
                style="resize: none; width: 100%; border: 1px solid black"
              ></textarea>
            </v-col>

            <v-col></v-col>
          </v-row>
          <v-row no-gutters justify="center">
            <v-col></v-col>
            <v-col>
              이름
              <textarea style="resize: none; width: 100%; border: 1px solid black" label="이름입력" v-model="proverb.proverbName"></textarea>
            </v-col>
            <v-col></v-col>
          </v-row>
        </v-container>

        <!-- <img :src="output" alt="" />  캔버스  -->

        <!--  -->

        <v-btn @click="print"> 변환하기</v-btn>
      </div>
      <div style="text-align: center">
        <ShareAndDownBtn :downloadLink="boardWritedownloadLink" contentType="image"></ShareAndDownBtn>

        <v-btn>
          <!-- <a id="downloadPhoto" download="my-photo.jpg" class="button" role="button" @click="down"> Download </a> -->
        </v-btn>
      </div>
      <!-- <v-img max-height="100%" max-width="100%" v-if="downloadLink" :src="downloadLink"></v-img> -->
    </div>
  </v-app>
</template>

<script>
import http from '@/util/http-common.js';
import FileUpload from '@/components/common/FileUpload.vue';
import ShareAndDownBtn from '@/components/common/ShareAndDownBtn.vue';
import Swal from 'sweetalert2';

export default {
  data() {
    return {
      isHide: true,
      previewImgUrl: '',
      downloadLink: '',
      boardWritedownloadLink: '',
      proverb: {
        //명언 내용, 이름
        proverbContent: '',
        proverbName: '',
      },
      file: {
        origin: '',
        target: '',
      },
      // imgPath: require('@/assets/nineone.png'),
    };
  },
  components: {
    FileUpload,
    ShareAndDownBtn,
  },
  methods: {
    originUpload(file) {
      this.previewImgUrl = URL.createObjectURL(file);
      this.isHide = false;
      //FileUpload 컴포넌트에서 #emit으로 불러서 파일전해줌
      console.log('오리진파일 업로드');
      this.file.origin = file;
      console.log(this.file.origin);
    },
    targetUpload(file) {
      //FileUpload 컴포넌트에서 #emit으로 불러서 파일전해줌
      console.log('타겟파일 업로드');
      this.file.target = file;
      console.log(this.file.target);
    },

    async print() {
      const el = this.$refs.printMe; //캔버스 들고와서
      const options = {
        type: 'dataURL',
      };

      this.output = await this.$html2canvas(el, options); //canvas에 그려서 output이 가지고 있음
      // console.log('output');
      // console.log(this.output);
      const decodImg = atob(this.output.split(',')[1]);

      let array = [];
      for (let i = 0; i < decodImg.length; i++) {
        array.push(decodImg.charCodeAt(i));
      }
      console.log('canvas-> file 변환');
      const target = new Blob([new Uint8Array(array)], { type: 'image/jpeg' }); //canvas 값으 Blob배열형태로 저장해줌

      let formData = new FormData(); //폼데이터 만들고
      formData.append('origin', this.file.target); // 삽입할 사진
      formData.append('target', target); // 합성 당할사진

      // this.removeFile(); //파일 자동삭제

      http
        .post('/v1/deepfake', formData)
        .then((response) => {
          this.downloadLink = response.data.url + '?download=true'; //바로 다운받을 수 있게 downloadLink에다가 url넣어줌
          this.boardWritedownloadLink = response.data.url;
          console.log(this.downloadLink);
          console.log('성공 + 다운로드링크');
          console.log(this.downloadLink);
          Swal.fire({
            title: 'Sweet!',
            text: 'Modal with a custom image.',
            imageUrl: this.downloadLink,
            imageWidth: 2000,
            imageHeight: 400,
            width: 1000,

            imageAlt: 'Custom image',
          });
        })
        .catch((error) => {
          console.log('에러 + 에러내용');
          console.log(error);
          console.log(error.response);
        });

      //파일 삭제 하기
      // this.$swal('Heading', 'this is a Heading', 'OK');
    },
  },
  computed: {
    extension() {
      return this.file ? this.file.name.split('.').pop() : '';
    },
    OutProverbContent() {
      return this.proverb.proverbContent.replace(/\n/g, '<br>').replace(/ /g, '&nbsp');
    },
    OutProverbName() {
      return this.proverb.proverbName.replace(/\n/g, '<br>').replace(/ /g, '&nbsp');
    },
  },
};
</script>

<style scoped>
.hide {
  display: none;
}
.font-change {
  font-family: 'Yeon Sung', cursive;
  font-size: 2rem;
}
.swal2-popup {
  font-size: 1.6rem !important;
}
.swal-wide {
  width: 850px !important;
}
</style>
