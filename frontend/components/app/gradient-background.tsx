'use client';

import { cn } from '@/lib/utils';

interface GradientBackgroundProps {
  className?: string;
  intensity?: 'light' | 'medium' | 'strong';
}

export function GradientBackground({ className, intensity = 'medium' }: GradientBackgroundProps) {
  const intensityClass = {
    light: 'opacity-30 dark:opacity-15',
    medium: 'opacity-50 dark:opacity-30',
    strong: 'opacity-70 dark:opacity-45',
  };

  return (
    <div className={cn('gradient-bg', className)}>
      <div className={cn('floating-orb orb-1', intensityClass[intensity])} />
      <div className={cn('floating-orb orb-2', intensityClass[intensity])} />
      <div className={cn('floating-orb orb-3', intensityClass[intensity])} />
      <div className={cn('floating-orb orb-4', intensityClass[intensity])} />
    </div>
  );
}
