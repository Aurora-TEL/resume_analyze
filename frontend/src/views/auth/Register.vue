<template>
  <div class="auth-shell glass-card">
    <section class="auth-panel">
      <div class="section-head">
        <div>
          <h2 class="section-title">{{ t.auth.register.panelTitle }}</h2>
          <p class="section-copy">{{ t.auth.register.panelCopy }}</p>
        </div>
      </div>

      <el-form ref="formRef" :model="form" :rules="rules" label-position="top" @submit.prevent="handleRegister">
        <el-form-item :label="t.auth.register.nickname" prop="nickname">
          <el-input v-model="form.nickname" :placeholder="t.auth.register.nicknamePlaceholder" />
        </el-form-item>
        <el-form-item :label="t.auth.register.email" prop="email">
          <el-input v-model="form.email" placeholder="you@example.com" />
        </el-form-item>
        <el-form-item :label="t.auth.register.password" prop="password">
          <el-input v-model="form.password" show-password :placeholder="t.auth.register.passwordPlaceholder" />
        </el-form-item>
        <el-form-item :label="t.auth.register.confirmPassword" prop="confirmPassword">
          <el-input
            v-model="form.confirmPassword"
            show-password
            :placeholder="t.auth.register.confirmPasswordPlaceholder"
          />
        </el-form-item>
        <el-button type="primary" :loading="submitting" class="submit-button" @click="handleRegister">
          {{ t.auth.register.submit }}
        </el-button>
      </el-form>

      <p class="auth-footer">
        {{ t.auth.register.hasAccount }}
        <RouterLink to="/login">{{ t.auth.register.toLogin }}</RouterLink>
      </p>
    </section>

    <section class="auth-hero">
      <p class="hero-kicker">One Flow</p>
      <h1>{{ t.auth.register.heroTitle }}</h1>
      <p>{{ t.auth.register.heroCopy }}</p>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { ElMessage, type FormInstance, type FormRules } from "element-plus";

import { register } from "@/api/auth";
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
  nickname: "",
  email: "",
  password: "",
  confirmPassword: "",
});

const rules = computed<FormRules>(() => ({
  nickname: [{ required: true, message: t.value.auth.register.validationNicknameRequired, trigger: "blur" }],
  email: [
    { required: true, message: t.value.auth.register.validationEmailRequired, trigger: "blur" },
    { type: "email", message: t.value.auth.register.validationEmailInvalid, trigger: "blur" },
  ],
  password: [
    { required: true, message: t.value.auth.register.validationPasswordRequired, trigger: "blur" },
    { min: 8, message: t.value.auth.register.validationPasswordMin, trigger: "blur" },
  ],
  confirmPassword: [
    { required: true, message: t.value.auth.register.validationConfirmRequired, trigger: "blur" },
    {
      validator: (_rule, value, callback) => {
        if (value !== form.password) {
          callback(new Error(t.value.auth.register.validationConfirmMismatch));
          return;
        }
        callback();
      },
      trigger: "blur",
    },
  ],
}));

async function handleRegister() {
  const valid = await formRef.value?.validate().catch(() => false);
  if (!valid) {
    return;
  }

  submitting.value = true;
  try {
    const result = await register({
      email: form.email,
      password: form.password,
      nickname: form.nickname,
    });
    authStore.setToken(result.access_token);
    await userStore.fetchCurrentUser(true);
    ElMessage.success(t.value.auth.register.success);
    router.push("/dashboard");
  } finally {
    submitting.value = false;
  }
}
</script>

<style scoped lang="scss">
.auth-shell {
  width: min(1080px, 100%);
  display: grid;
  grid-template-columns: minmax(380px, 0.95fr) minmax(0, 1.05fr);
  overflow: hidden;
}

.auth-panel,
.auth-hero {
  padding: 42px;
}

.auth-panel {
  background: rgba(255, 255, 255, 0.95);
}

.auth-hero {
  background:
    radial-gradient(circle at top right, rgba(217, 140, 43, 0.22), transparent 32%),
    linear-gradient(180deg, #f6efe4 0%, #e4f0ec 100%);
}

.auth-hero h1 {
  margin: 18px 0 16px;
  font-size: 42px;
  line-height: 1.08;
  color: var(--brand-deep);
}

.auth-hero p {
  margin: 0;
  line-height: 1.8;
  color: var(--text-secondary);
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

  .auth-panel,
  .auth-hero {
    padding: 32px 24px;
  }

  .auth-hero h1 {
    font-size: 34px;
  }
}
</style>
