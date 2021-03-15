<template>
  <div id="container">
    <v-container>
      <v-container>
        <div class="videoContainer" style="margin:auto">
          <my-video
            :sources="video.sources"
            :options="video.options"
          ></my-video>
        </div>
      </v-container>

      <div>
        <v-container>
          <div v-if="!file" style="margin:auto; width:50%">
            <div
              :class="['dropZone', dragging ? 'dropZone-over' : '']"
              @dragenter="dragging = true"
              @dragleave="dragging = false"
            >
              <div class="dropZone-info" @drag="onChange">
                <span class="fa fa-cloud-upload dropZone-title"></span>
                <span class="dropZone-title">배경제거 동영상 Drag&Drop</span>
                <div class="dropZone-upload-limit-info">
                  <!-- <div>extension support: image</div> -->
                  <div>maximum file size: 5 MB</div>
                </div>
              </div>
              <input type="file" @change="onChange" />
            </div>
          </div>

          <div v-else style="margin:auto; width:50%" class="dropZone-uploaded">
            <div class="dropZone-uploaded-info">
              <span class="dropZone-title">Uploaded</span>
              <button
                style="color:red; "
                type="button"
                class="btn btn-primary removeFile"
                @click="removeFile"
              >
                파일삭제
              </button>
            </div>
          </div>
        </v-container>

        <div class="uploadedFile-info">
          <div>fileName: {{ file.name }}</div>
          <div>fileZise(bytes): {{ file.size }}</div>
          <div>extension：{{ extension }}</div>
        </div>
      </div>
      <v-row no-gutters justify="center">
        <v-col cols="auto">
          <div class="my-2">
            <v-btn x-large color="primary" dark>변환하기</v-btn>
          </div>
          <v-btn>
            <a
              href="https://www.w3schools.com/tags/movie.mp4"
              target="_blank"
              download="file.mp4"
              >Download</a
            >
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import myVideo from 'vue-video';

export default {
  components: { myVideo },
  data() {
    return {
      file: '',
      dragging: false,
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
    onChange(e) {
      var files = e.target.files || e.dataTransfer.files;

      if (!files.length) {
        this.dragging = false;
        return;
      }

      this.createFile(files[0]);
    },
    createFile(file) {
      if (!file.type.match('mp4.*')) {
        alert('please select mp4 file');
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
  },
  computed: {
    extension() {
      return this.file ? this.file.name.split('.').pop() : '';
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
