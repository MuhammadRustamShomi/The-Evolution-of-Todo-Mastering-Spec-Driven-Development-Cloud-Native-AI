'use client';

import { useState, useCallback } from 'react';
import { Header } from '@/components/layout/header';
import { ChatInterface } from '@/components/chat/chat-interface';
import { streamChat } from '@/lib/chat';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [streamingContent, setStreamingContent] = useState('');
  const [conversationId, setConversationId] = useState<string>();

  const handleSendMessage = useCallback(
    async (message: string) => {
      // Get token from localStorage
      const token = localStorage.getItem('access_token');
      if (!token) {
        console.error('No access token');
        return;
      }

      // Add user message
      const userMessage: Message = {
        id: `user-${Date.now()}`,
        role: 'user',
        content: message,
      };
      setMessages((prev) => [...prev, userMessage]);
      setIsLoading(true);
      setStreamingContent('');

      try {
        let content = '';

        for await (const event of streamChat(
          message,
          token,
          conversationId,
          messages.map((m) => ({ role: m.role, content: m.content }))
        )) {
          switch (event.event) {
            case 'conversation_id':
              setConversationId(event.data);
              break;
            case 'message':
              content += event.data;
              setStreamingContent(content);
              break;
            case 'done':
              // Add assistant message
              const assistantMessage: Message = {
                id: `assistant-${Date.now()}`,
                role: 'assistant',
                content,
              };
              setMessages((prev) => [...prev, assistantMessage]);
              setStreamingContent('');
              break;
          }
        }
      } catch (error) {
        console.error('Chat error:', error);
        const errorMessage: Message = {
          id: `error-${Date.now()}`,
          role: 'assistant',
          content: 'Sorry, I encountered an error. Please try again.',
        };
        setMessages((prev) => [...prev, errorMessage]);
      } finally {
        setIsLoading(false);
      }
    },
    [conversationId, messages]
  );

  const handleClear = useCallback(() => {
    setMessages([]);
    setConversationId(undefined);
    setStreamingContent('');
  }, []);

  return (
    <div className="flex flex-col h-screen">
      <Header title="AI Chat" />

      <div className="flex-1 overflow-hidden">
        <div className="h-full max-w-3xl mx-auto">
          <ChatInterface
            onSendMessage={handleSendMessage}
            messages={messages}
            isLoading={isLoading}
            streamingContent={streamingContent}
            onClear={handleClear}
          />
        </div>
      </div>
    </div>
  );
}
