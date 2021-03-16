<template>
      <v-row class="mt-2 pt-4">
        <v-col cols="1" md="1"></v-col>
        <v-col cols="12" md="3">
          <v-textarea
            outlined
            label="NickName"
            value=""
            height="10px"
            class=""
            no-resize
          ></v-textarea>

          <v-textarea
            outlined
            label="PassWord"
            height="10px"
            value=""
            no-resize
          ></v-textarea>
        </v-col>

        <v-col cols="12" md="7">
          <v-textarea
            outlined
            label="content"
            auto-grow
            height="141px"
            value="The Woodman set to work at once, and so sharp was his axe that the tree was soon chopped nearly through."
          ></v-textarea>

          <v-btn class="mb-5" style="float:right">등록</v-btn>
        </v-col>
        <v-col cols="1" md="1"></v-col>
      </v-row>
</template>