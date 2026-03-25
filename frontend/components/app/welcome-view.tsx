import { GradientBackground } from '@/components/app/gradient-background';
import { Button } from '@/components/livekit/button';

function MayaAvatar() {
  return (
    <div className="relative mb-8">
      {/* Outer glow ring */}
      <div className="from-primary/40 via-accent/30 to-primary/40 absolute inset-0 scale-110 animate-pulse rounded-full bg-gradient-to-br blur-xl" />

      {/* Avatar container */}
      <div className="glass-card glow-primary relative rounded-full p-1">
        <div className="from-primary via-accent to-primary relative size-28 rounded-full bg-gradient-to-br p-[2px]">
          <div className="bg-background flex size-full items-center justify-center rounded-full">
            {/* Voice wave icon */}
            <svg
              width="48"
              height="48"
              viewBox="0 0 64 64"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
              className="text-primary"
            >
              <path
                d="M15 24V40C15 40.7957 14.6839 41.5587 14.1213 42.1213C13.5587 42.6839 12.7956 43 12 43C11.2044 43 10.4413 42.6839 9.87868 42.1213C9.31607 41.5587 9 40.7957 9 40V24C9 23.2044 9.31607 22.4413 9.87868 21.8787C10.4413 21.3161 11.2044 21 12 21C12.7956 21 13.5587 21.3161 14.1213 21.8787C14.6839 22.4413 15 23.2044 15 24ZM22 5C21.2044 5 20.4413 5.31607 19.8787 5.87868C19.3161 6.44129 19 7.20435 19 8V56C19 56.7957 19.3161 57.5587 19.8787 58.1213C20.4413 58.6839 21.2044 59 22 59C22.7956 59 23.5587 58.6839 24.1213 58.1213C24.6839 57.5587 25 56.7957 25 56V8C25 7.20435 24.6839 6.44129 24.1213 5.87868C23.5587 5.31607 22.7956 5 22 5ZM32 13C31.2044 13 30.4413 13.3161 29.8787 13.8787C29.3161 14.4413 29 15.2044 29 16V48C29 48.7957 29.3161 49.5587 29.8787 50.1213C30.4413 50.6839 31.2044 51 32 51C32.7956 51 33.5587 50.6839 34.1213 50.1213C34.6839 49.5587 35 48.7957 35 48V16C35 15.2044 34.6839 14.4413 34.1213 13.8787C33.5587 13.3161 32.7956 13 32 13ZM42 21C41.2043 21 40.4413 21.3161 39.8787 21.8787C39.3161 22.4413 39 23.2044 39 24V40C39 40.7957 39.3161 41.5587 39.8787 42.1213C40.4413 42.6839 41.2043 43 42 43C42.7957 43 43.5587 42.6839 44.1213 42.1213C44.6839 41.5587 45 40.7957 45 40V24C45 23.2044 44.6839 22.4413 44.1213 21.8787C43.5587 21.3161 42.7957 21 42 21ZM52 17C51.2043 17 50.4413 17.3161 49.8787 17.8787C49.3161 18.4413 49 19.2044 49 20V44C49 44.7957 49.3161 45.5587 49.8787 46.1213C50.4413 46.6839 51.2043 47 52 47C52.7957 47 53.5587 46.6839 54.1213 46.1213C54.6839 45.5587 55 44.7957 55 44V20C55 19.2044 54.6839 18.4413 54.1213 17.8787C53.5587 17.3161 52.7957 17 52 17Z"
                fill="currentColor"
              />
            </svg>
          </div>
        </div>
      </div>
    </div>
  );
}

function FeatureTag({ children }: { children: React.ReactNode }) {
  return (
    <span className="bg-primary/10 text-primary dark:bg-primary/20 inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-medium">
      <span className="bg-primary size-1.5 animate-pulse rounded-full" />
      {children}
    </span>
  );
}

interface WelcomeViewProps {
  startButtonText: string;
  onStartCall: () => void;
}

export const WelcomeView = ({
  startButtonText,
  onStartCall,
  ref,
}: React.ComponentProps<'div'> & WelcomeViewProps) => {
  return (
    <div ref={ref} className="relative min-h-svh">
      {/* Gradient Background */}
      <GradientBackground intensity="medium" />

      {/* Main Content */}
      <section className="relative z-10 flex min-h-svh flex-col items-center justify-center px-4 text-center">
        {/* Badge */}
        <div className="mb-6 flex flex-wrap items-center justify-center gap-2">
          <FeatureTag>AI-Powered</FeatureTag>
          <FeatureTag>24/7 Available</FeatureTag>
          <FeatureTag>B2B Expert</FeatureTag>
        </div>

        {/* Avatar */}
        <MayaAvatar />

        {/* Title */}
        <h1 className="from-foreground via-foreground/90 to-foreground/70 mb-3 bg-gradient-to-br bg-clip-text text-4xl font-bold tracking-tight text-transparent md:text-5xl lg:text-6xl">
          Meet Maya
        </h1>

        <p className="text-primary mb-2 text-lg font-medium md:text-xl">
          Your AI Sales Development Representative
        </p>

        <p className="text-muted-foreground mb-8 max-w-md leading-relaxed md:max-w-lg">
          Experience the future of B2B sales. Maya helps you explore cloud solutions, discuss
          scalability, and discover how we can solve your business challenges.
        </p>

        {/* CTA Button */}
        <Button
          variant="primary"
          size="lg"
          onClick={onStartCall}
          className="group from-primary via-primary to-accent pulse-glow relative min-w-64 overflow-hidden bg-gradient-to-r px-8 py-6 text-base font-semibold tracking-wide transition-all duration-300 hover:scale-[1.02] hover:shadow-2xl"
        >
          <span className="relative z-10 flex items-center gap-2">
            <svg
              className="size-5 transition-transform duration-300 group-hover:scale-110"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"
              />
            </svg>
            {startButtonText}
          </span>
        </Button>

        {/* Trust indicators */}
        <div className="mt-10 flex flex-col items-center gap-4">
          <div className="text-muted-foreground flex items-center gap-6 text-xs">
            <span className="flex items-center gap-1.5">
              <svg className="size-4 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                  clipRule="evenodd"
                />
              </svg>
              No credit card required
            </span>
            <span className="flex items-center gap-1.5">
              <svg className="size-4 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                  clipRule="evenodd"
                />
              </svg>
              Instant connection
            </span>
            <span className="flex items-center gap-1.5">
              <svg className="size-4 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                  clipRule="evenodd"
                />
              </svg>
              Enterprise-ready
            </span>
          </div>
        </div>
      </section>

      {/* Footer */}
      <div className="fixed bottom-5 left-0 z-10 flex w-full flex-col items-center justify-center gap-2 px-4">
        <p className="glass-card text-muted-foreground rounded-full px-4 py-2 text-center text-xs leading-5 md:text-sm">
          Powered by advanced AI • Your conversation is private and secure
        </p>
        <p className="text-muted-foreground/70 text-xs">Made by Swarnodip Nag with ❤️</p>
      </div>
    </div>
  );
};
