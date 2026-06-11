"use client";

import { useState } from "react";
import { PiggyBank, Sparkles } from "lucide-react";
import { proposeSavings, type SavingsProposal } from "@/lib/api";

export default function SavingsPage() {
  const [data, setData] = useState<SavingsProposal | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(false);
  const [done, setDone] = useState<string | null>(null);

  async function load() {
    setLoading(true);
    setError(false);
    try {
      setData(await proposeSavings());
    } catch {
      setError(true);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="px-5 pb-8 pt-4">
      <span className="flex size-16 items-center justify-center rounded-2xl bg-gradient-to-b from-amber-300 to-amber-500 text-white shadow-sm">
        <PiggyBank className="size-9" aria-hidden />
      </span>
      <h1 className="mt-4 text-3xl font-black text-slate-900">여윳돈 적금 제안</h1>
      <p className="mt-2 text-lg text-slate-600">
        통장에 잠자는 여윳돈을 찾아 AI가 알맞은 적금을 제안해 드려요.
      </p>

      {!data && (
        <button
          type="button"
          onClick={load}
          disabled={loading}
          className="mt-6 flex w-full items-center justify-center gap-2 rounded-2xl bg-gradient-to-b from-jb-500 to-jb-700 px-6 py-5 text-xl font-bold text-white shadow-[0_10px_24px_-8px_rgba(0,56,118,0.6)] active:scale-[0.98] disabled:opacity-60"
        >
          <Sparkles className="size-6" aria-hidden />
          {loading ? "여윳돈을 찾는 중…" : "내 여윳돈 확인하기"}
        </button>
      )}

      {error && (
        <p className="mt-6 rounded-2xl bg-danger/10 px-5 py-4 text-lg font-semibold text-danger">
          불러오지 못했어요. 잠시 후 다시 시도해 주세요.
        </p>
      )}

      {data && (
        <div className="mt-6 space-y-4">
          <div className="card rounded-3xl p-6">
            <p className="text-lg text-slate-500">잠자는 여윳돈</p>
            <p className="mt-1 text-4xl font-black text-jb-700">
              {data.idle_amount.toLocaleString("ko-KR")}원
            </p>
            <div className="mt-4 flex items-baseline justify-between border-t border-slate-100 pt-4">
              <span className="text-lg text-slate-600">예상 월 이자</span>
              <span className="text-2xl font-bold text-safe">
                +{data.monthly_interest.toLocaleString("ko-KR")}원
              </span>
            </div>
            <div className="mt-2 flex items-baseline justify-between">
              <span className="text-lg text-slate-600">적용 금리</span>
              <span className="text-xl font-bold text-slate-800">연 {data.rate}%</span>
            </div>
          </div>

          <div className="rounded-3xl border border-jb-100 bg-jb-50 px-5 py-4">
            <p className="text-lg font-medium leading-relaxed text-jb-800">
              💬 {data.ai_message}
            </p>
          </div>

          {done ? (
            <p className="rounded-2xl bg-safe/10 px-5 py-4 text-center text-lg font-bold text-safe">
              {done}
            </p>
          ) : (
            <div className="grid grid-cols-2 gap-3">
              <button
                type="button"
                onClick={() => setDone("좋아요! 직원이 도와드릴 거예요 😊")}
                className="rounded-2xl bg-gradient-to-b from-jb-500 to-jb-700 px-5 py-5 text-xl font-bold text-white active:scale-[0.98]"
              >
                {data.agree_label}
              </button>
              <button
                type="button"
                onClick={() => setDone("알겠어요. 다음에 또 도와드릴게요.")}
                className="rounded-2xl bg-slate-100 px-5 py-5 text-xl font-bold text-slate-600 active:scale-[0.98]"
              >
                {data.reject_label}
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
