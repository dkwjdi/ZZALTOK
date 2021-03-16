<template>
  <v-row class="mt-1">
    <v-col cols="1" md="1"></v-col>
    <v-col cols="12" md="10">
        <comment-list-item v-for="k in 4" :key=k />
    </v-col>
    <v-col cols="1" md="1"></v-col>
  </v-row>
</template>

<script>
import CommentListItem from './CommentListItem.vue'
export default {
  components: { CommentListItem },
}
</script>