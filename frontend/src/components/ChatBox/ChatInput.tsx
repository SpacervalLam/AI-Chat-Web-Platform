import React, { useState, useRef } from 'react';
import '../../App.css';

interface ChatInputProps {
  onSend: (message: string) => void;
  isCentered: boolean;
  isDisabled: boolean; // 新增属性，用于控制发送按钮的可用性
  className?: string; // 新增className属性
}

const ChatInput: React.FC<ChatInputProps> = ({ onSend, isCentered, isDisabled, className }: ChatInputProps) => {
  const [input, setInput] = useState('');
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const handleSend = () => {
    if (input.trim() !== '') {
      onSend(input);
      setInput('');
      if (inputRef.current) {
        inputRef.current.style.height = '65px'; // 发送消息后重置高度
      }
    }
  };

  const handleInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value);
    if (inputRef.current) {
      const maxHeight = 200; // 最大高度
      inputRef.current.style.height = 'auto';
      inputRef.current.style.height = `${Math.min(inputRef.current.scrollHeight, maxHeight)}px`;
    }
  };

  return (
    <div
      className={`p-4 fixed bottom-0 left-1/2 transform -translate-x-1/2 w-full max-w-3xl flex items-center bg-white dark:bg-gray-800 shadow-md ${className || ''}`}
    >
      <textarea
        ref={inputRef}
        className="flex-1 border rounded px-4 py-2 resize-y overflow-y-auto mr-2 bg-white dark:bg-gray-700 dark:text-gray-200 border-gray-300 dark:border-gray-600" // 添加暗黑模式样式
        value={input}
        onChange={handleInput}
        onKeyDown={(e) => {
          if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
          }
        }}
        placeholder="Type a message ..."
        disabled={isDisabled} // 禁用输入框
        style={{ height: '65px' }} // 设置初始高度为80px
      />
      <button
        className="bg-blue-500 dark:bg-blue-700 text-white px-4 py-2 rounded"
        onClick={handleSend}
        disabled={isDisabled} // 禁用发送按钮
      >
        Send
      </button>
    </div>
  );
};

export default ChatInput;
