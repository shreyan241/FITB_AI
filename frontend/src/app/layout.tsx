import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { ThemeProvider } from "@/providers/theme";
import LandingNavbar from "@/components/navbar/LandingNavbar";
import "./globals.css";
import { Inter } from 'next/font/google';
import { Providers } from "./providers";
import { ReactScan } from "./react-scan";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: "Fries in the Bag AI - Automated Job Applications",
  description: "AI-powered job application assistant that helps you land your dream job faster.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <ReactScan />
      <body className={`${geistSans.variable} ${geistMono.variable} ${inter.className}`}>
        <Providers>
            <ThemeProvider>
              <LandingNavbar />
              <main style={{ 
                paddingTop: '64px',
                minHeight: '100vh',
                transition: 'background-color 0.3s ease-in-out'
              }}>
                {children}
              </main>
            </ThemeProvider>
        </Providers>
      </body>
    </html>
  );
}
