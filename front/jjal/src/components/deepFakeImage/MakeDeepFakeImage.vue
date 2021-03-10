<template>
  <v-app>
    <div>
      <div>
        <!-- SOURCE -->
        <div ref="printMe" style="padding: 10px; background: #f5da55">
          <textarea name="" id="" cols="30" rows="10" class="a"></textarea>
        </div>
        <img style="display:none" :src="output" alt="" />
        <v-btn @click="print"> 캔버스에 그리기</v-btn>
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
    </div>
  </v-app>
</template>

<script>
export default {
  data() {
    return {
      output: null,
    };
  },
  methods: {
    down() {
      console.log('down');
      const download = document.getElementById('downloadPhoto');
      console.log(download);
      download.setAttribute('href', this.output); //파일생성
    },
    async print() {
      const el = this.$refs.printMe;
      const options = {
        type: 'dataURL',
      };

      this.output = await this.$html2canvas(el, options);
    },
  },
};
</script>

<style scoped>
.a {
  background-image: url('assets/asf.png');
}
</style>
