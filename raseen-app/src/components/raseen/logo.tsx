import { cn } from "@/lib/utils";

// new identity (Nov 24): dot + broadcast waves; files live in public/brand
export const raseenLogoUrl = "/brand/raseen-logo-navy.png";

export function RaseenMark({
  className,
  invert = false,
}: {
  className?: string;
  invert?: boolean;
}) {
  return (
    <span
      aria-hidden="true"
      className={cn("grid size-9 shrink-0 place-items-center p-1", className)}
    >
      <img
        src={invert ? "/brand/raseen-mark-white.png" : "/brand/raseen-mark-navy.png"}
        alt=""
        className="h-full w-full object-contain"
      />
    </span>
  );
}

export function RaseenLogo({
  className,
  invert = false,
}: {
  className?: string;
  /** kept for API compatibility; the logo carries the brand name itself */
  showTagline?: boolean;
  invert?: boolean;
}) {
  return (
    <div className={cn("flex min-w-0 items-center px-1 py-1.5", className)}>
      <img
        src={invert ? "/brand/raseen-logo-white.png" : "/brand/raseen-logo-navy.png"}
        alt="رسين Raseen"
        className="h-9 w-auto max-w-full object-contain object-right"
      />
    </div>
  );
}
