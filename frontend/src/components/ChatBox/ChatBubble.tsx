import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import '../../App.css';

interface ChatBubbleProps {
  message: string;
  sender: 'user' | 'assistant';
  timestamp: string; // 添加时间戳属性
}

const ChatBubble: React.FC<ChatBubbleProps> = ({ message, sender, timestamp }) => {
  const [showThoughts, setShowThoughts] = useState(false); // 控制思维链显示状态

  const isUser = sender === 'user';
  const bubbleClass = isUser
    ? 'bg-blue-500 text-white dark:bg-blue-700'
    : 'bg-gray-200 text-black dark:bg-gray-600 dark:text-white';
  const alignClass = isUser ? 'justify-end' : 'justify-start';

  // 提取思维链信息和实际消息
  const thoughtMatch = message.match(/<think>([\s\S]*?)<\/think>/);
  const thoughts = thoughtMatch ? thoughtMatch[1].trim() : null;
  const displayMessage = message.replace(/<think>[\s\S]*?<\/think>/, '').trim();

  return (
    <div className={`flex ${alignClass} mb-2`}>
      <div className="flex flex-col max-w-xs">
        {thoughts && showThoughts && (
          <div className="mb-1 p-2 bg-yellow-100 text-black rounded-md">
            <strong>Thought:</strong>
            <p>{thoughts}</p>
          </div>
        )}
        <div
          className={`px-4 py-2 rounded-lg ${bubbleClass}`}
          onClick={() => setShowThoughts(!showThoughts)} // 点击切换显示状态
        >
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            components={{
              p: ({ node, ...props }) => <p style={{ whiteSpace: 'pre-wrap' }} {...props} />,
            }}
          >
            {displayMessage}
          </ReactMarkdown>
        </div>
        <span className="text-xs text-gray-500 mt-1 self-end">{timestamp}</span>
      </div>
    </div>
  );
};

export default ChatBubble;
