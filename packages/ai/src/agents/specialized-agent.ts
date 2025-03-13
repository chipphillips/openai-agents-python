import { z } from 'zod';
import { AgentType } from '@/packages/database';
import { SystemMessage, UserMessage } from 'ai';

export const agentInstructionsMap = {
  [AgentType.PRODUCT_MANAGER]: `You are an expert Product Manager specializing in construction software solutions. 
Your responsibility is to gather requirements, define user stories, and create product specifications.
Focus on understanding user needs and translating them into clear, actionable development tasks.`,

  [AgentType.SOFTWARE_ARCHITECT]: `You are an expert Software Architect with deep knowledge of modern web development.
Your responsibility is to design system architecture, select appropriate technologies, and ensure scalable, maintainable solutions.
Focus on creating robust technical designs that meet both functional and non-functional requirements.`,

  [AgentType.FRONTEND_DEVELOPER]: `You are an expert Frontend Developer specializing in Next.js 15, TypeScript, and Shadcn UI.
Your responsibility is to build beautiful, responsive user interfaces and client-side functionality.
Focus on writing clean, efficient code that follows best practices and delivers excellent user experiences.`,

  [AgentType.BACKEND_DEVELOPER]: `You are an expert Backend Developer specializing in Next.js API routes, Prisma ORM, and Supabase.
Your responsibility is to develop server-side logic, database interactions, and API endpoints.
Focus on creating secure, performant solutions that handle complex business logic.`,

  [AgentType.DEVOPS_ENGINEER]: `You are an expert DevOps Engineer specializing in CI/CD pipelines and cloud infrastructure.
Your responsibility is to streamline deployment processes and ensure optimal system performance.
Focus on automating workflows and implementing monitoring solutions.`,

  [AgentType.QA_TESTER]: `You are an expert QA Tester with a keen eye for detail and edge cases.
Your responsibility is to develop comprehensive test plans and ensure software quality.
Focus on identifying bugs, validating requirements, and improving the overall user experience.`,

  [AgentType.TECHNICAL_WRITER]: `You are an expert Technical Writer with excellent communication skills.
Your responsibility is to create clear, concise documentation for developers and end-users.
Focus on explaining complex concepts in accessible language and providing helpful examples.`,

  [AgentType.PROJECT_ORCHESTRATOR]: `You are the Project Orchestrator responsible for coordinating the AI development team.
Your responsibility is to manage the overall workflow, assign tasks to specialized agents, and ensure project success.
Focus on understanding requirements and effectively delegating to the most appropriate specialized agents.`
};

// Define the handoff keywords for each agent type
export const handoffKeywords = {
  [AgentType.PRODUCT_MANAGER]: ['requirements', 'user stories', 'product', 'feature', 'specification'],
  [AgentType.SOFTWARE_ARCHITECT]: ['architecture', 'design', 'system design', 'technical design', 'technology selection'],
  [AgentType.FRONTEND_DEVELOPER]: ['ui', 'frontend', 'interface', 'component', 'react', 'client-side'],
  [AgentType.BACKEND_DEVELOPER]: ['api', 'backend', 'database', 'server', 'endpoint', 'data model'],
  [AgentType.DEVOPS_ENGINEER]: ['deployment', 'ci/cd', 'infrastructure', 'pipeline', 'hosting', 'monitoring'],
  [AgentType.QA_TESTER]: ['testing', 'qa', 'quality', 'test plan', 'bug', 'validation'],
  [AgentType.TECHNICAL_WRITER]: ['documentation', 'docs', 'guide', 'tutorial', 'readme', 'explain'],
  [AgentType.PROJECT_ORCHESTRATOR]: ['coordinate', 'manage', 'overview', 'workflow', 'project', 'plan', 'schedule']
};

export interface AgentContext {
  projectId?: string;
  conversationHistory?: Message[];
  handoffContext?: string;
  environmentVariables?: Record<string, string>;
}

export interface Message {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

export class SpecializedAgent {
  private agentType: AgentType;
  private instructions: string;
  private conversationHistory: Message[] = [];
  private maxHistoryLength = 10;

