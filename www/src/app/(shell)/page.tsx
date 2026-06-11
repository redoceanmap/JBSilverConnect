import Link from "next/link";
import { Mic, ChevronRight, Sun, Ticket } from "lucide-react";
import { Mascot } from "@/components/Mascot";
import { features } from "@/lib/features";

const todayLabel = new Date().toLocaleDateString("ko-KR", {
  year: "numeric",
  month: "long",
  day: "numeric",
  weekday: "long",
});

// 가로 스와이프 카드용 아이콘 칩 톤 (기능별 색)
const tints: Record<string, string> = {
  savings: "from-amber-300 to-amber-500",
  phishing: "from-rose-300 to-rose-500",
  branch: "from-emerald-300 to-emerald-500",
  report: "from-violet-300 to-violet-500",
};

const carousel = features.filter((f) =>
  ["savings", "phishing", "branch", "report"].includes(f.slug),
);

export default function Home() {
  return (
    <div className="px-5 pb-6 pt-4">
      {/* 인사 */}
      <p className="text-base font-medium text-slate-500">{todayLabel}</p>
      <h1 className="mt-1 text-3xl font-black text-slate-900">
        안녕하세요, <span className="text-jb-700">어르신</span> 😊
      </h1>

      {/* 마스코트 히어로 — 탭하면 대화형 AI */}
      <Link
        href="/chat"
        aria-label="도우미와 대화 시작하기"
        className="relative mt-5 block overflow-hidden rounded-[28px] border border-jb-100 bg-gradient-to-b from-jb-50 to-white p-6 shadow-[0_12px_32px_-12px_rgba(20,50,110,0.2)] transition active:scale-[0.99]"
      >
        <p className="text-lg font-bold text-jb-700">JB 도우미</p>

        <div className="mt-3 flex items-end gap-2">
          <div className="mb-5 max-w-[58%] rounded-3xl rounded-bl-md border border-slate-100 bg-white px-4 py-3 shadow-sm">
            <p className="text-lg font-semibold leading-snug text-slate-800">
              무엇을 도와드릴까요?
              <br />
              저를 누르고 말씀해 보세요.
            </p>
          </div>
          <Mascot className="ml-auto h-40 w-40 shrink-0 drop-shadow-xl" />
        </div>

        <span className="flex items-center justify-center gap-2 rounded-2xl bg-gradient-to-b from-jb-500 to-jb-700 px-5 py-4 text-xl font-bold text-white shadow-[0_8px_20px_-6px_rgba(0,56,118,0.6)]">
          <Mic className="size-6" aria-hidden />
          눌러서 대화 시작하기
        </span>
      </Link>

      {/* 빠른 실행 — 브리핑 / 예약 */}
      <div className="mt-4 grid grid-cols-2 gap-3">
        <Link
          href="/briefing"
          className="card flex flex-col gap-3 rounded-3xl p-5 transition active:scale-[0.98]"
        >
          <span className="flex size-14 items-center justify-center rounded-2xl bg-gradient-to-b from-amber-300 to-amber-500 text-white shadow-sm">
            <Sun className="size-8" aria-hidden />
          </span>
          <span className="text-xl font-bold leading-tight text-slate-900">
            오늘의
            <br />
            안심 브리핑
          </span>
        </Link>

        <Link
          href="/reservation"
          className="card flex flex-col gap-3 rounded-3xl p-5 transition active:scale-[0.98]"
        >
          <span className="flex size-14 items-center justify-center rounded-2xl bg-gradient-to-b from-jb-400 to-jb-700 text-white shadow-sm">
            <Ticket className="size-8" aria-hidden />
          </span>
          <span className="text-xl font-bold leading-tight text-slate-900">
            지점
            <br />
            번호표 예약
          </span>
        </Link>
      </div>

      {/* 가로 스와이프 — 그 밖의 기능 */}
      <div className="mt-7">
        <h2 className="text-2xl font-black text-slate-900">
          이런 것도 할 수 있어요
        </h2>
        <p className="mt-1 text-base text-slate-500">옆으로 넘겨서 보세요 →</p>

        <ul className="no-scrollbar mt-4 flex snap-x snap-mandatory gap-4 overflow-x-auto pb-2 [scroll-padding-left:1.25rem]">
          {carousel.map((f) => (
            <li key={f.slug} className="w-[76%] shrink-0 snap-start">
              <Link
                href={f.href}
                className="card flex h-full flex-col rounded-3xl p-6 transition active:scale-[0.98]"
              >
                <span
                  className={`flex size-16 items-center justify-center rounded-2xl bg-gradient-to-b text-white shadow-sm ${tints[f.slug]}`}
                >
                  <f.icon className="size-9" aria-hidden />
                </span>
                <span className="mt-4 text-2xl font-bold text-slate-900">
                  {f.title}
                </span>
                <span className="mt-2 flex-1 text-lg leading-relaxed text-slate-600">
                  {f.description}
                </span>
                <span className="mt-4 inline-flex items-center gap-1 text-lg font-bold text-jb-600">
                  바로 가기
                  <ChevronRight className="size-5" aria-hidden />
                </span>
              </Link>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
