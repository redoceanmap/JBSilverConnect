import { Header } from "@/components/Header";
import { BottomNav } from "@/components/BottomNav";

export default function ShellLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <div className="relative flex min-h-dvh flex-col bg-gradient-to-b from-sky-100 via-white to-rose-50">
      {/* 리퀴드 글래스용 배경 컬러 블롭 */}
      <div className="pointer-events-none absolute -left-20 -top-16 size-72 rounded-full bg-jb-300/40 blur-3xl" />
      <div className="pointer-events-none absolute -right-24 top-44 size-72 rounded-full bg-sky-300/40 blur-3xl" />
      <div className="pointer-events-none absolute -bottom-10 left-10 size-72 rounded-full bg-rose-200/40 blur-3xl" />

      <div className="relative flex min-h-dvh flex-col">
        <Header />
        <main className="flex-1">{children}</main>
        <BottomNav />
      </div>
    </div>
  );
}
