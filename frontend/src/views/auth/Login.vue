<template>
  <div class="auth-shell glass-card">
    <section class="auth-hero">
      <p class="hero-kicker">DeepSeek Connected</p>
      <h1>{{ t.auth.login.heroTitle }}</h1>
      <p>{{ t.auth.login.heroCopy }}</p>
      <ul class="hero-points">
        <li>{{ t.auth.login.pointResume }}</li>
        <li>{{ t.auth.login.pointStructure }}</li>
        <li>{{ t.auth.login.pointReport }}</li>
      </ul>
    </section>

    <section class="auth-panel">
      <div class="section-head">
        <div>
          <h2 class="section-title">{{ t.auth.login.panelTitle }}</h2>
          <p class="section-copy">{{ t.auth.login.panelCopy }}</p>
        </div>
      </div>

      <el-form ref="formRef" :model="form" :rules="rules" label-position="top" @submit.prevent="handleLogin">
        <el-form-item :label="t.auth.login.email" prop="email">
          <el-input v-model="form.email" placeholder="you@example.com" />
        </el-form-item>
        <el-form-item :label="t.auth.login.password" prop="password">
          <el-input v-model="form.password" show-password :placeholder="t.auth.login.passwordPlaceholder" />
        </el-form-item>
        <el-button type="primary" :loading="submitting" class="submit-button" @click="handleLogin">
          {{ t.auth.login.submit }}
        </el-button>
      </el-form>

      <p class="auth-footer">
        {{ t.auth.login.noAccount }}
        <RouterLink to="/register">{{ t.auth.login.registerNow }}</RouterLink>
      </p>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { ElMessage, type FormInstance, type FormRules } from "element-plus";

import { login } from "@/api/auth";
import { useAuthStore } from "@/stores/auth";
import { useUserStore } from "@/stores/user";
import { useUserMessages } from "@/utils/userI18n";

const router = useRouter();
const authStore = useAuthStore();
const userStore = useUserStore();
const messages = useUserMessages();

const t = computed(() => messages.value);
const formRef = ref<FormInstance>();
const submitting = ref(false);
const form = reactive({
  email: "",
  password: "",
});

const rules = computed<FormRules>(() => ({
  email: [
    { required: true, message: t.value.auth.login.validationEmailRequired, trigger: "blur" },
    { type: "email", message: t.value.auth.login.validationEmailInvalid, trigger: "blur" },
  ],
  password: [{ required: true, message: t.value.auth.login.validationPasswordRequired, trigger: "blur" }],
}));

async function handleLogin() {
  const valid = await formRef.value?.validate().catch(() => false);
  if (!valid) {
    return;
  }

  submitting.value = true;
  try {
    const result = await login(form);
    authStore.setToken(result.access_token);
    userStore.setCurrentUser({
      id: result.user.id,
      email: result.user.email,
      nickname: result.user.nickname,
      phone: null,
      avatar_url: null,
      target_position: null,
      target_city: null,
      work_years: null,
      role: result.user.role,
      status: result.user.status,
    });
    await userStore.fetchCurrentUser(true);
    ElMessage.success(t.value.auth.login.success);
    router.push(result.user.role === "admin" ? "/admin" : "/dashboard");
  } finally {
    submitting.value = false;
  }
}
</script>

<style scoped lang="scss">
.auth-shell {
  width: min(1080px, 100%);
  display: grid;
  grid-template-columns: minmax(0, 1.05fr) minmax(360px, 0.95fr);
  overflow: hidden;
}

.auth-hero {
  padding: 48px;
  background:
    radial-gradient(circle at top left, rgba(217, 140, 43, 0.28), transparent 35%),
    linear-gradient(180deg, #183a34 0%, #255247 100%);
  color: #f5f8f4;
}

.auth-hero h1 {
  margin: 18px 0 16px;
  font-size: 44px;
  line-height: 1.08;
}

.auth-hero p {
  margin: 0;
  line-height: 1.8;
  color: rgba(245, 248, 244, 0.8);
}

.hero-points {
  margin: 26px 0 0;
  padding-left: 18px;
  display: grid;
  gap: 10px;
}

.auth-panel {
  padding: 42px;
  background: rgba(255, 255, 255, 0.94);
}

.submit-button {
  width: 100%;
  margin-top: 12px;
}

.auth-footer {
  margin: 18px 0 0;
  color: var(--text-secondary);
}

.auth-footer a {
  color: var(--brand-primary);
  font-weight: 700;
}

@media (max-width: 920px) {
  .auth-shell {
    grid-template-columns: 1fr;
  }

  .auth-hero,
  .auth-panel {
    padding: 32px 24px;
  }

  .auth-hero h1 {
    font-size: 34px;
  }
}
</style>
