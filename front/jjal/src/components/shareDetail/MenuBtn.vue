<template>
  <div class="v-btn--example" style="float: left">
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
        <v-icon>mdi-download</v-icon>
      </v-btn>
    </div>
    <div class="mt-3">
      <v-btn color="warning" fab dark>
        <v-icon>mdi-share-variant</v-icon>
      </v-btn>
    </div>
  </div>
</template>

<script>
import http from "@/util/http-common.js";
import { mapActions, mapGetters } from "vuex";
import Swal from "sweetalert2";

export default {
  props: {
    board_no: { Type: Number },
    title: { Type: String },
    content: { Type: String },
    url:{ Type: String},
    content_type: { Type: String },
    nickname: { Type: String },
  },
  computed: {
    ...mapGetters("mainStore", ["getShareDetail"]),
  },
  data() {
    return {
      pwd: "",
    };
  },

  methods: {
    ...mapActions("mainStore", ["updateShareDetail", "deleteShareDetail"]),
    pwdDialog(str) {
      Swal.fire({
        title: "비밀번호를 입력해주세요",
        input: "password",
        width: 500,
        inputAttributes: {
          autocapitalize: "off",
        },
        showCancelButton: true,
        confirmButtonText: "Ok",
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

    findshareDetailPwd(str) {
      http
        .post(`/v1/board/check/${this.board_no}`, { password: this.pwd })
        .then((res) => {
          console.log("게시판 비빌번호 성공 : " + res.data.result);

          if (!res.data.result) {
            Swal.fire({
              icon: "error",
              title: "비밀번호가 틀립니다.",
            });
            return;
          }

          // 게시판 수정
          if (str == "update") {
            Swal.fire({
              showCancelButton: true,
              html:
                `제목<input id="swal-input1" class="swal2-input" value="${this.title}">` +
                `내용<textarea id="swal-input2" class="swal2-input" style="height:150px">${this.content}</textarea>`,
              focusConfirm: false,
              preConfirm: () => {
                  return [
                  document.getElementById("swal-input1").value,
                  document.getElementById("swal-input2").value,
                ];
              },
            }).then((result) => {
              console.log(result);
              if (result.isConfirmed) {
                let data = {};
                data.board_no = this.board_no;
                data.title = result.value[0];
                data.content = `{"url":"${this.url}", "content":"${result.value[1]}"}`;
                data.content_type = this.content_type;
                data.nickname = this.nickname;
                data.password = this.pwd;
                this.updateShareDetail(data);
              }
            });
          } 
          
          else {
            this.deleteShareDetail({ no: this.board_no, password: this.pwd });
            this.$router.push({ name: "Main" });
          }
        })
        .catch((error) => {
          console.log("에러", error);
          console.log("에러내용", error.response);
        });
    },
  },
};
</script>