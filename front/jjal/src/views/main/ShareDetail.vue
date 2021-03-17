<template>
  <v-container fluid class="back-img">
    <v-row class="mt-2">
      <v-col cols="1" md="2"></v-col>
      <v-col cols="12" md="8">
        <div class="box-shadow">
          <div class="pt-3 pl-2">
            <v-avatar color="indigo" size="53" style="float: left" class="mr-3">
              <v-icon dark> mdi-account-circle </v-icon>
            </v-avatar>
            <div style="padding-top: -10px">
              <div class="font-weight-bold title">제목</div>
              <div class="subtitle-2">사용자</div>
            </div>
          </div>

          <v-img
            :src="require('../../assets/example.png')"
            aspect-ratio="1.5"
            @click="moveDetail()"
            class="detail-img mt-3"
          >
          </v-img>

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
                    <div class="pt-5 pl-5">내용</div>

                    <div class="text-center mt-10">
                      <v-btn color="indigo" fab large dark>
                        <i class="fas fa-thumbs-up fa-lg"></i>
                      </v-btn>
                      <div class="mt-3">
                        <i class="fas fa-thumbs-up mr-1"></i>50 <i class="far fa-eye ml-1"></i> 100
                        <i class="fas fa-comment"></i> 2
                      </div>

                      <div class="mt-2">게시일 : 2021. 03. 16</div>
                    </div>
                  </v-col>
                </v-row>
              </v-sheet>
            </v-sheet>
          </div>

          <!-- 댓글 -->
          <v-container>
            <v-sheet class="mt-10 mb-5">
              <comment-form :type="'create'" />

              <v-divider></v-divider>

              <comment-list />
            </v-sheet>
          </v-container>
        </div>
      </v-col>
      <v-col cols="1" md="2"></v-col>
    </v-row>
  </v-container>
</template>

<script>
import CommentForm from '../../components/shareDetail/CommentForm.vue';
import CommentList from '../../components/shareDetail/CommentList.vue';
export default {
  components: { CommentForm, CommentList },
  created() {
    window.scrollTo(0, 0);
  },
};
</script>

<style>
CommentForm .text-main {
}
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
</style>
