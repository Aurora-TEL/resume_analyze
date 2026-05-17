<template>
  <main class="blank-layout">
    <router-view />
  </main>
</template>

<style scoped lang="scss">
.blank-layout {
  min-height: 100vh;
  padding: 32px 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
