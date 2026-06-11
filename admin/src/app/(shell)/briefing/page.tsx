"use client";

import { useEffect, useState } from "react";
import { Sun, Volume2 } from "lucide-react";
import { getDailyBriefing, type Briefing } from "@/lib/api";

const today = new Date().toLocaleDateString("ko-KR", {
  month: "long",
  day: "numeric",
  weekday: "long",
});

export default function BriefingPage() {
  const [data, setData] = useState<Briefing | null>(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    getDailyBriefing().then(setData).catch(() => setError(true));
  }, []);

  function speak() {
    if (!data || typeof window === "undefined" || !window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    const utter = new SpeechSynthesisUtterance(data.spoken_text);
    utter.lang = "ko-KR";
    utter.rate = 0.95;
    window.speechSynthesis.speak(utter);
  }

  return (
    <div className="px-5 pb-8 pt-4">
      <span className="flex size-16 items-center justify-center rounded-2xl bg-gradient-to-b from-amber-300 to-amber-500 text-white shadow-sm">
        <Sun className="size-9" aria-hidden />
      </span>
      <h1 className="mt-4 text-3xl font-black text-slate-900">오늘의 안심 브리핑</h1>
      <p className="mt-2 text-lg text-slate-600">{today}</p>

      {error && (
        <p className="mt-6 rounded-2xl bg-danger/10 px-5 py-4 text-lg font-semibold text-danger">
          브리핑을 불러오지 못했어요.
        </p>
      )}

      {!data && !error && (
        <p className="mt-6 text-lg text-slate-500">브리핑을 준비하고 있어요…</p>
      )}

      {data && (
        <div className="mt-6 space-y-4">
          <div className="grid grid-cols-2 gap-3">
            <div className="card rounded-3xl p-5">
              <p className="text-base text-slate-500">오늘 잔액</p>
              <p className="mt-1 text-2xl font-black text-jb-700">
                {data.balance.toLocaleString("ko-KR")}원
              </p>
            </div>
            <div className="card rounded-3xl p-5">
              <p className="text-base text-slate-500">날씨</p>
              <p className="mt-1 text-2xl font-black text-slate-900">
                {data.temperature}° {data.weather_description}
              </p>
            </div>
          </div>

          <div className="rounded-3xl border border-jb-100 bg-jb-50 px-5 py-5">
            <p className="text-xl font-medium leading-relaxed text-jb-800">
              {data.spoken_text}
            </p>
          </div>

          <button
            type="button"
            onClick={speak}
            className="flex w-full items-center justify-center gap-2 rounded-2xl bg-gradient-to-b from-jb-500 to-jb-700 px-6 py-5 text-xl font-bold text-white active:scale-[0.98]"
          >
            <Volume2 className="size-7" aria-hidden />
            음성으로 들려주세요
          </button>
        </div>
      )}
    </div>
  );
}
