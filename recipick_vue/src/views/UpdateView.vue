<template>
    <div class="update">
        <div class="box">
            <label for="id">ID</label>
            <div class="black-bar"></div>
            <div class="input-group">
                <input type="text" id="id" v-model="user.id" disabled readonly />
            </div>
        </div>

        <div class="box">
            <label for="profile_image">Profile Image</label>
            <div class="black-bar"></div>
            <div class="input-group">
                <div v-if="previewImage" class="preview">
                    <img :src="previewImage" alt="프로필 이미지 미리보기" />
                </div>
                <input type="file" id="profile_image" @change="onFileChange" />
                <button @click.prevent="updateField('profile_image')">수정하기</button>
            </div>
            <div v-if="fieldMessages.profile_image" class="field-message">
                {{ fieldMessages.profile_image }}
            </div>
        </div>

        <div class="box">
            <label for="nick_name">Nickname</label>
            <div class="black-bar"></div>
            <div class="input-group">
                <input type="text" id="nick_name" v-model="user.nick_name" />
                <button @click.prevent="updateField('nick_name')">수정하기</button>
            </div>
            <div v-if="fieldMessages.nick_name" class="field-message">
                {{ fieldMessages.nick_name }}
            </div>
        </div>

        <div class="box">
            <label for="email">E-mail</label>
            <div class="black-bar"></div>
            <div class="input-group">
                <input type="email" id="email" v-model="user.email" />
                <button @click.prevent="updateField('email')">수정하기</button>
            </div>
            <div v-if="fieldMessages.email" class="field-message">
                {{ fieldMessages.email }}
            </div>
        </div>

        <div class="box">
            <label for="password1">Password</label>
            <div class="black-bar"></div>
            <div class="input-group">
                <input type="password" id="password1" v-model="password1" placeholder="비밀번호 입력" />
                <input type="password" id="password2" v-model="password2" placeholder="비밀번호 확인" />
                <button @click.prevent="updatePassword">수정하기</button>
            </div>
            <div v-if="fieldMessages.password" class="field-message">
                {{ fieldMessages.password }}
            </div>
        </div>

        <button @click.prevent="updateAll" class="upateall">전체 수정하기</button>
        <div v-if="message" class="message">
            {{ message }}
        </div>

        <div class="black-bar"></div>

        <div class="button-group">
            <button @click="goToMypage" class="mypage">마이페이지</button>
            <div>
                <button @click="showDeleteModal = true" class="delete">회원 탈퇴</button>

                <div v-if="showDeleteModal" class="modal">
                    <div class="modal-content">
                        <h4>비밀번호 확인</h4>
                        <input type="password" v-model="password" placeholder="비밀번호를 입력하세요" />
                        <div class="modal-buttons">
                            <button @click="confirmDeleteAccount">확인</button>
                            <button @click="showDeleteModal = false">취소</button>
                        </div>
                        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

</template>

  <script>
import apiClient from "@/store/api";

