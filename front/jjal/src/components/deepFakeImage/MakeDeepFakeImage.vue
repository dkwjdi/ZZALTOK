<template>
  <v-app>
    <div>
      {{ a }}
      <div>
        <v-container>
          <v-row justify="center">
            <v-col></v-col>
            <v-col cols="4" ref="printMe">
              <v-textarea
                hide-details
                name=""
                id=""
                height="600"
                full-width
                :style="cssProps"
              ></v-textarea>
            </v-col>
            <v-col></v-col>
          </v-row>
        </v-container>
        <img style="display: none" :src="output" alt="" />

        <!--  -->

        <v-container>
          <div v-if="!file" style="margin: auto; width: 50%">
            <div
              :class="['dropZone', dragging ? 'dropZone-over' : '']"
              @dragenter="dragging = true"
              @dragleave="dragging = false"
            >
              <div class="dropZone-info" @drag="onChange">
                <span class="fa fa-cloud-upload dropZone-title"></span>
                <span class="dropZone-title"
                  >다메다메밈 생성 사진 Drag&Drop</span
                >
                <div class="dropZone-upload-limit-info">
                  <!-- <div>extension support: image</div> -->
                  <div>maximum file size: 5 MB</div>
                </div>
              </div>
              <input type="file" @change="onChange" />
            </div>
          </div>

          <div
            v-else
            class="dropZone-uploaded"
            style="margin: auto; width: 50%"
          >
            <div class="dropZone-uploaded-info">
              <span class="dropZone-title">Uploaded</span>
              <button
                style="color: red"
                type="button"
                class="btn btn-primary removeFile"
                @click="removeFile"
              >
                파일삭제
              </button>
            </div>
          </div>
        </v-container>

        <!--  -->

        <v-btn @click="print"> 변환하기</v-btn>
      </div>
      <div>
        <v-btn>
          <a
            id="downloadPhoto"
            download="my-photo.jpg"
            class="button"
            role="button"
            @click="down"
          >
            Download
          </a>
        </v-btn>
      </div>
      <v-img
        max-height="100%"
        max-width="100%"
        v-if="downloadLink"
        :src="downloadLink"
      ></v-img>
    </div>
  </v-app>
</template>

<script>
import http from '@/util/http-common.js';

export default {
  data() {
    return {
      a: 'a',
      file: '',
      dragging: false,
      output: null,
      downloadLink: '',
      cssProps: {
        backgroundImage: `url(${require('@/assets/nineone.png')})`,
      },
    };
  },
  methods: {
    onChange(e) {
      var files = e.target.files || e.dataTransfer.files;

      if (!files.length) {
        this.dragging = false;
        return;
      }

      this.createFile(files[0]);
    },
    createFile(file) {
      if (!file.type.match('image*')) {
        alert('please select image file');
        this.dragging = false;
        return;
      }

      if (file.size > 5000000) {
        alert('please check file size no over 5 MB.');
        this.dragging = false;
        return;
      }

      this.file = file;
      console.log(this.file);
      this.dragging = false;
    },
    removeFile() {
      this.file = '';
    },
    down() {
      console.log('down'); //사진 다운로드 할 때 쓰는데 일단은 사용  x
      const download = document.getElementById('downloadPhoto');
      console.log(download);
      download.setAttribute('href', this.output); //파일생성
    },
    async print() {
      const el = this.$refs.printMe; //캔버스 들고와서
      const options = {
        type: 'dataURL',
      };

      this.a = 'asdf';

      this.output = await this.$html2canvas(el, options); //canvas에 그려서 output이 가지고 있음
      const decodImg = atob(this.output.split(',')[1]);

      let array = [];
      for (let i = 0; i < decodImg.length; i++) {
        array.push(decodImg.charCodeAt(i));
      }
      console.log('canvas-> file 변환');
      const target = new Blob([new Uint8Array(array)], { type: 'image/jpeg' }); //canvas 값으 Blob배열형태로 저장해줌

      let formData = new FormData(); //폼데이터 만들고
      formData.append('origin', this.file); // 삽입할 사진
      formData.append('target', target); // 합성 당할사진

      http
        .post('/v1/deepfake', formData)
        .then((response) => {
          alert('변환완료');
          this.downloadLink =
            'http://localhost:8000' + response.data.url + '?download=true'; //바로 다운받을 수 있게 downloadLink에다가 url넣어줌
          console.log('성공 + 다운로드링크');
          console.log(this.downloadLink);
        })
        .catch((error) => {
          console.log('에러 + 에러내용');
          console.log(error);
          console.log(error.response);
        });
    },
  },
  computed: {
    extension() {
      return this.file ? this.file.name.split('.').pop() : '';
    },
  },
};
</script>

<style scoped>
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
