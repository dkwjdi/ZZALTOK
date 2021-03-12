<template>
  <v-app-bar app color="white" flat id="navbar" height="80vh">
    <img
      :src="require('../../assets/logo2.png')"
      @click="MovePage('home')"
      style="height: 80px"
    />

    <ul class="nav_mian hidden-sm-and-down">
      <li class="nav_title">Menu1</li>
      <li class="nav_title">Menu2</li>
      <li class="nav_title">Menu3</li>
      <li class="nav_title">Menu4</li>
    </ul>

    <v-spacer></v-spacer>

    <v-app-bar-nav-icon class="hidden-md-and-up" @click="OnOffMenu"></v-app-bar-nav-icon>
  </v-app-bar>
</template>

<script>
export default {
  data() {
    return {drawer: null};
  },
  created() {},
  methods: {
    MovePage: function (check) {
      switch (check) {
        case "opinion":
          this.$router.push({ name: "Opinion" });
          break;
        case "home":
          this.$router.push({ name: "Main" });
          break;
        case "club":
          this.$router.push({ name: "Club" });
          break;
        case "issue":
          this.$router.push({ name: "Issue" });
          break;
        case "data":
          this.$router.push({ name: "Magazine" });
          break;
        case "join":
          this.$router.push({ name: "Join" });
          break;
        case "myPage":
          this.$router.push({ name: "MyPage" });
          break;
      }
    },
    OnOffMenu(){
        this.$store.commit("SET_ON_OFF_MENU", true);
    }
  },
};
</script>

<style lang="scss">
#navbar {
  outline: 1px solid rgb(225, 225, 225);
}

ul li {
  list-style-type: none;
  float: left;
  margin: 20px;
}
</style>