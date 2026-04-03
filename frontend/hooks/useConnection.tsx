'use client';

import { createContext, useContext, useMemo, useState } from 'react';
import { TokenSource } from 'livekit-client';
import { SessionProvider, useSession } from '@livekit/components-react';
import type { AppConfig } from '@/app-config';

type ConnectionDetails = {
  serverUrl: string;
  roomName: string;
  participantName: string;
  participantToken: string;
};

const CONNECTION_DETAILS_ENDPOINT = '/api/connection-details';

function isConnectionDetails(value: unknown): value is ConnectionDetails {
  if (!value || typeof value !== 'object') {
    return false;
  }

  const payload = value as Record<string, unknown>;
  return (
    typeof payload.serverUrl === 'string' &&
    typeof payload.roomName === 'string' &&
    typeof payload.participantName === 'string' &&
    typeof payload.participantToken === 'string'
  );
}

async function fetchConnectionDetails(endpoint: string, appConfig: AppConfig): Promise<ConnectionDetails> {
  const url = new URL(endpoint, window.location.origin);
  const response = await fetch(url.toString(), {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Sandbox-Id': appConfig.sandboxId ?? '',
    },
    body: JSON.stringify({
      room_config: appConfig.agentName
        ? {
            agents: [{ agent_name: appConfig.agentName }],
          }
        : undefined,
    }),
  });

  if (!response.ok) {
    const details = await response.text();
    throw new Error(`Connection details request failed (${response.status}): ${details}`);
  }

  const payload: unknown = await response.json();
  if (!isConnectionDetails(payload)) {
    throw new Error('Invalid connection details payload');
  }

  return payload;
}

interface ConnectionContextType {
  isConnectionActive: boolean;
  connect: (startSession?: boolean) => void;
  startDisconnectTransition: () => void;
  onDisconnectTransitionComplete: () => void;
}

const ConnectionContext = createContext<ConnectionContextType>({
  isConnectionActive: false,
  connect: () => {},
  startDisconnectTransition: () => {},
  onDisconnectTransitionComplete: () => {},
});

export function useConnection() {
  const ctx = useContext(ConnectionContext);
  if (!ctx) {
    throw new Error('useConnection must be used within a ConnectionProvider');
  }
  return ctx;
}

interface ConnectionProviderProps {
  appConfig: AppConfig;
  children: React.ReactNode;
}

export function ConnectionProvider({ appConfig, children }: ConnectionProviderProps) {
  const [isConnectionActive, setIsConnectionActive] = useState(false);
  const [isConnecting, setIsConnecting] = useState(false);

  const tokenSource = useMemo(() => {
    const customConnectionEndpoint = process.env.NEXT_PUBLIC_CONN_DETAILS_ENDPOINT?.trim();

    return TokenSource.custom(async () => {
      if (customConnectionEndpoint) {
        try {
          return await fetchConnectionDetails(customConnectionEndpoint, appConfig);
        } catch (error) {
          console.error(
            `Custom connection-details endpoint failed (${customConnectionEndpoint}). Falling back to ${CONNECTION_DETAILS_ENDPOINT}.`,
            error
          );
        }
      }

      return fetchConnectionDetails(CONNECTION_DETAILS_ENDPOINT, appConfig);
    });
  }, [appConfig]);

  const session = useSession(
    tokenSource,
    appConfig.agentName ? { agentName: appConfig.agentName } : undefined
  );

  const { start: startSession, end: endSession } = session;

  const value = useMemo(() => {
    return {
      isConnectionActive,
      connect: () => {
        if (isConnectionActive || isConnecting) {
          return;
        }

        setIsConnecting(true);
        setIsConnectionActive(true);

        Promise.resolve(startSession())
          .catch((error) => {
            console.error('Failed to start LiveKit session:', error);
            setIsConnectionActive(false);
          })
          .finally(() => {
            setIsConnecting(false);
          });
      },
      startDisconnectTransition: () => {
        setIsConnectionActive(false);
      },
      onDisconnectTransitionComplete: () => {
        setIsConnecting(false);
        endSession();
      },
    };
  }, [startSession, endSession, isConnectionActive, isConnecting]);

  return (
    <SessionProvider session={session}>
      <ConnectionContext.Provider value={value}>{children}</ConnectionContext.Provider>
    </SessionProvider>
  );
}
