<template>
    <div>
        <div class="profile-container">
            <div v-if="user.profile_image" class="profile" :style="{ backgroundImage: `url(${user.profile_image})` }"></div>
            <div v-else class="profile"></div>
            <div class="name-container">
                <span class="profile-name">{{ user.nick_name }} - {{ user.level }}</span>
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
    background-image: url("@/assets/default-profile.png");
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