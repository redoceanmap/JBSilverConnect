import type { Metadata } from "next";
import { Noto_Sans_KR } from "next/font/google";
import "./globals.css";

const notoSansKr = Noto_Sans_KR({
  variable: "--font-noto-sans-kr",
  subsets: ["latin"],
  weight: ["400", "500", "700", "900"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "JB AI Connect | 고객님을 위한 든든한 금융 도우미",
  description:
    "전북·광주은행 JB금융그룹의 AI 금융 서비스. 가까운 지점 찾기, 번호표 예약, 창업·법인 사무 안내까지 AI가 도와드립니다.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko" className={`${notoSansKr.variable} h-full antialiased`}>
      <body className="min-h-dvh bg-slate-300 font-sans">
        {/* 모바일 앱 셸 — 데스크톱에서도 폰 폭으로 고정 */}
        <div className="relative mx-auto min-h-dvh max-w-[480px] overflow-hidden shadow-2xl">
          {children}
        </div>
      </body>
    </html>
  );
}
