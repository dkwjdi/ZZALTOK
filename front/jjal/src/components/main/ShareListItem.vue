<template>
  <v-row align="center" justify="center" class="ml-1 mr-1">
    <v-col cols="12">
      <div data-aos="fade-up" data-aos-duration="1000">
        <div class="figure">
          <v-img
            :src="require('../../assets/example.png')"
            aspect-ratio="1.5"
            class="img cur-point"
            @click="moveDetail()"
          >
            <div class="img-text">더 보기</div>
          </v-img>
        </div>
        <div class="ml-1 mt-3">
          <div class="mt-1 font-weight-bold text-md-body-1">
            <span class="title-choice" @click="moveDetail()">제목</span>
          </div>
          <div class="mt-1">
            <i class="far fa-heart mr-1"></i>58 <i class="far fa-eye ml-1"></i> 100
          </div>
        </div>
      </div>
    </v-col>
  </v-row>
</template>

<script>
export default {
  data: () => ({
    no: 1,
  }),
  methods: {
    moveDetail() {
      this.$router.push(`/shareDetail?no=${this.no}`);
    },
  },
};
</script>

<style>
.figure {
  position: relative;
  overflow: hidden;
  cursor: pointer;
  -webkit-transition: all 0.35s ease;
  transition: all 0.35s ease;
}
.img {
  z-index: 1;
  -webkit-transform: all 0.5s ease;
  transition: all 0.5s ease;
  overflow: hidden;
  border-radius: 5px;
}

.img:hover {
  opacity: 0.8;
  -webkit-transform: scale(1.15);
  transform: scale(1.15);
}

.img:hover .img-text {
  opacity: 0.8;
  text-align: center;
  color: #ffffff;
}

.img-text {
  opacity: 0;
  transform: scale(2);
  transition: all 0.3s linear;
  padding-top: 80px;
}

.title-choice:hover {
  cursor: pointer;
  border-bottom: 0.5px solid rgb(112, 108, 108);
}
</style>
