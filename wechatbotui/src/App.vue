<template>
  <div>
    <div class="headerWrapper">
      <header>
        <el-menu default-active="1" mode="horizontal" @select="handleSelect">
          <el-menu-item index="1">Home</el-menu-item>
          <el-menu-item index="3">Orders</el-menu-item>
        </el-menu>
      </header>
    </div>
    <div class="main-cnt">
      <div class="page-container page-component">
        <div class="el-row">
          <router-view></router-view>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    methods: {
      handleSelect(key, keyPath) {
        console.log(key, keyPath);
      }
    }
  }
</script>

<style>
  .el-menu {
    float: right;
  }

  body {
    margin: 0;
  }
</style>
