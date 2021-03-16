<template>
  <v-container>
    <v-row class="mt-7">
      <v-col cols="12">
        <VueSlickCarousel v-bind="slickData">
          <!-- 페이지 이동권 
            @click="movePage('DeepFakeMovie')"
            가볍게 넘겼는데도 클릭으로 이동함, 특정화면 클릭시 or 이동 편하게 멀 만들어주든가.
           -->
          <v-img
            :src="require('../../assets/fakeImage_banner.png')"
            aspect-ratio="6"
            @click="movePage('DeepFakeMovie')"
          ></v-img>
          <v-img :src="require('../../assets/fakemovie_banner.png')" aspect-ratio="6"></v-img>
          <v-img :src="require('../../assets/example.png')" aspect-ratio="6"></v-img>
        </VueSlickCarousel>
      </v-col>

      <!-- <v-col :key="n" class="mt-2" cols="12">
        <div style="font-weight: bolder; text-align: center">
          <strong class="text-xl-h4 text-lg-h6">공유짤</strong>
        </div>
      </v-col> -->

      <v-col v-for="j in items" :key="`${n}${j}`" cols="12" sm="6" md="4" xl="3">
        <share-list-item />
      </v-col>

      <v-col cols="12">
        <div style="text-align: center">
          <v-btn text @click="more()">The More</v-btn>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import VueSlickCarousel from 'vue-slick-carousel';
import 'vue-slick-carousel/dist/vue-slick-carousel.css';
import 'vue-slick-carousel/dist/vue-slick-carousel-theme.css';
import ShareListItem from '../../components/main/ShareListItem.vue';

export default {
  components: { VueSlickCarousel, ShareListItem },
  data: () => ({
    drawer: null,

    slickData: {
      slidesToShow: 1,
      slidesToScroll: 1,
      speed: 400,
      autoplay: true,
      arrows: false,
      autoplaySpeed: 2000,
      responsive: [
        { breakpoint: 1600, settings: { slidesToShow: 1, slidesToScroll: 1 } },
        { breakpoint: 1200, settings: { slidesToShow: 1, slidesToScroll: 1 } },
        { breakpoint: 750, settings: { slidesToShow: 1, slidesToScroll: 1 } },
      ],
    },

    items: 4,
  }),
  methods: {
    movePage: function (move) {
      this.$router.push({ name: move });
    },
    more() {
      //객체로 추가
      this.items += 4;
    },
  },

  created() {
    window.scrollTo(0, 0);
    //axios하기
    this.items = 4;
  },
};
</script>
