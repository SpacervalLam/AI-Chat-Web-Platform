import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import '../../App.css';

interface ChatBubbleProps {
  message: string;
  sender: 'user' | 'assistant';
  timestamp: string; // 添加时间戳属性
}

const ChatBubble: React.FC<ChatBubbleProps> = ({ message, sender, timestamp }) => {
  const isUser = sender === 'user';
  const bubbleClass = isUser
    ? 'bg-blue-500 text-white dark:bg-blue-700'
    : 'bg-gray-200 text-black dark:bg-gray-600 dark:text-white';
  const alignClass = isUser ? 'justify-end' : 'justify-start';

  return (
    <div className={`flex ${alignClass} mb-2`}>
      <div className="flex flex-col max-w-xs">
        <div className={`px-4 py-2 rounded-lg ${bubbleClass}`}>
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            components={{
              p: ({ node, ...props }) => <p style={{ whiteSpace: 'pre-wrap' }} {...props} />,
            }}
          >
            {message}
          </ReactMarkdown>
        </div>
        <span className="text-xs text-gray-500 mt-1 self-end">{timestamp}</span>
      </div>
    </div>
  );
};

export default ChatBubble;
  