<template>
  <div class="auth-shell glass-card">
    <section class="auth-panel">
      <div class="section-head">
        <div>
          <h2 class="section-title">创建账号</h2>
          <p class="section-copy">注册后就能上传简历、解析岗位并生成分析报告。</p>
        </div>
      </div>

      <el-form ref="formRef" :model="form" :rules="rules" label-position="top" @submit.prevent="handleRegister">
        <el-form-item label="昵称" prop="nickname">
          <el-input v-model="form.nickname" placeholder="怎么称呼你" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" placeholder="you@example.com" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" show-password placeholder="至少 8 位密码" />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input v-model="form.confirmPassword" show-password placeholder="再次输入密码" />
        </el-form-item>
        <el-button type="primary" :loading="submitting" class="submit-button" @click="handleRegister">
          注册并进入工作台
        </el-button>
      </el-form>

      <p class="auth-footer">
        已经有账号？
        <RouterLink to="/login">去登录</RouterLink>
      </p>
    </section>

    <section class="auth-hero">
      <p class="hero-kicker">One Flow</p>
      <h1>从注册开始，把简历优化流程装进同一个工作台。</h1>
      <p>
        你不需要再在文档、模型和表格之间来回切。这里会把简历、JD、分析结果和修改建议串成一条路径。
      </p>
    </section>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { ElMessage, type FormInstance, type FormRules } from "element-plus";

import { register } from "@/api/auth";
import { useAuthStore } from "@/stores/auth";
import { useUserStore } from "@/stores/user";

const router = useRouter();
const authStore = useAuthStore();
const userStore = useUserStore();

const formRef = ref<FormInstance>();
const submitting = ref(false);
const form = reactive({
  nickname: "",
  email: "",
  password: "",
  confirmPassword: "",
});

const rules: FormRules = {
  nickname: [{ required: true, message: "请输入昵称", trigger: "blur" }],
  email: [
    { required: true, message: "请输入邮箱", trigger: "blur" },
    { type: "email", message: "邮箱格式不正确", trigger: "blur" },
  ],
  password: [
    { required: true, message: "请输入密码", trigger: "blur" },
    { min: 8, message: "密码至少 8 位", trigger: "blur" },
  ],
  confirmPassword: [
    { required: true, message: "请再次输入密码", trigger: "blur" },
    {
      validator: (_rule, value, callback) => {
        if (value !== form.password) {
          callback(new Error("两次输入的密码不一致"));
          return;
        }
        callback();
      },
      trigger: "blur",
    },
  ],
};

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
    ElMessage.success("注册成功");
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
