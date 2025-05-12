import * as React from 'react';
import { useEffect, useState } from 'react';
import axios from 'axios';
import '../../App.css';

interface ModelSelectorProps {
  model: string;
  onChange: (model: string) => void;
  className?: string; // 新增className属性
}

const ModelSelector: React.FC<ModelSelectorProps> = ({ model, onChange, className }: ModelSelectorProps) => {
  const [models, setModels] = useState<string[]>([]); // 存储模型列表

  useEffect(() => {
    const fetchModels = async () => {
      try {
        const response = await axios.get<{ models: string[] }>('http://localhost:8000/api/v1/chat/models'); // 修正请求路径并添加类型
        setModels(response.data.models);
      } catch (error) {
        console.error('Error fetching models:', error);
      }
    };

    fetchModels();
  }, []);

  return (
    <div className="p-4">
      <label className="mr-2 text-black dark:text-white">Select model:</label>
      <select
        value={model}
        onChange={(e) => onChange(e.target.value)}
        className={`bg-white dark:bg-gray-700 dark:text-gray-200 border border-gray-300 dark:border-gray-600 rounded-md p-2 text-black dark:text-white ${className || ''}`}
      >
        {models.map((modelName) => (
          <option key={modelName} value={modelName}>
            {modelName}
          </option>
        ))}
      </select>
    </div>
  );
};

export default ModelSelector;
