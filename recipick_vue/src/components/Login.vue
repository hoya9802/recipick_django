<template>
  <div class="login-box">
    <img src="@/assets/login.png" alt="Login Image" />
    <form>  <!--로그인 -->
        <input placeholder="아이디" required />
        <input type="password" placeholder="비밀번호" required />
        <button type="submit">로그인</button>
    </form>
    <a href="">아이디 찾기 / </a>
    <a href="">비밀번호 찾기 / </a>
    <a href="">회원가입</a>
  </div>
</template>

<script>

export default {
  data() {
    return {
      id: '',
      password: '',
    };
  },
}
</script>

<style>
.login-box {
  background: white;
  border: 1px solid #dbdbdb;
  padding: 20px;
  margin-bottom: 20px;
  text-align: center;
  width: 300px;
  height: 400px;
}

.login-box img {
  margin-top: 30px;
  max-width: 160px;
  width: 60%;
  height: auto;
}

input {
  width: 70%;
  margin-bottom: 10px;
  padding: 10px;
  border: 1px solid #dbdbdb;
  border-radius: 5px;
  background: #fafafa;
  font-size: 40%;
}

button {
  width: 77%;
  padding: 8px;
  color: white;
  background-color: #fadba0;
  border: none;
  border-radius: 5px;
  font-weight: bold;
  cursor: pointer;
  margin-bottom: 20px;
}

a {
  text-decoration-line: none;
  color: #fdb226;
  font-size: 60%;
}

</style>