<script setup>
import { nextTick, onMounted, ref } from "vue";
import VueMarkdown from "vue-markdown-render";
import YouIcon from "./assets/account.svg";
import BotIcon from "./assets/account-tie.svg";

const chatHistory = ref(
  JSON.parse(localStorage.getItem("chatHistory") || "[]")
);
const query = ref("");
const messagesSection = ref(null);
const loading = ref(false);

onMounted(() => {
  messagesSection.value.scrollTop = messagesSection.value.scrollHeight;
});

const sendQuery = async () => {
  loading.value = true;
  const queryValue = query.value;
  query.value = "";

  chatHistory.value = [
    ...chatHistory.value,
    {
      id: chatHistory.value.length,
      type: "message",
      name: "You",
      avatar: "https://i.pravatar.cc/150?img=2",
      text: queryValue,
    },
  ];

  nextTick(() => {
    messagesSection.value.scrollTop = messagesSection.value.scrollHeight;
  });

  const response = await fetch("http://192.168.0.156:8000", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      query: queryValue,
    }),
  });

  const data = await response.json();

  chatHistory.value = [
    ...chatHistory.value,
    {
      id: chatHistory.value.length,
      type: "message",
      name: "Assistant",
      avatar: "https://i.pravatar.cc/150?img=1",
      text: data,
    },
  ];

  loading.value = false;

  localStorage.setItem("chatHistory", JSON.stringify(chatHistory.value));
  await nextTick();

  messagesSection.value.scrollTop = messagesSection.value.scrollHeight;
};

const clearStorage = (event) => {
  if (event.detail === 3) {
    localStorage.removeItem("chatHistory");
    chatHistory.value = [];
  }
};

const onKeypress = (event) => {
  // if its command + enter
  if (event.metaKey && event.key === "Enter") {
    sendQuery();
  }
};
</script>

<template>
  <div ref="messagesSection" class="mesages-wrapper">
    <template v-for="message in chatHistory" :key="message.id">
      <section class="messages">
        <img
          width="24"
          :src="message.name === 'You' ? YouIcon : BotIcon"
          alt="avatar"
          @click="clearStorage"
        />
        <VueMarkdown class="text" :source="message.text" />
      </section>
    </template>
  </div>
  <div class="input">
    <textarea
      autofocus
      @keydown.meta.enter="sendQuery"
      rows="5"
      res
      v-model="query"
    />
    <button @click="sendQuery">
      <template v-if="loading">
        <span>.</span>
        <span>.</span>
        <span>.</span>
      </template>
      <span v-else> Send </span>
    </button>
  </div>
</template>

<style scoped>
.messages {
  display: grid;
  grid-template-columns: 36px auto;
  margin-bottom: 10px;
  padding: 16px;
}

.messages:nth-child(even) {
  background-color: #444654;
}

.mesages-wrapper {
  height: calc(100vh - 120px);
  overflow-y: scroll;
}

textarea {
  border: none;
  resize: none;
  font-family: inherit;
}

.input {
  display: grid;
  grid-template-columns: 1fr 100px;
  position: fixed;
  bottom: 0;
  width: 100%;
  background-color: #444654;
  padding: 16px;
  box-sizing: border-box;
}
</style>
