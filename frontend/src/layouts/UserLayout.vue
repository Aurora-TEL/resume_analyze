<template>
  <div class="shell">
    <aside class="sidebar">
      <div class="brand-block">
        <p class="brand-kicker">Resume Studio</p>
        <h1 class="brand-title">AI Resume Analyzer</h1>
        <p class="brand-copy">
          把简历、岗位和分析报告放进一条顺滑主链路里。
        </p>
      </div>

      <nav class="nav-list">
        <RouterLink
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          class="nav-link"
          active-class="is-active"
        >
          <span class="nav-label">{{ item.label }}</span>
          <span class="nav-hint">{{ item.hint }}</span>
        </RouterLink>
      </nav>

      <div class="sidebar-footer">
        <div class="user-card">
          <p class="user-name">{{ userStore.currentUser?.nickname || "未命名用户" }}</p>
          <p class="user-email">{{ userStore.currentUser?.email || "未登录" }}</p>
        </div>
        <el-button plain @click="handleLogout">退出登录</el-button>
      </div>
    </aside>

    <main class="main-panel">
      <header class="topbar">
        <div>
          <p class="topbar-kicker">Local + DeepSeek</p>
          <h2 class="topbar-title">{{ currentRouteMeta.title }}</h2>
        </div>
        <div class="topbar-actions">
          <el-button @click="router.push('/analysis/create')">新建分析</el-button>
          <el-button type="primary" @click="router.push('/resumes/upload')">上传简历</el-button>
        </div>
      </header>

      <section class="main-content">
        <router-view />
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useRouter, useRoute } from "vue-router";

import { logout as requestLogout } from "@/api/auth";
import { useAuthStore } from "@/stores/auth";
import { useUserStore } from "@/stores/user";

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();
const userStore = useUserStore();

const navItems = [
  { to: "/dashboard", label: "概览", hint: "总览当前进度" },
  { to: "/resumes", label: "简历", hint: "上传与解析" },
  { to: "/jobs", label: "岗位", hint: "整理 JD 需求" },
  { to: "/analysis/create", label: "分析", hint: "发起匹配分析" },
  { to: "/reports", label: "报告", hint: "查看结果沉淀" },
  { to: "/profile", label: "我的", hint: "维护个人信息" },
];

const currentRouteMeta = computed(() => {
  if (route.path === "/dashboard") {
    return { title: "工作台" };
  }
  if (route.path === "/resumes") {
    return { title: "简历中心" };
  }
  if (route.path === "/resumes/upload") {
    return { title: "上传简历" };
  }
  if (route.path.startsWith("/resumes/")) {
    return { title: "简历详情" };
  }
  if (route.path === "/jobs") {
    return { title: "岗位中心" };
  }
  if (route.path === "/jobs/create") {
    return { title: "创建岗位" };
  }
  if (route.path.startsWith("/jobs/")) {
    return { title: "岗位详情" };
  }
  if (route.path === "/analysis/create") {
    return { title: "发起分析" };
  }
  if (route.path.startsWith("/analysis/tasks/")) {
    return { title: "任务状态" };
  }
  if (route.path === "/reports") {
    return { title: "分析报告" };
  }
  if (route.path.startsWith("/reports/")) {
    return { title: "报告详情" };
  }
  if (route.path === "/profile") {
    return { title: "个人设置" };
  }
  return { title: "详情页" };
});

async function handleLogout() {
  try {
    await requestLogout();
  } catch {
    // Ignore logout API errors and clear local session anyway.
  }

  authStore.logout();
  userStore.clearCurrentUser();
  router.push("/login");
}
</script>

<style scoped lang="scss">
.shell {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 320px 1fr;
  background:
    radial-gradient(circle at top left, rgba(24, 111, 92, 0.26), transparent 30%),
    linear-gradient(180deg, #f5efe3 0%, #eef3f1 100%);
}

.sidebar {
  padding: 28px 22px;
  display: flex;
  flex-direction: column;
  gap: 28px;
  background: linear-gradient(180deg, #173732 0%, #214d45 100%);
  color: #f5f7f2;
}

.brand-block {
  display: grid;
  gap: 10px;
}

.brand-kicker,
.topbar-kicker {
  margin: 0;
  font-size: 12px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.65);
}

.brand-title,
.topbar-title {
  margin: 0;
  font-size: 30px;
  line-height: 1.1;
}

.brand-copy {
  margin: 0;
  color: rgba(245, 247, 242, 0.78);
  line-height: 1.7;
}

.nav-list {
  display: grid;
  gap: 12px;
}

.nav-link {
  padding: 14px 16px;
  display: grid;
  gap: 6px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid transparent;
  transition:
    transform 0.18s ease,
    border-color 0.18s ease,
    background 0.18s ease;
}

.nav-link:hover,
.nav-link.is-active {
  transform: translateY(-1px);
  border-color: rgba(255, 255, 255, 0.22);
  background: rgba(255, 255, 255, 0.14);
}

.nav-label {
  font-size: 16px;
  font-weight: 700;
}

.nav-hint {
  font-size: 13px;
  color: rgba(245, 247, 242, 0.72);
}

.sidebar-footer {
  margin-top: auto;
  display: grid;
  gap: 14px;
}

.user-card {
  padding: 16px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.08);
}

.user-name,
.user-email {
  margin: 0;
}

.user-name {
  font-size: 15px;
  font-weight: 700;
}

.user-email {
  margin-top: 6px;
  font-size: 13px;
  color: rgba(245, 247, 242, 0.72);
}

.main-panel {
  min-width: 0;
  padding: 24px;
}

.topbar {
  padding: 22px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  border: 1px solid rgba(49, 62, 82, 0.1);
  border-radius: 28px;
  background: rgba(255, 255, 255, 0.74);
  backdrop-filter: blur(16px);
  box-shadow: var(--shadow-soft);
}

.topbar-kicker {
  color: var(--brand-primary);
}

.topbar-title {
  font-size: 26px;
  color: var(--text-primary);
}

.topbar-actions {
  display: flex;
  gap: 12px;
}

.main-content {
  padding-top: 24px;
}

@media (max-width: 1080px) {
  .shell {
    grid-template-columns: 1fr;
  }

  .topbar {
    flex-direction: column;
    align-items: flex-start;
  }
}

@media (max-width: 640px) {
  .main-panel {
    padding: 16px;
  }

  .topbar-actions {
    width: 100%;
    display: grid;
    grid-template-columns: 1fr 1fr;
  }
}
</style>
