import type { Metadata } from "next";
import "./globals.css";
import { Inter } from "next/font/google";
import NPLogoMark from "@/components/NPLogoMark";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Klaviyo Audit | National Positions",
  description:
    "Free AI-powered Klaviyo email & SMS audit. Get your account score, critical findings, and a prioritized action plan in minutes.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <header className="bg-np-navy text-white">
          <div className="max-w-6xl mx-auto px-4 sm:px-6 py-3 flex items-center justify-between">
            {/* Logo lockup */}
            <a
              href="/"
              className="flex items-center gap-3 hover:opacity-90 transition-opacity"
            >
              <NPLogoMark size={36} variant="white" />
              <div className="flex flex-col leading-none">
                <span className="font-bold text-base tracking-wide text-white">
                  NATIONAL POSITIONS
                </span>
                <span className="text-[10px] tracking-[0.18em] text-np-gray uppercase mt-0.5">
                  Profitable Internet Marketing
                </span>
              </div>
            </a>

            {/* Right side */}
            <div className="flex items-center gap-4">
              <span className="text-np-gray text-xs hidden sm:block border border-np-gray/30 px-2 py-1 rounded-full">
                Klaviyo Audit Tool
              </span>
              <a
                href="https://www.nationalpositions.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-xs text-np-gray hover:text-white transition-colors hidden md:block"
              >
                nationalpositions.com ↗
              </a>
            </div>
          </div>
        </header>

        <main className="min-h-screen">{children}</main>

        <footer className="bg-np-navy py-8 mt-16">
          <div className="max-w-6xl mx-auto px-4 sm:px-6">
            <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
              {/* Footer logo */}
              <div className="flex items-center gap-3">
                <NPLogoMark size={28} variant="white" />
                <div className="flex flex-col leading-none">
                  <span className="font-bold text-sm tracking-wide text-white">
                    NATIONAL POSITIONS
                  </span>
                  <span className="text-[9px] tracking-[0.15em] text-np-gray uppercase mt-0.5">
                    Profitable Internet Marketing
                  </span>
                </div>
              </div>
              {/* Footer links / disclaimer */}
              <div className="text-center sm:text-right space-y-1">
                <p className="text-np-gray text-xs">
                  &copy; {new Date().getFullYear()} National Positions. All rights reserved.
                </p>
                <p className="text-np-gray/60 text-xs max-w-sm">
                  Audit results are diagnostic estimates only and are not
                  guarantees of performance.
                </p>
              </div>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
