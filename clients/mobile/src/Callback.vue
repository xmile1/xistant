<template>
  {{ error?.message }}
</template>

<script setup>
import { useAuth0 } from "@auth0/auth0-vue";

const { error } = useAuth0();
</script>
