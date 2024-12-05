<template>
    <div>
        <div class="profile-container">
            <div class="profile"></div>
            <div class="name-container">
                <span class="profile-name">{{ user.nick_name }} - </span>
                <span class="profile-name">{{ user.level }}</span>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ProfileHeader',
    props: {
        user: {}
    }
}
</script>

<style scoped>
.profile-container {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
}

.profile {
    background-image: url("https://picsum.photos/100?random=0");
    width: 50px;
    height: 50px;
    background-size: 100%;
    border-radius: 50%;
}

.name-container {
    display: flex;
    margin-left: 15px;
}

.profile-name {
    font-size: 20px;
}
</style>