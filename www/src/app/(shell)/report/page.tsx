"use client";

import { useEffect, useState } from "react";
import { LineChart, Flame } from "lucide-react";
import { getInterestReport, type InterestReport } from "@/lib/api";

export default function ReportPage() {
  const [data, setData] = useState<InterestReport | null>(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    getInterestReport().then(setData).catch(() => setError(true));
  }, []);

  const max =
    data && data.monthly.length > 0
      ? Math.max(...data.monthly.map((m) => m.amount))
      : 1;

  return (
    <div className="px-5 pb-8 pt-4">
      <span className="flex size-16 items-center justify-center rounded-2xl bg-gradient-to-b from-violet-300 to-violet-500 text-white shadow-sm">
        <LineChart className="size-9" aria-hidden />
      </span>
      <h1 className="mt-4 text-3xl font-black text-slate-900">이자 리포트</h1>
      <p className="mt-2 text-lg text-slate-600">
        그동안 받은 이자와 연속으로 이자가 들어온 개월을 정리해 드려요.
      </p>

      {error && (
        <p className="mt-6 rounded-2xl bg-danger/10 px-5 py-4 text-lg font-semibold text-danger">
          리포트를 불러오지 못했어요.
        </p>
      )}

      {!data && !error && (
        <p className="mt-6 text-lg text-slate-500">리포트를 준비하고 있어요…</p>
      )}

      {data && (
        <div className="mt-6 space-y-4">
          <div className="grid grid-cols-2 gap-3">
            <div className="card rounded-3xl p-5">
              <p className="text-base text-slate-500">받은 이자 합계</p>
              <p className="mt-1 text-2xl font-black text-jb-700">
                {data.total_interest.toLocaleString("ko-KR")}원
              </p>
            </div>
            <div className="card flex flex-col rounded-3xl p-5">
              <p className="text-base text-slate-500">연속 이자</p>
              <p className="mt-1 flex items-center gap-1 text-2xl font-black text-warning">
                <Flame className="size-6" aria-hidden />
                {data.streak_months}개월
              </p>
            </div>
          </div>

          <div className="card rounded-3xl p-6">
            <p className="text-lg font-bold text-slate-800">월별 이자</p>
            <ul className="mt-4 space-y-3">
              {data.monthly.map((m) => (
                <li key={m.month} className="flex items-center gap-3">
                  <span className="w-14 shrink-0 text-base text-slate-500">{m.month}</span>
                  <span className="h-3 flex-1 overflow-hidden rounded-full bg-slate-100">
                    <span
                      className="block h-full rounded-full bg-gradient-to-r from-jb-400 to-jb-600"
                      style={{ width: `${Math.max(8, (m.amount / max) * 100)}%` }}
                    />
                  </span>
                  <span className="w-20 shrink-0 text-right text-base font-bold text-slate-800">
                    {m.amount.toLocaleString("ko-KR")}
                  </span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}
