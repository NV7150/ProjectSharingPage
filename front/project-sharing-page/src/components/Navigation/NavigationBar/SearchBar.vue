<template>
  <v-text-field
      label="検索"
      v-model="keyword"
      @keydown.enter="search"
  />
</template>

<script>
export default {
  name: "SearchBar",
  data(){
    return {
      keyword : ""
    }
  },
  methods: {
    search(){
      if(!this.keyword)
        return;

      this.$router.push({name: "Search", query: {
        keyword: this.keyword
      }});
    }
  }
}
</script>

<style scoped>

</style>