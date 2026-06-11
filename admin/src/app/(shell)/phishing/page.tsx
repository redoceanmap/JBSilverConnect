"use client";

import { useState } from "react";
import { ShieldAlert, Mic } from "lucide-react";
import { checkPhishing, type PhishingResult } from "@/lib/api";
import { useSpeechRecognition } from "@/lib/useSpeechRecognition";

// signal_color → 화면 색. 타입 분기 대신 매핑 테이블.
const palette: Record<string, { ring: string; text: string; bg: string; dot: string }> = {
  green: { ring: "border-safe", text: "text-safe", bg: "bg-safe/10", dot: "bg-safe" },
  yellow: { ring: "border-warning", text: "text-warning", bg: "bg-warning/10", dot: "bg-warning" },
  red: { ring: "border-danger", text: "text-danger", bg: "bg-danger/10", dot: "bg-danger" },
};
const fallbackTone = palette.yellow;

export default function PhishingPage() {
  const [message, setMessage] = useState("");
  const [result, setResult] = useState<PhishingResult | null>(null);
  const [loading, setLoading] = useState(false);

  const { supported: micSupported, listening, toggle } = useSpeechRecognition(
    (text) => setMessage((prev) => prev ? prev + " " + text : text),
  );

  async function check() {
    if (!message.trim() || loading) return;
    setLoading(true);
    try {
      setResult(await checkPhishing(message.trim()));
    } catch {
      setResult(null);
    } finally {
      setLoading(false);
    }
  }

  const tone = result ? palette[result.signal_color] ?? fallbackTone : fallbackTone;

  return (
    <div className="px-5 pb-8 pt-4">
      <span className="flex size-16 items-center justify-center rounded-2xl bg-gradient-to-b from-rose-300 to-rose-500 text-white shadow-sm">
        <ShieldAlert className="size-9" aria-hidden />
      </span>
      <h1 className="mt-4 text-3xl font-black text-slate-900">보이스피싱 확인</h1>
      <p className="mt-2 text-lg text-slate-600">
        받은 전화나 문자 내용을 적어 주세요. 위험한지 신호등 색으로 알려드려요.
      </p>

      <textarea
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        rows={4}
        placeholder="예: 검찰청인데요, 계좌가 범죄에 연루되어 지금 송금하셔야 합니다"
        className="mt-5 w-full resize-none rounded-2xl border border-slate-200 bg-white px-5 py-4 text-lg leading-relaxed text-slate-800 placeholder:text-slate-400 focus:border-jb-400"
      />
      {micSupported && (
        <button
          type="button"
          onClick={toggle}
          aria-label="음성으로 입력하기"
          className={`mt-2 flex w-full items-center justify-center gap-3 rounded-2xl border-2 py-4 text-lg font-bold transition active:scale-[0.98] ${
            listening
              ? "animate-pulse border-rose-300 bg-rose-50 text-rose-500"
              : "border-slate-200 bg-white text-slate-500"
          }`}
        >
          <Mic className="size-6" aria-hidden />
          {listening ? "듣는 중… (탭하면 멈춰요)" : "말로 입력하기"}
        </button>
      )}
      <button
        type="button"
        onClick={check}
        disabled={loading || !message.trim()}
        className="mt-3 w-full rounded-2xl bg-gradient-to-b from-jb-500 to-jb-700 px-6 py-5 text-xl font-bold text-white active:scale-[0.98] disabled:opacity-50"
      >
        {loading ? "확인하는 중…" : "위험한지 확인하기"}
      </button>

      {result && (
        <div className={`mt-6 rounded-3xl border-2 ${tone.ring} ${tone.bg} p-6`}>
          <div className="flex items-center gap-3">
            <span className={`size-5 rounded-full ${tone.dot}`} aria-hidden />
            <span className={`text-2xl font-black ${tone.text}`}>{result.risk_label}</span>
          </div>
          <p className="mt-4 text-lg leading-relaxed text-slate-800">{result.advice}</p>
          {result.alert_staff && (
            <p className="mt-4 rounded-2xl bg-white px-4 py-3 text-lg font-bold text-danger">
              ⚠️ 위험이 높아 은행 직원에게 함께 알렸어요.
            </p>
          )}
        </div>
      )}
    </div>
  );
}
