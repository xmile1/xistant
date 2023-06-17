<script setup>
import { computed, nextTick, onMounted, ref } from "vue";
import VueMarkdown from "vue-markdown-render";
import YouIcon from "./assets/account.svg";
import BotIcon from "./assets/account-tie.svg";

const apiUrl = import.meta.env.VITE_API_URL;

const chatHistory = ref(
  JSON.parse(localStorage.getItem("chatHistory") || "[]")
);
const query = ref("");
const messagesSection = ref(null);
const loading = ref(false);
const slashCommands = ref([]);
const showAutocomplete = ref(false);
const currentSelectedIndex = ref(0);
const selectedSlashCommand = ref("");

onMounted(() => {
  messagesSection.value.scrollTop = messagesSection.value.scrollHeight;
  getSlashCommands();
});

const getSlashCommands = async () => {
  const response = await fetch(`${apiUrl}/slash-commands`);
  const data = await response.json();
  slashCommands.value = data;
};

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

  const finalQueryValue = queryValue.startsWith("/")
    ? queryValue
    : selectedSlashCommand.value + queryValue;

  const response = await fetch(apiUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      query: finalQueryValue,
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
      text: typeof data === "object" ? JSON.stringify(data) : data,
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

const handleInputChange = (event) => {
  if (!query.value.startsWith("/") && event.target.value.startsWith("/")) {
    showAutocomplete.value = true;
  } else if (
    query.value.startsWith("/") &&
    !event.target.value.startsWith("/")
  ) {
    showAutocomplete.value = false;
  }

  query.value = event.target.value;

  if (showAutocomplete.value) {
    currentSelectedIndex.value = 0;
  }
};

const filteredSlashCommands = computed(() => {
  return slashCommands.value.filter((slashCommand) => {
    return slashCommand.name.includes(query.value.split(" ")[0]);
  });
});

const handleKeyDown = (event) => {
  if (
    event.key === "Enter" &&
    !showAutocomplete.value &&
    !event.metaKey &&
    !event.shiftKey
  ) {
    event.preventDefault();
    sendQuery();
  }

  if (!filteredSlashCommands.value.length || !showAutocomplete.value) return;

  if (event.key === "ArrowUp" && showAutocomplete.value) {
    event.preventDefault();
    currentSelectedIndex.value =
      currentSelectedIndex.value === 0
        ? filteredSlashCommands.value.length - 1
        : currentSelectedIndex.value - 1;
  } else if (event.key === "ArrowDown" && showAutocomplete.value) {
    event.preventDefault();
    currentSelectedIndex.value =
      currentSelectedIndex.value === filteredSlashCommands.value.length - 1
        ? 0
        : currentSelectedIndex.value + 1;
  } else if (event.key === "Enter" && showAutocomplete.value) {
    handleAutocompleteItemClick(
      event,
      filteredSlashCommands.value[currentSelectedIndex.value].name
    );
  }

  // if enter but showAutocomplete is false, send the query

  if (event.key === " " || event.key === "Escape") {
    showAutocomplete.value = false;
  }
};

const handleAutocompleteItemClick = (event, command) => {
  event.preventDefault();
  query.value = query.value.replace(query.value.split(" ")[0], command);
  showAutocomplete.value = false;
};

const handleFocus = () => {
  // showAutocomplete.value = true;
};

const handleBlur = () => {
  // showAutocomplete.value = false;
};

const handleSelectChange = (event) => {
  selectedSlashCommand.value = event.target.value;
};
</script>

<template>
  <div class="app-wrapper">
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
      <!-- a dropdown with the list of slash commands -->
      <div />
      <select class="select" @change="handleSelectChange">
        <option value="">Select a command</option>
        <option v-for="command in slashCommands" :value="command.name">
          {{ command.name.replace("/", "") }}
        </option>
      </select>
      <div style="position: relative">
        <ul
          v-if="showAutocomplete && filteredSlashCommands.length"
          class="autocomplete"
        >
          <template
            v-for="(slashCommand, index) in filteredSlashCommands"
            :key="filteredSlashCommands.length + index"
          >
            <li
              :class="{
                active: index === currentSelectedIndex,
              }"
              @click="handleAutocompleteItemClick($event, slashCommand.name)"
            >
              {{ slashCommand.name.replace("/", "") }}
            </li>
          </template>
        </ul>
        <textarea
          autofocus
          rows="4"
          @input="handleInputChange"
          :value="query"
          @keydown="handleKeyDown"
          @focus="handleFocus"
          @blur="handleBlur"
        />
      </div>
      <button @click="sendQuery">
        <template v-if="loading">
          <span class="animate-loading">...</span>
        </template>
        <span v-else> Send </span>
      </button>
    </div>
  </div>
</template>

<style scoped lang="scss">
.app-wrapper {
  display: grid;
  place-content: center;
  grid-template-rows: 1fr 140px;
  height: 100vh;

  > * {
    max-width: 48rem;
  }
}
.messages {
  display: grid;
  grid-template-columns: 36px auto;
  margin-bottom: 10px;
  padding: 16px;
}

.messages:nth-child(even) {
  background-color: #777b93;
}

.mesages-wrapper {
  overflow-y: scroll;
}

.text {
  overflow: auto;
}
:deep(.text pre) {
  overflow-x: auto;
}

textarea {
  border: none;
  resize: none;
  font-family: inherit;
  width: 100%;
}

.input {
  display: grid;
  grid-template-columns: 1fr 100px;
  bottom: 0;
  width: 100%;
  background-color: #777b93;
  padding: 16px;
  box-sizing: border-box;
  column-gap: 16px;
}

.select {
  grid-column: 1 / 3;
  justify-self: end;
  margin-bottom: 16px;
  padding: 0 16px 0 4px;
  height: 20px;
}

.autocomplete {
  position: absolute;
  background-color: #777b93;
  padding: 0;
  margin: 0;
  transform: translateY(-110%);
  border: 1px solid #666b8a;
  list-style: none;
  & > li {
    padding: 4px 8px;
    cursor: pointer;
  }
}

.active {
  background-color: #fff;
  color: #000;
}

.animate-loading {
  animation: loading 1s infinite;
}

@keyframes loading {
  0% {
    opacity: 0.2;
  }
  50% {
    opacity: 1;
  }
  100% {
    opacity: 0.2;
  }
}
</style>
