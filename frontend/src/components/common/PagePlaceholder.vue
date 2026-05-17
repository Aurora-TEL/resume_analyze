<template>
  <section class="page-placeholder">
    <div class="hero">
      <p class="eyebrow">Preparation Ready</p>
      <h1>{{ title }}</h1>
      <p>{{ description }}</p>
    </div>

    <div class="panel">
      <slot>
        <p>页面骨架已经就位，下一步可以继续接业务组件、真实接口和交互细节。</p>
      </slot>
    </div>
  </section>
</template>

<script setup lang="ts">
defineProps<{
  title: string;
  description: string;
}>();
</script>

<style scoped lang="scss">
.page-placeholder {
  display: grid;
  gap: 20px;
}

.hero,
.panel {
  padding: 28px;
  border: 1px solid var(--panel-border);
  border-radius: var(--radius-lg);
  background: var(--panel-bg);
  box-shadow: var(--shadow-soft);
  backdrop-filter: blur(10px);
}

.eyebrow {
  margin: 0 0 8px;
  color: var(--brand-primary);
  font-size: 12px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

h1 {
  margin: 0 0 12px;
  font-size: 32px;
}

p {
  margin: 0;
  line-height: 1.7;
  color: var(--text-secondary);
}
</style>
