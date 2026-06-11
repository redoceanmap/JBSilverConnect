"use client";

import { useState } from "react";
import { Ticket, Check } from "lucide-react";
import { createReservation, type Reservation } from "@/lib/api";

const PURPOSES = ["통장 정리", "예금·적금 상담", "공과금 납부", "카드 발급"];

export default function ReservationPage() {
  const [purpose, setPurpose] = useState(PURPOSES[0]);
  const [result, setResult] = useState<Reservation | null>(null);
  const [loading, setLoading] = useState(false);

  async function reserve() {
    if (loading) return;
    setLoading(true);
    try {
      setResult(await createReservation(purpose));
    } catch {
      setResult(null);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="px-5 pb-8 pt-4">
      <span className="flex size-16 items-center justify-center rounded-2xl bg-gradient-to-b from-jb-400 to-jb-700 text-white shadow-sm">
        <Ticket className="size-9" aria-hidden />
      </span>
      <h1 className="mt-4 text-3xl font-black text-slate-900">지점 번호표 예약</h1>
      <p className="mt-2 text-lg text-slate-600">
        가시기 전에 번호표를 미리 받아 기다리는 시간을 줄이세요.
      </p>

      {!result && (
        <>
          <p className="mt-6 text-lg font-bold text-slate-700">무엇 때문에 가시나요?</p>
          <div className="mt-3 grid grid-cols-2 gap-3">
            {PURPOSES.map((p) => {
              const active = p === purpose;
              return (
                <button
                  key={p}
                  type="button"
                  onClick={() => setPurpose(p)}
                  className={`rounded-2xl border-2 px-4 py-5 text-lg font-bold transition active:scale-[0.98] ${
                    active
                      ? "border-jb-500 bg-jb-50 text-jb-700"
                      : "border-slate-200 bg-white text-slate-600"
                  }`}
                >
                  {p}
                </button>
              );
            })}
          </div>

          <button
            type="button"
            onClick={reserve}
            disabled={loading}
            className="mt-6 w-full rounded-2xl bg-gradient-to-b from-jb-500 to-jb-700 px-6 py-5 text-xl font-bold text-white active:scale-[0.98] disabled:opacity-60"
          >
            {loading ? "번호표를 받는 중…" : "번호표 받기"}
          </button>
        </>
      )}

      {result && (
        <div className="mt-6 flex flex-col items-center rounded-3xl border border-jb-100 bg-jb-50 p-8 text-center">
          <span className="flex size-14 items-center justify-center rounded-full bg-safe text-white">
            <Check className="size-8" aria-hidden />
          </span>
          <p className="mt-4 text-lg text-jb-700">{result.purpose} · 내 번호표</p>
          <p className="mt-1 text-6xl font-black text-jb-700">{result.ticket_number}</p>
          <p className="mt-4 text-lg leading-relaxed text-slate-700">{result.message}</p>
        </div>
      )}
    </div>
  );
}
