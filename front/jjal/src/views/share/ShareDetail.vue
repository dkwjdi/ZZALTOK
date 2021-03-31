<template>
  <v-container fluid class="back-img">
    <v-row class="mt-2">
      <v-col cols="1" md="2"></v-col>
      <v-col cols="12" md="8">
        <div class="box-shadow">
          <!-- 메뉴 -->
          <div class="hidden-md-and-up" style="float: right">
            <v-menu bottom left>
              <template v-slot:activator="{ on, attrs }">
                <v-btn icon v-bind="attrs" v-on="on" class="mt-5 mr-1">
                  <v-icon>mdi-dots-vertical</v-icon>
                </v-btn>
              </template>

              <v-list>
                <v-list-item v-for="(item, i) in listItem" :key="i">
                  <v-list-item-title class="menu-choice">{{
                    item.title
                  }}</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </div>

          <div class="pt-3 pl-2">
            <v-avatar
              color="indigo"
              size="53"
              style="float: left"
              class="mr-3 mt-1"
            >
              <v-icon dark> mdi-account-circle </v-icon>
            </v-avatar>
            <div style="padding-top: -10px">
              <div class="font-weight-bold title">
                <span>{{ getShareDetail.title }}</span>
              </div>
              <div class="subtitle-2">
                <span>{{ getShareDetail.nickname }} </span>
                <span style="font-size: 12px; color: #888888"
                  >({{ getShareDetail.ip }})</span
                >
              </div>
            </div>
          </div>

          <v-img
            v-if="getShareDetail.content_type == 'image'"
            :src="getShareDetail.url"
            aspect-ratio="1.6"
            class="detail-img mt-3"
          >
          </v-img>
          <my-video
            v-if="getShareDetail.content_type == 'video'"
            :sources="getVideo()"
            :options="video.options"
          ></my-video>

          <div class="text-main">
            <!-- <div class="mt-5 detail-text">
            <div class="text-h5">제목</div>
            <div class="mt-2 body-2">조회수 10회 | 2021.03.16</div>
            <div class="mt-2 body-2">by 익명</div>
          </div> -->

            <v-sheet min-height="100px">
              <v-sheet>
                <v-row>
                  <v-col cols="1"></v-col>
                  <v-col cols="10">
                    <div class="pt-5 pl-5">{{ getShareDetail.content }}</div>

                    <div class="text-center mt-10">
                      <v-btn
                        color="indigo"
                        fab
                        large
                        dark
                        @click="updateDetailLike(getShareDetail.board_no)"
                      >
                        <i class="fas fa-thumbs-up fa-lg"></i>
                      </v-btn>
                      <div class="mt-3">
                        <i class="fas fa-thumbs-up mr-1"></i
                        >{{ getShareDetail.good }}
                        <i class="far fa-eye ml-1"></i>
                        {{ getShareDetail.view_cnt }}
                        <i class="fas fa-comment"></i> {{ getCommentSize }}
                      </div>

                      <div class="mt-2">
                        게시일 : {{ getShareDetail.regdate }}
                      </div>
                    </div>
                  </v-col>
                </v-row>
              </v-sheet>
            </v-sheet>
          </div>

          <!-- 댓글 -->
          <v-container>
            <v-sheet class="mt-10 mb-5">
              <comment-list />
            </v-sheet>
          </v-container>
        </div>
      </v-col>
      <v-col cols="1" md="2">
        <menu-btn
          :board_no="getShareDetail.board_no"
          :title="getShareDetail.title"
          :content="getShareDetail.content"
          :url="getShareDetail.url"
          :content_type="getShareDetail.content_type"
          :nickname="getShareDetail.nickname"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import CommentList from "../../components/shareDetail/CommentList.vue";
import { mapGetters, mapActions } from "vuex";
import MenuBtn from "../../components/shareDetail/MenuBtn.vue";
import myVideo from "vue-video";
import $ from "jquery";

export default {
  components: { CommentList, MenuBtn, myVideo },

  computed: {
    ...mapGetters("mainStore", ["getShareDetail", "getCommentSize"]),
  },
  data: () => ({
    shareItem: {},
    listItem: [
      { title: "수정" },
      { title: "삭제" },
      { title: "공유" },
      { title: "Download" },
    ],
    video: {
      options: {
        controls: true,
        muted: true,
        poster: "https://ifh.cc/g/fP091M.jpg",
      },
    },
  }),
  methods: {
    ...mapActions("mainStore", ["findShareDetail", "updateDetailLike"]),
    getVideo() {
      return {
        sources: {
          src: this.getShareDetail.url,
          type: "video/mp4",
        },
      };
    },
  },
  created() {
    window.scrollTo(0, 0);
    this.findShareDetail(this.$route.query.no);
  },

  mounted() {
    // appbar 관리
    $("#nav-ul-id").removeClass("main-bar");
    $("#nav-ul-id").addClass("func-bar");
    $(".nav_ul").css("color", "black");
    $("#navbar").css("background-color", "#ffffff");
  },
};
</script>

<style>
.detail-text {
  padding-bottom: 10px;
  border-bottom: 1px solid rgb(225, 225, 225);
}

.detail-img {
  display: block;
  margin: auto;
}

.back-img {
  background-color: rgb(249, 249, 249);
}

.box-shadow {
  box-shadow: 5px 5px 5px 5px gray;
}

.v-btn--example {
  position: fixed;
}

.menu-choice:hover {
  cursor: pointer;
  color: #3395f4;
}
</style>
