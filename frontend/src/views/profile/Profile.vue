<template>
  <div class="app-page" v-loading="loading">
    <section class="hero-card">
      <p class="hero-kicker">Profile Settings</p>
      <h1 class="hero-title">维护你的目标岗位信息，让后续解析更贴近投递方向。</h1>
      <p class="hero-copy">
        这里保存的是用户维度的长期信息，比如昵称、目标岗位和目标城市。修改后会影响后续部分解析提示。
      </p>
    </section>

    <div class="two-column">
      <section class="section-card">
        <div class="section-head">
          <div>
            <h2 class="section-title">个人资料</h2>
            <p class="section-copy">这些字段会在用户主链路中长期复用。</p>
          </div>
        </div>

        <el-form ref="profileFormRef" :model="profileForm" label-position="top">
          <el-form-item label="邮箱">
            <el-input :model-value="userStore.currentUser?.email || ''" disabled />
          </el-form-item>
          <el-form-item label="昵称">
            <el-input v-model="profileForm.nickname" maxlength="100" />
          </el-form-item>
          <el-form-item label="手机号">
            <el-input v-model="profileForm.phone" maxlength="50" />
          </el-form-item>
          <el-form-item label="目标岗位">
            <el-input v-model="profileForm.target_position" maxlength="100" />
          </el-form-item>
          <el-form-item label="目标城市">
            <el-input v-model="profileForm.target_city" maxlength="100" />
          </el-form-item>
          <el-form-item label="工作年限">
            <el-input-number v-model="profileForm.work_years" :min="0" :max="50" :precision="1" :step="0.5" />
          </el-form-item>
          <el-button type="primary" :loading="savingProfile" @click="handleSaveProfile">保存资料</el-button>
        </el-form>
      </section>

      <section class="section-card">
        <div class="section-head">
          <div>
            <h2 class="section-title">修改密码</h2>
            <p class="section-copy">建议定期更新密码，保持本地调试账号整洁可控。</p>
          </div>
        </div>

        <el-form ref="passwordFormRef" :model="passwordForm" :rules="passwordRules" label-position="top">
          <el-form-item label="旧密码" prop="old_password">
            <el-input v-model="passwordForm.old_password" show-password />
          </el-form-item>
          <el-form-item label="新密码" prop="new_password">
            <el-input v-model="passwordForm.new_password" show-password />
          </el-form-item>
          <el-form-item label="确认新密码" prop="confirm_password">
            <el-input v-model="passwordForm.confirm_password" show-password />
          </el-form-item>
          <el-button type="primary" plain :loading="savingPassword" @click="handleSavePassword">更新密码</el-button>
        </el-form>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from "vue";
import { ElMessage, type FormInstance, type FormRules } from "element-plus";

import { updateCurrentUser, updatePassword } from "@/api/users";
import { useUserStore } from "@/stores/user";

const userStore = useUserStore();
const loading = ref(false);
const savingProfile = ref(false);
const savingPassword = ref(false);
const profileFormRef = ref<FormInstance>();
const passwordFormRef = ref<FormInstance>();

const profileForm = reactive({
  nickname: "",
  phone: "",
  target_position: "",
  target_city: "",
  work_years: 0,
});

const passwordForm = reactive({
  old_password: "",
  new_password: "",
  confirm_password: "",
});

const passwordRules: FormRules = {
  old_password: [{ required: true, message: "请输入旧密码", trigger: "blur" }],
  new_password: [
    { required: true, message: "请输入新密码", trigger: "blur" },
    { min: 8, message: "新密码至少 8 位", trigger: "blur" },
  ],
  confirm_password: [
    { required: true, message: "请再次输入新密码", trigger: "blur" },
    {
      validator: (_rule, value, callback) => {
        if (value !== passwordForm.new_password) {
          callback(new Error("两次输入的新密码不一致"));
          return;
        }
        callback();
      },
      trigger: "blur",
    },
  ],
};

function syncProfileForm() {
  profileForm.nickname = userStore.currentUser?.nickname || "";
  profileForm.phone = userStore.currentUser?.phone || "";
  profileForm.target_position = userStore.currentUser?.target_position || "";
  profileForm.target_city = userStore.currentUser?.target_city || "";
  profileForm.work_years = Number(userStore.currentUser?.work_years || 0);
}

async function loadProfile() {
  loading.value = true;
  try {
    await userStore.fetchCurrentUser(true);
    syncProfileForm();
  } finally {
    loading.value = false;
  }
}

async function handleSaveProfile() {
  savingProfile.value = true;
  try {
    const result = await updateCurrentUser({
      nickname: profileForm.nickname || null,
      phone: profileForm.phone || null,
      target_position: profileForm.target_position || null,
      target_city: profileForm.target_city || null,
      work_years: profileForm.work_years,
    });
    userStore.setCurrentUser(result);
    syncProfileForm();
    ElMessage.success("资料已更新");
  } finally {
    savingProfile.value = false;
  }
}

async function handleSavePassword() {
  const valid = await passwordFormRef.value?.validate().catch(() => false);
  if (!valid) {
    return;
  }

  savingPassword.value = true;
  try {
    await updatePassword({
      old_password: passwordForm.old_password,
      new_password: passwordForm.new_password,
    });
    passwordForm.old_password = "";
    passwordForm.new_password = "";
    passwordForm.confirm_password = "";
    ElMessage.success("密码已更新");
  } finally {
    savingPassword.value = false;
  }
}

onMounted(loadProfile);
</script>
