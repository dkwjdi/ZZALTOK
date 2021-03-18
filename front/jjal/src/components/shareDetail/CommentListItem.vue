<template>
  <div>
    <div
      v-if="!isCommentForm"
      class="mt-5 mb-5 pt-3 pl-2"
      @mouseover="isMenu = true"
      @mouseleave="isMenu = false"
      @click="isMenu = !isMenu"
    >
      <v-avatar color="indigo" size="53" style="float: left" class="mr-3">
        <v-icon dark> mdi-account-circle </v-icon>
      </v-avatar>
      <div style="padding-top: -10px">
        <div class="font-weight-bold subtitle-1">
          사용자<span style="color: #a9a9a9; font-size: 13px">(ip)</span> &middot;
          <span style="color: #a9a9a9; font-size: 13px">날짜</span>

          <div style="float: right" v-if="isMenu">
            <div v-if="!isUpdate">
              <!-- 수정 -->
              <v-btn icon x-small color="primary" fab dark @click="chageInput('수정')">
                <v-icon>mdi-pencil</v-icon>
              </v-btn>

              <!-- 삭제 -->
              <v-btn icon x-small color="primary" fab dark @click="chageInput('삭제')">
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </div>

            <div class="menu-input" v-if="isUpdate">
              <input type="text" placeholder="password" />
              <v-btn text dark @click="chackHandler()">{{ typeForm }}</v-btn>
              <v-btn icon color="white" @click="isUpdate = false"><v-icon>mdi-close</v-icon></v-btn>
            </div>
          </div>
        </div>
        <div class="subtitle-2">내용</div>
      </div>
    </div>

    <!-- 수정창 -->
    <div class="update-form" v-if="isCommentForm">
      <comment-form :type="'update'" v-on:CommentDown="checkMenu()" />
    </div>
  </div>
</template>

<script>
import CommentForm from './CommentForm.vue';
export default {
  components: { CommentForm },
  data() {
    return {
      menu1: false,
      menu2: false,

      isMenu: false,
      isCommentForm: false,
      isUpdate: false,
      typeForm: '',
    };
  },

  methods: {
    checkMenu() {
      this.isCommentForm = false;
      this.isUpdate = false;
    },
    chageInput(str) {
      this.isUpdate = true;
      this.typeForm = str;
    },
    chackHandler() {
      //타입에 맞게 update, delete
      if (this.typeForm == '수정') {
        this.isCommentForm = true;
      }
    },
    updateComment() {
      //패스워드 맞는지 검사하고
    },
    deleteComment() {},
  },
};
</script>

<style>
.comment-content {
  width: 90%;
}

.menu-input {
  border: 1px solid black;
  background-color: rgb(3, 3, 90);
  border-radius: 5px;
}

.menu-input input {
  background-color: white;
  border-radius: 5px;
  margin-left: 5px;
  padding-left: 5px;
  width: 150px;
}

.update-form {
  border: 1px solid black;
  border-radius: 5px;
}
</style>
