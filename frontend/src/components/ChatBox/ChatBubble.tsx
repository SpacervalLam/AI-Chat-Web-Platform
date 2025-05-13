// frontend/src/components/ChatBox/ChatBubble.tsx
import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import '../../App.css';

interface ChatBubbleProps {
  sender: 'user' | 'assistant';
  message: string;
  thoughts?: string;
  timestamp: string;
}

const ChatBubble: React.FC<ChatBubbleProps> = ({ message, thoughts, sender, timestamp }) => {
  const [showThoughts, setShowThoughts] = useState(false);
  const isUser = sender === 'user';
  const bubbleClass = isUser
    ? 'bg-blue-500 text-white dark:bg-blue-700'
    : 'bg-gray-200 text-black dark:bg-gray-600 dark:text-white';
  const alignClass = isUser ? 'justify-end' : 'justify-start';

  const toggleThoughts = () => setShowThoughts(prev => !prev);

  return (
    <div className={`flex ${alignClass} mb-2`}>
      <div className="flex flex-col max-w-xs">
        {/* 思维链区域：透明背景 & 边框 */}
        {thoughts && showThoughts && (
          <div
            className="
              mb-1 p-2
              bg-transparent
              border border-gray-300 dark:border-gray-600
              rounded-md
              cursor-pointer
            "
            onClick={toggleThoughts}
          >
            <strong className="text-gray-700 dark:text-gray-200">Thought:</strong>
            <p className="whitespace-pre-wrap text-gray-800 dark:text-gray-100">
              {thoughts}
            </p>
          </div>
        )}
        {/* 对话气泡 */}
        <div
          className={`px-4 py-2 rounded-lg ${bubbleClass} cursor-pointer`}
          onClick={thoughts ? toggleThoughts : undefined}
        >
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            components={{
              p: ({ node, ...props }) => <p style={{ whiteSpace: 'pre-wrap' }} {...props} />,
            }}
          >
            {message}
          </ReactMarkdown>
        </div>
        <span className="text-xs text-gray-500 dark:text-gray-400 mt-1 self-end">
          {timestamp}
        </span>
      </div>
    </div>
  );
};

export default ChatBubble;
