import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Kenya Airways Reviews",
  description:
    "Positive, negative, and neutral reviews of Kenya Airways collected from google, x,facebook, tripadvisor and airlineratings.com",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="max-w-6xl p-5 m-auto bg-secondary  bg-opacity-5">
          {children}
        </div>
      </body>
    </html>
  );
}
