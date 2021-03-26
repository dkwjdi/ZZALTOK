<template>
  <v-container class="main-container" fluid>
    <v-row class="mt-7">
      <slider />
      <v-container>
        <v-row>
          <v-col cols="12">
            <div class="mt-4 ml-5">
            <list-tab />
            </div>
          <v-divider></v-divider>
          </v-col>
          <v-col
            v-for="item in getShareItems"
            :key="item.board_no"
            cols="12"
            sm="6"
            md="4"
            xl="3"
          >
            <share-list-item
              :board_no="item.board_no"
              :title="item.title"
              :content="item.content"
              :contentType="item.contentType"
              :ip="item.ip"
              :good="item.good"
              :regdate="item.regdate"
              :imageUrl="'http://localhost:8000' + JSON.parse(item.content).url"
              :video="'hi'"
              :view_cnt="item.view_cnt"
            />
          </v-col>

          <v-col cols="12">
            <div style="text-align: center">
              <v-btn text @click="more()" class="">The More</v-btn>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </v-row>
  </v-container>
</template>

<script>
import VueSlickCarousel from "vue-slick-carousel";
import "vue-slick-carousel/dist/vue-slick-carousel.css";
import "vue-slick-carousel/dist/vue-slick-carousel-theme.css";
import ShareListItem from "../../components/main/ShareListItem.vue";
import { mapGetters, mapActions } from "vuex";
import Slider from "../../components/main/Slider.vue";
import ListTab from "../../components/main/ListTab.vue";

export default {
  components: { VueSlickCarousel, ShareListItem, Slider, ListTab },
  computed: {
    ...mapGetters("mainStore", ["getShareItems"]),
  },
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

    items: {},
  }),
  methods: {
    ...mapActions("mainStore", ["fetchShareList"]),
    movePage: function (move) {
      this.$router.push({ name: move });
    },
    more() {
      this.$store.commit("mainStore/SET_PAGE_COUNT");
      this.fetchShareList();
    },
  },

  created() {
    window.scrollTo(0, 0);
    //axios하기
    this.fetchShareList();
  },
};
</script>

<style>
.main-container {
  margin-top: -40px;
}
</style>
