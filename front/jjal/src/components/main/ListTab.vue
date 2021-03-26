<template>
  <v-tabs>
    <v-tab style="color: #337ab7" @click="changeTeb('good')">
      <i class="fas fa-thumbs-up mr-2"></i>추천순</v-tab
    >
    <v-tab style="color: #337ab7" @click="changeTeb('view')">
      <i class="fas fa-eye mr-2"></i>조회순</v-tab
    >
    <v-tab style="color: #337ab7" @click="changeTeb('new')">
      <i class="fas fa-upload mr-2"></i>최신순</v-tab
    >
  </v-tabs>
</template>

<script>
import { mapActions } from "vuex";

export default {
  data: () => ({}),
  methods: {
    ...mapActions("mainStore", ["fetchShareListGood", "fetchShareListView"]),
    changeTeb(str) {
      this.$store.commit("mainStore/SET_PAGE_COUNT", "first");
      this.$store.commit("mainStore/SET_CURRENT_TAB", str);
      this.$store.commit("mainStore/SET_SHARE_ITEMS_RESET");

      switch (str) {
        case "good":
          this.fetchShareListGood();
          break;
        case "view":
          this.fetchShareListView();
          break;
      }
    },
  },
};
</script>