export default {
    name: 'Update',
    data() {
        return {
            user: {
                id: "",
                nick_name: "",
                email: "",
                password1: "",
                password2: "",
                profile_image: null,
            },
            previewImage: null,
            fieldMessages: {
                profile_image: "",
                nick_name: "",
                email: "",
                password: "",
            },
            showDeleteModal: false,
            password: "",
            errorMessage: "",
            message: "",
        };
    },
    methods: {
        async fetchUserData() {
            try {
                const response = await apiClient.get("/user/mypage/me/");
                this.user = response.data;

                if (this.user.profile_image) {
                    this.previewImage = this.user.profile_image;
                }
            } catch (error) {
                console.error("사용자 정보를 불러오는 중 오류:", error);
            }
        },

        async updateField(fieldName) {
            const formData = new FormData();
            formData.append(fieldName, this.user[fieldName]);

            try {
                const response = await apiClient.patch("/user/mypage/me/", formData, {
                    headers: {
                        Authorization: `Token ${localStorage.getItem("authToken")}`,
                        "Content-Type": "multipart/form-data",
                    },
                });
                this.fieldMessages[fieldName]= "성공적으로 수정되었습니다.";
                console.log(`${fieldName} 수정 성공:`, response.data);
            } catch (error) {
                console.error(`${fieldName} 수정 중 오류:`, error.response?.data || error);
                this.fieldMessages[fieldName] = "수정에 실패했습니다.";
            }
        },

        async updateAll() {
            const formData = new FormData();
            if (this.user.profile_image) formData.append("profile_image", this.user.profile_image);
            formData.append("nick_name", this.user.nick_name);
            formData.append("email", this.user.email);
            if (this.password1 && this.password2) {
                formData.append("password1", this.password1);
                formData.append("password2", this.password2);
            }

            try {
                const response = await apiClient.patch("/user/mypage/me/", formData, {
                    headers: {
                        Authorization: `Token ${localStorage.getItem("authToken")}`,
                        "Content-Type": "multipart/form-data",
                    },
                });
                this.message = "전체 정보가 성공적으로 수정되었습니다.";
                console.log("수정 성공:", response.data);
            } catch (error) {
                const errors = error.response?.data || {};

                this.message = "전체 정보 수정에 실패했습니다.";

                for (const [key, value] of Object.entries(errors)) {
                    this.fieldMessages[key] = Array.isArray(value) ? value.join(", ") : value;
                }
                console.log("오류 내용:", errors);
            }
        },

        async updatePassword() {
            if (this.password1 !== this.password2) {
                this.fieldMessages.password = "비밀번호가 일치하지 않습니다.";
                return;
            }

            try {
                const formData = new FormData();
                formData.append("password1", this.password1);
                formData.append("password2", this.password2);
                formData.append("nick_name", this.user.nick_name || "");
                formData.append("email", this.user.email || "");

                const response = await apiClient.patch("/user/mypage/me/", formData, {
                    headers: {
                        Authorization: `Token ${localStorage.getItem("authToken")}`,
                        "Content-Type": "multipart/form-data",
                    },
                });

                this.fieldMessages.password = "비밀번호가 성공적으로 변경되었습니다.";
            } catch (error) {
                console.error("비밀번호 변경 중 오류:", error.response?.data || error);
                this.fieldMessages.password = "비밀번호 변경에 실패했습니다.";
            }
        },


        onFileChange(event) {
            const file = event.target.files[0];

            if (!file) {
                console.error("파일 선택이 되지 않았습니다.");
                return;
            }

            this.user.profile_image = file;

            if (file) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    this.previewImage = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        },

        async confirmDeleteAccount() {
            if (!this.password) {
                this.errorMessage = "비밀번호를 입력해주세요.";
                return;
            }
            try {
                const response = await apiClient.post("/user/mypage/delete/", {
                    password: this.password,
                }, {
                    headers: {
                        Authorization: `Token ${localStorage.getItem("authToken")}`,
                        "Content-Type": "multipart/form-data",
                    },
                });

                alert("회원 탈퇴가 완료되었습니다. 회원가입 페이지로 이동합니다.");
                localStorage.removeItem("authToken");
                window.location.href = "/signup";
            } catch (err) {
                console.error("회원 탈퇴 중 오류:", err.response?.data || err);
                this.errorMessage = err.response?.data?.error || "회원 탈퇴에 실패했습니다.";
            }
        },
        goToMypage() {
            this.$router.push("/mypage");
        },
    },
    mounted() {
        document.title = '회원정보수정 - Recipick'
        this.fetchUserData();
    },
};
</script>

<style scoped>
.update {
    max-width: 700px;
    margin: 17px auto;
    padding: 20px;
    border: 1px solid #d6d6d6;
}
.update form {
    display: flex;
    flex-direction: column;
}
.box {
    margin-bottom: 30px;
    display: flex;
    flex-direction: column;
}
.box label {
    display: block;
    font-size: 20px;
    font-weight: bold;
    text-align: left;
    margin-bottom: 2px;
}
.input-group {
    flex: 1;
    display: flex;
    align-items: center;
    gap: 5%;
    justify-content: space-between;
}
.input-group input {
    flex: 1;
    padding: 10px;
    border: 1px solid #bebebe;
    font-size: 15px;
    margin-left: 20px;
    margin-right: 20px;
    width: 50%;
}
.upateall {
    width: 130px;
    height: 44px;
    padding: 8px;
    background-color: #5c5c5c;
    color: white;
    border: none;
    border-radius: 5px;
    font-size: 15px;
    font-weight: bold;
    margin-bottom: 20px;
}
.input-group button {
    width: 100px;
    height: 44px;
    padding: 8px;
    background-color: #5c5c5c;
    color: white;
    border: none;
    border-radius: 5px;
    font-size: 15px;
    font-weight: bold;
    margin-right: 15px;
}

.preview {
    margin-bottom: 10px;
    text-align: left;
}
.preview img {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    border: 1px solid #d6d6d6;
    object-fit: cover;
    margin-bottom: 10px;
}
.field-message,
.message {
  margin-top: 20px;
  text-align: center;
  color: red;
}

/* 블랙바 */
.black-bar {
    width: 100%;
    height: 4px;
    background-color: black;
    margin-top: 5px;
    margin-bottom: 13px;
}

/* 회원탈퇴, 마이페이지 버튼 */
.button-group {
    display: flex;
    justify-content: center;
    gap: 15px;
    margin-top: 20px;
}
.button-group button {
    width: 140px;
    height: 44px;
    font-size: 16px;
    font-weight: bold;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: all 0.3s ease;
}
.mypage {
    background-color: #658aee;
    color: white;
}
.delete {
    background-color: #f44336;
    color: white;
}
/* 비밀번호 확인 모달 */
.modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
}
.modal-content {
    background: white;
    padding: 20px;
    border-radius: 5px;
    text-align: center;
    width: 300px;
}
.modal-buttons {
    display: flex;
    justify-content: space-between;
    margin-top: 15px;
}
.modal-buttons button {
    flex: 1;
    margin: 0 5px;
    padding: 10px;
    background: #f0f0f0;
    border: 1px solid #ccc;
    border-radius: 5px;
    cursor: pointer;
    transition: background 0.3s ease;
}
.error-message {
    color: red;
    margin-top: 10px;
}

</style>