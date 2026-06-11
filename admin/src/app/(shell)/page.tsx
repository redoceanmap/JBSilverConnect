"use client";

import { useEffect, useState } from "react";
import { Ticket, Users, MapPin, RefreshCw, Inbox } from "lucide-react";
import { listQueue, listHandoffs, type Reservation, type StaffHandoffCard } from "@/lib/api";
import { HandoffCard } from "@/components/HandoffCard";

// 창구 대기 현황은 실시간성이 중요해 일정 주기로 자동 갱신한다.
const POLL_MS = 3000;

export default function QueueBoard() {
  const [queue, setQueue] = useState<Reservation[] | null>(null);
  const [handoffs, setHandoffs] = useState<StaffHandoffCard[]>([]);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    let alive = true;
    async function load() {
      try {
        const [q, h] = await Promise.all([listQueue(), listHandoffs()]);
        if (!alive) return;
        setQueue(q);
        setHandoffs(h);
      } catch {
        if (alive) setQueue([]);
      }
    }
    void load();
    const timer = setInterval(() => void load(), POLL_MS);
    return () => {
      alive = false;
      clearInterval(timer);
    };
  }, []);

  async function refresh() {
    setRefreshing(true);
    try {
      const [q, h] = await Promise.all([listQueue(), listHandoffs()]);
      setQueue(q);
      setHandoffs(h);
    } catch {
      // 갱신 실패 시 직전 화면을 유지한다.
    } finally {
      setRefreshing(false);
    }
  }

  const waiting = queue?.length ?? 0;

  return (
    <div className="px-5 pb-8 pt-4">
      <div className="flex items-start justify-between gap-3">
        <div>
          <span className="flex size-16 items-center justify-center rounded-2xl bg-gradient-to-b from-jb-400 to-jb-700 text-white shadow-sm">
            <Ticket className="size-9" aria-hidden />
          </span>
          <h1 className="mt-4 text-3xl font-black text-slate-900">창구 대기 현황</h1>
          <p className="mt-2 flex items-center gap-2 text-lg text-slate-600">
            <Users className="size-5" aria-hidden />
            현재 <span className="font-bold text-jb-700">{waiting}</span>명 대기 중
          </p>
        </div>
        <button
          type="button"
          onClick={() => void refresh()}
          aria-label="새로고침"
          className="mt-1 flex shrink-0 items-center gap-2 rounded-xl border-2 border-slate-200 bg-white px-4 py-2 text-base font-bold text-slate-500 active:scale-95"
        >
          <RefreshCw
            className={`size-5 ${refreshing ? "animate-spin" : ""}`}
            aria-hidden
          />
          새로고침
        </button>
      </div>

      {/* 전달된 방문 안내 — 어르신이 도우미로 보낸 내용이 실시간으로 도착 */}
      {handoffs.length > 0 && (
        <div className="mt-8">
          <div className="flex items-center justify-between">
            <p className="flex items-center gap-2 text-lg font-bold text-slate-700">
              <Inbox className="size-5 text-jb-600" aria-hidden />
              전달된 방문 안내
            </p>
            <span className="rounded-full bg-jb-600 px-3 py-1 text-sm font-bold text-white">
              신규 {handoffs.length}건
            </span>
          </div>
          <ul className="mt-3 space-y-3">
            {[...handoffs].reverse().map((card) => (
              <li key={card.handoff_id}>
                <HandoffCard card={card} staff />
              </li>
            ))}
          </ul>
        </div>
      )}

      {queue === null && (
        <p className="mt-8 text-lg text-slate-500">대기 현황을 불러오는 중…</p>
      )}

      {queue !== null && queue.length === 0 && (
        <div className="mt-10 flex flex-col items-center rounded-3xl border border-slate-100 bg-white/70 p-10 text-center">
          <span className="flex size-16 items-center justify-center rounded-full bg-slate-100 text-slate-400">
            <Ticket className="size-9" aria-hidden />
          </span>
          <p className="mt-4 text-lg font-bold text-slate-500">
            대기 중인 번호표가 없습니다.
          </p>
        </div>
      )}

      {queue !== null && queue.length > 0 && (
        <ul className="mt-6 space-y-3">
          {queue.map((t, idx) => (
            <li
              key={t.reservation_id}
              className={`flex items-center gap-4 rounded-2xl border px-4 py-4 ${
                idx === 0 ? "border-jb-300 bg-jb-50" : "border-slate-200 bg-white"
              }`}
            >
              <span className="flex size-16 shrink-0 items-center justify-center rounded-2xl bg-gradient-to-b from-jb-400 to-jb-700 text-2xl font-black text-white">
                {t.ticket_number}
              </span>
              <div className="min-w-0 flex-1">
                <p className="text-xl font-bold text-slate-900">{t.purpose}</p>
                {t.branch_name && (
                  <p className="mt-1 flex items-center gap-1 text-base text-slate-500">
                    <MapPin className="size-4 shrink-0" aria-hidden />
                    {t.branch_name}
                  </p>
                )}
                {t.note && (
                  <p className="mt-2 rounded-xl bg-slate-50 px-3 py-2 text-base text-slate-600">
                    💬 {t.note}
                  </p>
                )}
              </div>
              {idx === 0 && (
                <span className="shrink-0 rounded-xl bg-jb-600 px-3 py-2 text-sm font-bold text-white">
                  다음 차례
                </span>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
