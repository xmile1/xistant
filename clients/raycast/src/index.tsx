import { useEffect, useState } from "react";
import { ActionPanel, Action, Icon, List, Detail, useNavigation, Form } from "@raycast/api";
import { LocalStorage } from "@raycast/api";
import fetch from "cross-fetch";

export default function Command(props: any) {
  const [markdown, setMarkdown] = useState<string>("");
  const { push } = useNavigation();
  const [isLoading, setIsLoading] = useState(false);
  const [history, setHistory] = useState([]);

  useEffect(() => {
    LocalStorage.getItem("conversation-history").then(async (storeHistory) => {
      const parsedHistory = JSON.parse((storeHistory as string) || "[]");
      setHistory(parsedHistory);
      setMarkdown(parseConversationToMarkdown(parsedHistory));
    });
  }, []);

  const queryAi = async (query: string, history: any) => {
    setIsLoading(true);
    const response = await fetch("http://0.0.0.0:8000", {
      method: "POST",
      body: JSON.stringify({ query }),
    });
    const data = await response.json();

    const newData = [query, data];
    const newHistory = [...newData, ...history];
    LocalStorage.setItem("conversation-history", JSON.stringify(newHistory));

    setMarkdown(parseConversationToMarkdown(newHistory));
    setIsLoading(false);
  };

  const parseConversationToMarkdown = (conversation: any) => {
    const md = conversation.reduce((acc: any, item: any, index: number) => {
      if (index % 2 === 0) {
        return acc + ">" + item + "\n\r";
      }
      return acc + item + "\n\r";
    }, "");
    return md;
  };

  useEffect(() => {
    if (props.arguments.query) queryAi(props.arguments.query, history);
  }, [props.arguments.query]);

  return (
    <Detail
      markdown={markdown}
      isLoading={isLoading}
      actions={
        <ActionPanel>
          <Action title="Press Enter to Make a Query" onAction={() => push(<QueryPage />)} />
        </ActionPanel>
      }
    />
  );
}

function QueryPage() {
  const { push } = useNavigation();
  const [searchText, setSearchText] = useState("");
  const [history, setHistory] = useState([]);

  useEffect(() => {
    LocalStorage.getItem("conversation-history").then(async (history) => {
      setHistory(JSON.parse((history as string) || "[]"));
    });
  }, []);

  const onSubmitQuery = async () => {
    push(<Command arguments={{ query: searchText }} />);
  };

  const goToMultilineQuery = async () => {
    push(<QueryForm initialValue={searchText} />);
  };

  return (
    <List
      isShowingDetail
      filtering={false}
      onSearchTextChange={setSearchText}
      searchBarPlaceholder="How can i help you today, Uyi?"
      actions={
        <ActionPanel>
          <Action title="Press Enter to Submit Query" onAction={onSubmitQuery} />
          <Action title="Press Shift Enter for Multiline Query" onAction={goToMultilineQuery} />
        </ActionPanel>
      }
    >
      {history.map((item, index) => (
        <List.Item
          accessories={
            index % 2 === 0 ? [{ icon: Icon.Person, tooltip: "A person" }] : [{ icon: Icon.Bolt, tooltip: "A bot" }]
          }
          actions={
            <ActionPanel>
              <Action title="Press Enter to Submit Query" onAction={onSubmitQuery} />
              <Action title="Press Shift Enter for Multiline Query" onAction={goToMultilineQuery} />
            </ActionPanel>
          }
          detail={<List.Item.Detail markdown={item} />}
          title={item}
          key={index}
        />
      ))}
    </List>
  );
}

function QueryForm({ initialValue = "" }) {
  const { push } = useNavigation();
  const [searchText, setSearchText] = useState(initialValue);

  const onSubmitQuery = async () => {
    push(<Command arguments={{ query: searchText }} />);
  };

  return (
    <Form
      actions={
        <ActionPanel>
          <Action title="Press Cmd and Enter to Submit Query" onAction={onSubmitQuery} />
        </ActionPanel>
      }
    >
      <Form.TextArea
        value={searchText}
        onChange={setSearchText}
        id="query"
        title="Query"
        placeholder="How can i help you today, Uyi?"
      />
    </Form>
  );
}
