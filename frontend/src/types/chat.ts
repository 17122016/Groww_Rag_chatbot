export interface Message {
    role: 'user' | 'assistant';
    content: string;
    source_link?: string;
    footer?: string;
}

export interface ChatResponse {
    answer: string;
    source_link: string;
    footer: string;
}
