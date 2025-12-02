export interface AppConfig {
  pageTitle: string;
  pageDescription: string;
  companyName: string;

  supportsChatInput: boolean;
  supportsVideoInput: boolean;
  supportsScreenShare: boolean;
  isPreConnectBufferEnabled: boolean;

  logo: string;
  startButtonText: string;
  accent?: string;
  logoDark?: string;
  accentDark?: string;

  // for LiveKit Cloud Sandbox
  sandboxId?: string;
  agentName?: string;
}

export const APP_CONFIG_DEFAULTS: AppConfig = {
  companyName: 'Maya SDR',
  pageTitle: 'Maya | AI Sales Development Representative',
  pageDescription: 'Experience the future of B2B sales with Maya, your AI-powered Sales Development Representative',

  supportsChatInput: true,
  supportsVideoInput: false,
  supportsScreenShare: false,
  isPreConnectBufferEnabled: true,

  logo: '/lk-logo.svg',
  accent: '#6366f1',
  logoDark: '/lk-logo-dark.svg',
  accentDark: '#818cf8',
  startButtonText: 'Connect with Maya',

  // for LiveKit Cloud Sandbox
  sandboxId: undefined,
  agentName: 'MAYA',
};
