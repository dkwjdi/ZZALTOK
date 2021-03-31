<template>
  <v-row class="mt-4" align="center" justify="center">
    <v-col cols="12">
      <div data-aos="fade-up" data-aos-duration="1000">
        <div class="figure">
          <v-img
            :src="thumbnail"
            aspect-ratio="1.6"
            class="img cur-point"
            @click="moveDetail()"
          >
            <div class="img-text">더 보기</div>
          </v-img>
        </div>
        
        <div class="ml-1 mt-3">
          <div class="font-weight-bold text-md-body-1">
            <span class="title-choice" @click="moveDetail()"
              >{{title}}</span>
          </div>
          <div class="font-weight-bold like-lookup mt-1">
            <v-icon small class="mr-1" style="margin-top: -3px">mdi-thumb-up-outline</v-icon>
            <span>{{good}}</span>
            <i class="far fa-eye ml-2"></i> <span>{{view_cnt}}</span>
            <span>&middot;{{regdate}}</span>
          </div>
        </div>
      </div>
    </v-col>
  </v-row>
</template>

<script>
import http from "@/util/http-common.js";

export default {
  props:{
        board_no : {Type : Number},
        title : {Type : String},
        content : {Type : String},
        contentType : {Type : String},
        ip : {Type : String},
        good : {Type : Number},
        regdate : {Type : String},
        imageUrl : {Type : String},
        view_cnt : {Type : String},
  },
  data: () => ({
    thumbnail : '',
  }),
  methods: {
    async moveDetail() {
      await this.$store.dispatch("mainStore/findShareDetail", this.board_no);
      this.$router.push(`/shareDetail?no=${this.board_no}`);
    },
    findThumbnail(){
      http
        .get(`/v1/thumbnails/${this.board_no}.png`)
        .then(() => {
          this.thumbnail = "/api/v1/content/thumbnails/" +this.board_no +".png";
        })
        .catch((error) => {
          console.log("에러", error);
          console.log("에러내용", error.response);
        });
    },
  },
  created(){
    this.findThumbnail();
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
  border-radius: 4px;
}

.img:hover {
  opacity: 0.8;
  -webkit-transform: scale(1.15);
  transform: scale(1.15);
}

.img-text:hover{
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

.like-lookup {
  font-size: 13px;
  color: #888888;
}
</style>
