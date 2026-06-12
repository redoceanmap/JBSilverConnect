"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { BellRing, Wifi, WifiOff, Building2, Armchair } from "lucide-react";
import { listCalledEntries, type CallCard, type WindowType } from "@/lib/api";

const POLL_MS = 2000;

// 창구 종류 → 창구 번호/이름. 일반=1번 창구, 법인 사무=2번 창구.
function windowNumber(windowType: WindowType): string {
  return windowType === "corporate" ? "2" : "1";
}
function windowName(windowType: WindowType): string {
  return windowType === "corporate" ? "법인 사무 창구" : "일반 창구";
}

export default function DisplayPage() {
  const [calls, setCalls] = useState<CallCard[]>([]);
  const [online, setOnline] = useState(true);
  const [loaded, setLoaded] = useState(false);
  const aliveRef = useRef(true);

  const poll = useCallback(async () => {
    try {
      const next = await listCalledEntries();
      if (!aliveRef.current) return;
      setCalls(next);
      setOnline(true);
      setLoaded(true);
    } catch {
      if (!aliveRef.current) return;
      setOnline(false);
      setLoaded(true);
    }
  }, []);

  useEffect(() => {
    aliveRef.current = true;
    const kick = setTimeout(() => void poll(), 0);
    const id = setInterval(() => void poll(), POLL_MS);
    return () => {
      aliveRef.current = false;
      clearTimeout(kick);
      clearInterval(id);
    };
  }, [poll]);

  const latest = calls[0];
  const rest = calls.slice(1);

  return (
    <div className="flex min-h-dvh flex-col bg-gradient-to-b from-jb-700 via-jb-800 to-jb-900 text-white">
      {/* 헤더 */}
      <header className="flex items-center gap-3 px-8 py-6">
        <span className="flex size-12 items-center justify-center rounded-xl bg-white text-base font-black text-jb-700">
          JB
        </span>
        <div>
          <h1 className="text-2xl font-black">고객 호출 안내</h1>
          <p className="text-sm text-white/60">JB AI Connect</p>
        </div>
        <span
          className={`ml-auto flex items-center gap-1.5 text-sm font-bold ${
            online ? "text-emerald-300" : "text-rose-300"
          }`}
        >
          {online ? (
            <Wifi className="size-4" aria-hidden />
          ) : (
            <WifiOff className="size-4" aria-hidden />
          )}
          {online ? "실시간 연결" : "연결 끊김"}
        </span>
      </header>

      {/* 본문 */}
      <main className="flex flex-1 flex-col items-center justify-center px-6 pb-12">
        {loaded && calls.length === 0 && (
          <div className="flex flex-col items-center gap-4 text-center text-white/50">
            <Armchair className="size-20" aria-hidden />
            <p className="text-3xl font-bold">호출을 기다리고 있습니다</p>
            <p className="text-lg">창구에서 호출하면 번호가 여기에 표시됩니다.</p>
          </div>
        )}

        {latest && (
          <article
            key={latest.handoff_id}
            className="call-in call-pulse w-full max-w-3xl rounded-[2.5rem] bg-white px-10 py-14 text-center text-jb-900 shadow-2xl"
          >
            <p className="flex items-center justify-center gap-3 text-2xl font-bold text-jb-500">
              <BellRing className="size-8" aria-hidden />
              지금 호출
            </p>
            <p className="mt-6 text-[7rem] font-black leading-none text-jb-700">
              {latest.ticket_label}
              <span className="text-5xl">번 고객님</span>
            </p>
            <p className="mt-8 inline-flex items-center gap-3 rounded-full bg-jb-50 px-8 py-4 text-4xl font-black text-jb-700">
              {latest.window_type === "corporate" && (
                <Building2 className="size-9 shrink-0" aria-hidden />
              )}
              {windowNumber(latest.window_type)}번 창구로 오세요
            </p>
            <p className="mt-4 text-xl font-bold text-slate-500">
              {windowName(latest.window_type)} · {latest.customer_name} 고객님
            </p>
          </article>
        )}

        {rest.length > 0 && (
          <div className="mt-8 grid w-full max-w-4xl grid-cols-2 gap-4 md:grid-cols-3">
            {rest.map((call) => (
              <div
                key={call.handoff_id}
                className="call-in rounded-2xl bg-white/10 px-5 py-4 text-center backdrop-blur"
              >
                <p className="text-3xl font-black">{call.ticket_label}번 고객님</p>
                <p className="mt-1 text-lg font-bold text-white/80">
                  {windowNumber(call.window_type)}번 창구로 오세요
                </p>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
