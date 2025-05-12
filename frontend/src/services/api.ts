import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export interface ChatRequest {
  messages: ChatMessage[];
  model: string;
  stream?: boolean;
}

export interface ChatResponse {
  response: string;
  model: string;
}

/*
export const getModels = async (): Promise<string[]> => {
  try {
    const response = await api.get<{ models: string[] }>('/chat/models');
    return response.data.models;
  } catch (error) {
    console.error('Error fetching models:', error);
    throw error;
  }
};

export const sendMessage = async (messages: ChatMessage[], model: string) => {
  try {
    const response = await api.post('/chat', {
      messages, // 发送消息列表
      model,
      stream: false,
    });
    return response.data;
  } catch (error) {
    console.error('Error sending message:', error);
    throw error;  
  }
};

export const streamMessage = async (messages: ChatMessage[], model: string) => {
  try {
    const response = await api.post('/chat/stream', {
      messages, // 发送消息列表
      model,
      stream: true,
    }, {
      responseType: 'stream', // 用于流式响应
    });
    return response.data;
  } catch (error) {
    console.error('Error streaming message:', error);
    throw error;
  }
};
*/

export const sendChatCompletion = async (
  messages: ChatMessage[],
  model: string
): Promise<{ response: string; model: string }> => {
  try {
    // Log the request body for debugging
    console.log('[DEBUG] Sending request:', { messages, model, stream: false });

    const response = await api.post<{ response: string; model: string }>('/chat/completions', {
      messages,
      model,
      stream: false,
    });

    return response.data;
  } catch (error) {
    console.error('Error sending message:', error);
    throw error;
  }
};

export default api;
