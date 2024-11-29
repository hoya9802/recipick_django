<template>
    <div>
        <button @click="deleteAccount" class="btn btn-danger">
            회원 탈퇴
        </button>
    </div>
</template>

<script>
export default{
    name: 'Update',
    data() {

    },
    mounted() {
        document.title = '회원정보수정 - Recipick'
    },
    methods: {
        async deleteAccount() {
            if (confirm("정말로 회원 탈퇴를 진행하시겠습니까?")) {
                try {
                    await apiClient.delete("/user/mypage/me/");
                    alert("회원 탈퇴가 완료되었습니다. 회원가입 페이지로 이동합니다.");
                    this.$router.push("/signup"); // 탈퇴 후 회원가입 페이지로 이동
                } catch (err) {
                    console.error("회원 탈퇴 중 문제가 발생했습니다.", err);
                }
            }
        },
    },

}
</script>

<style scoped>

</style>