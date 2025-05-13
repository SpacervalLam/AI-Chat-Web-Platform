// frontend/src/App.tsx
import React, { useState, useRef, useEffect } from 'react';
import ChatBubble from './components/ChatBox/ChatBubble';
import ChatInput from './components/ChatBox/ChatInput';
import ModelSelector from './components/ChatBox/ModelSelector';
import ThemeToggle from './components/ChatBox/ThemeToggle';
import { sendChatCompletion } from './services/api';
import './App.css';

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  thoughts?: string;
  timestamp?: string;
}

const App: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const messagesRef = useRef<ChatMessage[]>(messages);
  const [model, setModel] = useState('deepseek-coder:1.3b');
  const [isDisabled, setIsDisabled] = useState(false);
  const chatContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesRef.current = messages;
  }, [messages]);

  const handleSend = async (message: string) => {
    const timestamp = new Date().toLocaleTimeString();
    // 用户消息无需 thoughts
    const userMsg: ChatMessage = { role: 'user', content: message, timestamp };
    const newMessages = [...messagesRef.current, userMsg];
    messagesRef.current = newMessages;
    setMessages(newMessages);
    setIsDisabled(true);

    try {
      const response = await sendChatCompletion(messagesRef.current, model);
      const raw = response.response;

      // 用正则提取 <think>…</think> 内容
      const thinkMatch = raw.match(/<think>([\s\S]*?)<\/think>/);
      const thoughts = thinkMatch ? thinkMatch[1].trim() : undefined;
      // 去掉标签后剩余的显示文本
      const content = raw.replace(/<think>[\s\S]*?<\/think>/, '').trim();

      const assistantMsg: ChatMessage = {
        role: 'assistant',
        content,
        thoughts,
        timestamp: new Date().toLocaleTimeString(),
      };

      messagesRef.current = [...messagesRef.current, assistantMsg];
      setMessages(messagesRef.current);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMsg: ChatMessage = {
        role: 'assistant',
        content: 'Error: Unable to fetch response.',
        timestamp: new Date().toLocaleTimeString(),
      };
      messagesRef.current = [...messagesRef.current, errorMsg];
      setMessages(messagesRef.current);
    } finally {
      setIsDisabled(false);
    }
  };

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTo({
        top: chatContainerRef.current.scrollHeight,
        behavior: 'smooth',
      });
    }
  }, [messages]);

  return (
    <div className="flex flex-col h-screen bg-gradient-to-b from-gray-100 to-gray-300 dark:from-gray-800 dark:to-gray-900">
      <header className="flex items-center justify-between p-2 bg-white dark:bg-gray-800 shadow-md h-12">
        <h1 className="text-lg font-semibold text-gray-800 dark:text-gray-200">Platform</h1>
        <ModelSelector
          model={model}
          onChange={setModel}
          className="dark:bg-gray-700 dark:text-gray-200 text-sm"
        />
        <ThemeToggle />
      </header>

      <div
        ref={chatContainerRef}
        className="flex-1 overflow-y-auto p-4 space-y-4 pb-20 box-border"
      >
        {messages.length === 0 ? (
          <p className="text-gray-500 text-center">Start a conversation...</p>
        ) : (
          messages.map((msg, idx) => (
            <ChatBubble
              key={idx}
              sender={msg.role}
              message={msg.content}
              thoughts={msg.thoughts}
              timestamp={msg.timestamp || ''}
            />
          ))
        )}
      </div>

      <footer className="p-4 bg-white dark:bg-gray-800 shadow-md">
        <ChatInput
          onSend={handleSend}
          isCentered={false}
          isDisabled={isDisabled}
          className="dark:bg-gray-700 dark:text-gray-200"
        />
      </footer>
    </div>
  );
};

export default App;
