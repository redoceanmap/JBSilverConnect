import Link from "next/link";
import { Mic, Ticket, MapPin } from "lucide-react";
import { Mascot } from "@/components/Mascot";

const todayLabel = new Date().toLocaleDateString("ko-KR", {
  year: "numeric",
  month: "long",
  day: "numeric",
  weekday: "long",
});

export default function Home() {
  return (
    <div className="px-5 pb-6 pt-4">
      {/* 인사 */}
      <p className="text-base font-medium text-slate-500">{todayLabel}</p>
      <h1 className="mt-1 text-3xl font-black text-slate-900">
        안녕하세요, <span className="text-jb-700">고객님</span> 😊
      </h1>

      {/* 마스코트 히어로 — 탭하면 대화형 AI */}
      <Link
        href="/chat"
        aria-label="도우미와 대화 시작하기"
        className="relative mt-5 block overflow-hidden rounded-[28px] border border-jb-100 bg-gradient-to-b from-jb-50 to-white p-6 shadow-[0_12px_32px_-12px_rgba(20,50,110,0.2)] transition active:scale-[0.99]"
      >
        <p className="text-lg font-bold text-jb-700">AI 도우미</p>

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

      {/* 빠른 실행 — 예약 / 지점 */}
      <div className="mt-4 grid grid-cols-2 gap-3">
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

        <Link
          href="/branch"
          className="card flex flex-col gap-3 rounded-3xl p-5 transition active:scale-[0.98]"
        >
          <span className="flex size-14 items-center justify-center rounded-2xl bg-gradient-to-b from-emerald-400 to-emerald-600 text-white shadow-sm">
            <MapPin className="size-8" aria-hidden />
          </span>
          <span className="text-xl font-bold leading-tight text-slate-900">
            가까운
            <br />
            지점 찾기
          </span>
        </Link>
      </div>
    </div>
  );
}