  constructor(agentType: AgentType) {
    this.agentType = agentType;
    this.instructions = agentInstructionsMap[agentType];
  }

  /**
   * Get the agent type
   */
  getAgentType(): AgentType {
    return this.agentType;
  }

  /**
   * Set the conversation history
   */
  setConversationHistory(history: Message[]): void {
    this.conversationHistory = history.slice(-this.maxHistoryLength);
  }

  /**
   * Get the conversation history
   */
  getConversationHistory(): Message[] {
    return this.conversationHistory;
  }

  /**
   * Process a user query
   */
  async processQuery(query: string, context?: AgentContext): Promise<string> {
    // Initialize messages with system prompt
    const messages: (SystemMessage | UserMessage)[] = [
      { role: 'system', content: this.getSystemPrompt(context) }
    ];

    // Add conversation history if available
    if (context?.conversationHistory && context.conversationHistory.length > 0) {
      this.setConversationHistory(context.conversationHistory);
    }

    // Add conversation history to messages
    this.conversationHistory.forEach(message => {
      if (message.role === 'user') {
        messages.push({ role: 'user', content: message.content });
      } else if (message.role === 'assistant') {
        messages.push({ role: 'assistant', content: message.content });
      }
    });

    // Add handoff context if available
    if (context?.handoffContext) {
      messages.push({ 
        role: 'system', 
        content: `Previous agent provided this context: ${context.handoffContext}` 
      });
    }

    // Add the current query
    messages.push({ role: 'user', content: query });

    try {
      // Make API call to the language model
      const response = await fetch('/api/ai/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          messages,
          temperature: 0.7,
          model: 'gpt-4o', // Or the model of your choice
        }),
      });

      if (!response.ok) {
        throw new Error(`API response error: ${response.status}`);
      }

      const data = await response.json();
      const responseText = data.choices[0].message.content;

      // Update conversation history
      this.conversationHistory.push({ role: 'user', content: query });
      this.conversationHistory.push({ role: 'assistant', content: responseText });

      // Keep history within length limit
      if (this.conversationHistory.length > this.maxHistoryLength * 2) {
        this.conversationHistory = this.conversationHistory.slice(-this.maxHistoryLength * 2);
      }

      return responseText;
    } catch (error) {
      console.error('Error processing query:', error);
      return `Error processing your query. Please try again later. ${error.message}`;
    }
  }

  /**
   * Generate the system prompt for the agent
   */
  private getSystemPrompt(context?: AgentContext): string {
    let systemPrompt = this.instructions;

    // Add project context if available
    if (context?.projectId) {
      systemPrompt += `\n\nYou are working on project with ID: ${context.projectId}.`;
    }

    // Add environment variables as context if available
    if (context?.environmentVariables) {
      systemPrompt += `\n\nThe following environment information is available to you:`;
      
      for (const [key, value] of Object.entries(context.environmentVariables)) {
        systemPrompt += `\n- ${key}: ${value}`;
      }
    }

    systemPrompt += `\n\nWhen you need to handoff to another specialized agent, use the phrase "I'll handoff to the [AGENT_TYPE] to handle this."`;

    return systemPrompt;
  }

  /**
   * Check if the response contains a handoff phrase
   */
  checkForHandoff(response: string): AgentType | null {
    // Check for explicit handoff phrases
    const handoffRegex = /(?:I'll handoff to|I'll hand off to|Let me hand off to|Let's hand off to|Handing off to|This should be handled by) the (\w+\s?\w*) (?:agent|specialist|developer|engineer|manager|writer|tester|orchestrator|architect)/i;
    const match = response.match(handoffRegex);
    
    if (match && match[1]) {
      const agentTypeString = match[1].toUpperCase().replace(/\s/g, '_');
      
      // Try to match the extracted string to an AgentType
      for (const type of Object.values(AgentType)) {
        const typeString = type.toString().toUpperCase().replace(/\s/g, '_');
        
        if (typeString === agentTypeString || 
            typeString.includes(agentTypeString) || 
            agentTypeString.includes(typeString)) {
          return type as AgentType;
        }
      }
    }
    
    return null;
  }
} 