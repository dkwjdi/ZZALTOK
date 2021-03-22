<template>
    <div>
    <comment-form :type="'create'" :no="getShareDetail.board_no" />

    <v-divider></v-divider>

    <v-row class="mt-1">
      <v-col cols="1" md="1"></v-col>
      <v-col cols="12" md="10">
        <comment-list-item
          v-for="item in getCommentItems"
          :key="item.comment_no"
          :comment_no="item.comment_no"
          :content="item.content"
          :ip="item.ip"
          :nickname="item.nickname"
          :regdate="item.regdate"
        />
      </v-col>
      <v-col cols="1" md="1"></v-col>
    </v-row>
  </div>
</template>

<script>
import CommentForm from './CommentForm.vue';
import CommentListItem from './CommentListItem.vue'
import { mapGetters } from "vuex";

export default {
  components: { CommentListItem, CommentForm },
    computed:{
    ...mapGetters("mainStore", ["getCommentItems","getShareDetail"]),
  },
}
</script>