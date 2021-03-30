<template>
  <div class="v-btn--example" style="float: left">
    <a href="javascript:;" class="kakao-link"> 호우! </a>
    <div class="mt-3">
      <v-btn color="indigo" dark fab @click="pwdDialog('update')">
        <v-icon>mdi-pencil</v-icon>
      </v-btn>
    </div>
    <div class="mt-3">
      <v-btn color="error" fab dark @click="pwdDialog('delete')">
        <v-icon>mdi-delete</v-icon>
      </v-btn>
    </div>
    <div class="mt-3">
      <v-btn color="green" fab dark>
        <a style="color: white" id="downloadDetail" download="my-photo.jpg" class="button" role="button" @click="down"
          ><v-icon>mdi-download</v-icon>
        </a>
      </v-btn>
    </div>
    <div class="mt-3">
      <v-btn color="warning" fab dark @click="kakaoShare">
        <v-icon>mdi-share-variant</v-icon>
      </v-btn>
    </div>
  </div>
</template>

<script>
import http from '@/util/http-common.js';
import { mapActions, mapGetters } from 'vuex';
import Swal from 'sweetalert2';

export default {
  props: {
    board_no: { Type: Number },
    title: { Type: String },
    content: { Type: String },
    url: { Type: String },
    content_type: { Type: String },
    nickname: { Type: String },
  },
  computed: {
    ...mapGetters('mainStore', ['getShareDetail']),
  },
  data() {
    return {
      pwd: '',
      feedSettings: {
        objectType: 'feed',
        content: {
          title: '청하, CHUNG HA ｜ チョンハ',
          description:
            '청하는 대한민국의 가수이다. 2016년 엠넷에서 주관한 서바이벌 프로그램 《프로듀스 101》에 김청하라는 예명으로 출연해 최종순위 11명 중 4위로 프로젝트 걸그룹 아이오아이의 멤버로 데뷔 했으며, 활동을 마친 후 2017년 6월에 솔로로 데뷔했다.',
          imageUrl:
            'https://w.namu.la/s/5a218e413a95f08b57a7b18998c294f9a8c18f2447e7e5ec6d369557b876646c8bf998ec5fd20db50eec75cfa5aeb7defb174242ace627c8d73bd90c86f934a98adb426c8a2f3cb512c7a66b69637bf92ce125f3becd127e0ae6aa7429ab11a2c5e5a9af2dd1895ac4aaebd346c8581d',
          link: {
            mobileWebUrl: 'http://webruden.tistory.com',
          },
        },
        social: {
          likeCount: 1234,
          commentCount: 431,
          sharedCount: 8493,
          viewCount: 47298,
          subscriberCount: 3489,
        },
        buttons: [
          {
            title: '웹으로 이동',
            link: {
              webUrl: 'http://webruden.tistory.com',
            },
          },
          {
            title: '앱으로 이동',
            link: {
              mobileWebUrl: 'https://developers.kakao.com',
            },
          },
        ],
      },
    };
  },

  methods: {
    ...mapActions('mainStore', ['updateShareDetail', 'deleteShareDetail']),
    pwdDialog(str) {
      Swal.fire({
        title: '비밀번호를 입력해주세요',
        input: 'password',
        width: 500,
        inputAttributes: {
          autocapitalize: 'off',
        },
        showCancelButton: true,
        confirmButtonText: 'Ok',
        showLoaderOnConfirm: true,
        allowOutsideClick: () => !Swal.isLoading(),
      }).then((result) => {
        console.log(result);
        if (result.isConfirmed) {
          this.pwd = result.value;
          this.findshareDetailPwd(str);
        }
      });
    },

    kakaoShare() {
      Kakao.Link.sendDefault(this.feedSettings);
    },

    findshareDetailPwd(str) {
      http
        .post(`/v1/board/check/${this.board_no}`, { password: this.pwd })
        .then((res) => {
          console.log('게시판 비빌번호 성공 : ' + res.data.result);

          if (!res.data.result) {
            Swal.fire({
              icon: 'error',
              title: '비밀번호가 틀립니다.',
            });
            return;
          }

          // 게시판 수정
          if (str == 'update') {
            Swal.fire({
              showCancelButton: true,
              html:
                `제목<input id="swal-input1" class="swal2-input" value="${this.title}">` +
                `내용<textarea id="swal-input2" class="swal2-input" style="height:150px">${this.content}</textarea>`,
              focusConfirm: false,
              preConfirm: () => {
                return [document.getElementById('swal-input1').value, document.getElementById('swal-input2').value];
              },
            }).then((result) => {
              console.log(result);
              if (result.isConfirmed) {
                let data = {};
                let temp = this.url.substr(this.url.indexOf('/api'));
                console.log(temp);
                data.board_no = this.board_no;
                data.title = result.value[0];
                data.content = `{"url":"${temp}", "content":"${result.value[1]}"}`;
                data.content_type = this.content_type;
                data.nickname = this.nickname;
                data.password = this.pwd;
                this.updateShareDetail(data);
              }
            });
          } else {
            this.deleteShareDetail({ no: this.board_no, password: this.pwd });
            this.$router.push({ name: 'Main' });
          }
        })
        .catch((error) => {
          console.log('에러', error);
          console.log('에러내용', error.response);
        });
    },
    down() {
      const download = document.getElementById('downloadDetail');

      if (this.contentType == 'image') {
        //이미지 일때
        download.setAttribute('download', 'my-photo.jpg');
      } else if (this.contentType == 'video') {
        //비디오 일 때
        download.setAttribute('download', 'my-video.mp4');
      }

      console.log(download);
      download.setAttribute('href', this.url); //파일생성
    },
  },

  mounted() {
    Kakao.Link.createDefaultButton(Object.assign({}, this.feedSettings, { container: '.kakao-link' }));
  },
};
</script>
