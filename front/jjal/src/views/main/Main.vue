<template>
  <v-container>
    <v-row>
      <v-col :key="n" class="mt-2" cols="10">
        <strong class="ml-6">Category {{ n }}</strong>
      </v-col>

      <template>
        <v-col v-for="j in 4" :key="`${n}${j}`" cols="12" sm="3">
          <template>
            <v-row>
              <v-col cols="1"></v-col>
              <v-col cols="10">
                <v-sheet height="180" class="grey lighten-2"></v-sheet>
              </v-col>
              <v-col cols="1"></v-col>
            </v-row>
          </template>
        </v-col>
      </template>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data: () => ({ drawer: null }),
};
</script>
