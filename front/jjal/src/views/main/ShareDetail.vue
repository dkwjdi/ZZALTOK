<template>
  <v-container>
    <v-row class="mt-7">
      <v-col cols="1"></v-col>
      <v-col cols="10">
        <v-img
          :src="require('../../assets/example.png')"
          aspect-ratio="1.5"
          @click="moveDetail()"
          class="detail-img"
          max-width="1000px"
          max-height="600px"
        >
        </v-img>

        <div class="text-center text-main">
          <div class="mt-5 detail-text">
            <div class="text-h5">제목</div>
            <div class="mt-2 body-2">조회수 10회 | 2021.03.16</div>
            <div class="mt-2 body-2">by 익명</div>
          </div>

          <div class="mt-5 detail-text">내용</div>

          <div>댓글</div>
        </div>
      </v-col>
      <v-col cols="1"></v-col>
    </v-row>
  </v-container>
</template>

<style>
.text-main {
}
.detail-text {
  padding-bottom: 10px;
  border-bottom: 1px solid rgb(225, 225, 225);
}

.detail-img {
  display: block;
  margin: auto;
  border-radius: 5px;
}
</style>
