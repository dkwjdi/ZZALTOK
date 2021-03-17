<template>
  <v-row class="mt-2 pt-4">
    <v-col cols="1" md="1"></v-col>
    <v-col cols="12" md="3">
      <v-text-field
        outlined
        label="NickName"
        height="10px"
        class=""
        ref="nickName"
        v-model="nickName"
      ></v-text-field>

      <v-text-field
        outlined
        type="password"
        label="PassWord"
        height="10px"
        password
        ref="password"
        v-model="password"
      ></v-text-field>
    </v-col>

    <v-col cols="12" md="7">
      <v-textarea
        outlined
        label="내용을 입력하세요"
        auto-grow
        height="141px"
        ref="content"
        v-model="content"
      ></v-textarea>

      <div class="mb-5" style="float: right">
        <v-btn @click="checkHandler()">등록</v-btn>
        <v-btn class="ml-2" v-if="type == 'update'" @click="change"> 취소</v-btn>
      </div>
    </v-col>
    <v-col cols="1" md="1"></v-col>
  </v-row>
</template>

<script>
export default {
  props: {
    type: { Type: String },
    propContent: { Type: String },
    no: { Type: Number },
  },
  data() {
    return {
      nickName: '',
      password: '',
    };
  },
  methods: {
    checkHandler() {
      let err = true;
      let msg = '';

      !this.nickName &&
        ((msg = '작성자를 입력해주세요'), (err = false), this.$refs.nickName.focus());
      err &&
        !this.password &&
        ((msg = '비밀번호를 입력해주세요'), (err = false), this.$refs.password.focus());
      err &&
        !this.content &&
        ((msg = '내용을 입력해주세요'), (err = false), this.$refs.content.focus());

      if (!err) alert(msg);
      else this.type == 'create' ? this.createHandler() : this.updateHandler();
    },

    createHandler() {},

    updateHandler() {},

    change() {
      this.$emit('CommentDown');
    },

    created() {
      //update일때 값 담아주기
    },
  },
};
</script>
