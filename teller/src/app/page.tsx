"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import {
  Armchair,
  FileText,
  CircleUserRound,
  Clock,
  Wifi,
  WifiOff,
  Lightbulb,
  CheckCircle2,
  BellRing,
  Timer,
} from "lucide-react";
import {
  listHandoffs,
  confirmArrival,
  callEntry,
  type HandoffCard,
} from "@/lib/api";

const POLL_MS = 5000;

export default function TellerPage() {
  const [cards, setCards] = useState<HandoffCard[]>([]);
  const [fetchedAt, setFetchedAt] = useState(0);
  const [online, setOnline] = useState(true);
  const [loaded, setLoaded] = useState(false);
  const [, setTick] = useState(0);
  const seenRef = useRef<Set<string>>(new Set());
  const aliveRef = useRef(true);

  const poll = useCallback(async () => {
    try {
      const next = await listHandoffs();
      if (!aliveRef.current) return;
      setCards(next);
      setFetchedAt(Date.now());
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
    void poll();
    const id = setInterval(() => void poll(), POLL_MS);
    // 카운트다운 1초 갱신
    const tickId = setInterval(() => setTick((t) => t + 1), 1000);
    return () => {
      aliveRef.current = false;
      clearInterval(id);
      clearInterval(tickId);
    };
  }, [poll]);

  // 이번 렌더에서 처음 등장한 카드만 강조 애니메이션
  const newIds = new Set<string>();
  for (const c of cards) {
    if (!seenRef.current.has(c.handoff_id)) newIds.add(c.handoff_id);
  }
  useEffect(() => {
    for (const c of cards) seenRef.current.add(c.handoff_id);
  }, [cards]);

  // 서버 잔여 초 - 폴링 후 경과 초
  const remainingOf = (card: HandoffCard) => {
    const elapsed = Math.floor((Date.now() - fetchedAt) / 1000);
    return Math.max(0, card.remaining_seconds - elapsed);
  };

  const waiting = cards.filter((c) => c.status === "waiting");
  const onSite = cards.filter(
    (c) => c.status === "on_site" || c.status === "called",
  );

  const onArrive = async (id: string) => {
    try {
      await confirmArrival(id);
      await poll();
    } catch {
      setOnline(false);
    }
  };

  const onCall = async (id: string) => {
    try {
      await callEntry(id);
      await poll();
    } catch {
      setOnline(false);
    }
  };

  return (
    <div className="mx-auto max-w-6xl px-6 py-6">
      {/* 헤더 */}
      <header className="flex items-center gap-3 border-b border-slate-200 pb-4">
        <span className="flex size-10 items-center justify-center rounded-lg bg-jb-700 text-sm font-black text-white">
          JB
        </span>
        <div>
          <h1 className="text-lg font-black text-slate-900">창구 단말</h1>
          <p className="text-sm text-slate-500">사전 방문 안내</p>
        </div>
        <div className="ml-auto flex items-center gap-4">
          <span className="rounded-full bg-jb-50 px-3 py-1 text-sm font-bold text-jb-700">
            대기 {waiting.length} · 현장 {onSite.length}
          </span>
          <span
            className={`flex items-center gap-1.5 text-sm font-bold ${
              online ? "text-safe" : "text-danger"
            }`}
          >
            {online ? (
              <Wifi className="size-4" aria-hidden />
            ) : (
              <WifiOff className="size-4" aria-hidden />
            )}
            {online ? "실시간 연결" : "연결 끊김"}
          </span>
        </div>
      </header>

      {/* 빈 상태 */}
      {loaded && cards.length === 0 && (
        <div className="mt-20 flex flex-col items-center gap-3 text-center text-slate-400">
          <Armchair className="size-12" aria-hidden />
          <p className="text-base leading-relaxed">
            예약 고객이 방문 내용을 보내면
            <br />
            여기에 표시됩니다.
          </p>
        </div>
      )}

      {/* 대기 고객 */}
      {waiting.length > 0 && (
        <section className="mt-6">
          <SectionTitle label="대기 고객" count={waiting.length} tone="wait" />
          <div className="mt-3 grid gap-5 md:grid-cols-2">
            {waiting.map((c) => (
              <Card key={c.handoff_id} card={c} isNew={newIds.has(c.handoff_id)}>
                <div className="mt-4 flex items-center gap-3">
                  <span className="flex flex-1 items-center justify-center gap-1.5 rounded-xl bg-slate-100 py-2 text-sm font-bold text-slate-600">
                    <Timer className="size-4" aria-hidden />
                    {fmtClock(remainingOf(c))} 남음
                  </span>
                  <button
                    type="button"
                    onClick={() => void onArrive(c.handoff_id)}
                    className="flex flex-1 items-center justify-center gap-1.5 rounded-xl bg-jb-600 py-2.5 text-sm font-bold text-white active:scale-[0.98]"
                  >
                    <CheckCircle2 className="size-4" aria-hidden />
                    도착 인증
                  </button>
                </div>
              </Card>
            ))}
          </div>
        </section>
      )}

      {/* 현장대기 고객 */}
      {onSite.length > 0 && (
        <section className="mt-8">
          <SectionTitle label="현장대기 고객" count={onSite.length} tone="onsite" />
          <div className="mt-3 grid gap-5 md:grid-cols-2">
            {onSite.map((c) => (
              <Card key={c.handoff_id} card={c} isNew={newIds.has(c.handoff_id)}>
                {c.status === "called" ? (
                  <div className="mt-4 flex items-center gap-2 rounded-xl bg-warning/10 px-3 py-2.5 text-sm font-bold text-warning">
                    <BellRing className="size-4 shrink-0" aria-hidden />
                    호출됨 · {fmtClock(remainingOf(c))} 후 자동 삭제
                  </div>
                ) : (
                  <button
                    type="button"
                    onClick={() => void onCall(c.handoff_id)}
                    className="mt-4 flex w-full items-center justify-center gap-1.5 rounded-xl bg-gradient-to-b from-jb-500 to-jb-700 py-2.5 text-sm font-bold text-white active:scale-[0.98]"
                  >
                    <BellRing className="size-4" aria-hidden />
                    호출
                  </button>
                )}
              </Card>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}

function fmtClock(sec: number): string {
  const s = Math.max(0, sec);
  const m = Math.floor(s / 60);
  const ss = String(s % 60).padStart(2, "0");
  return `${m}:${ss}`;
}

function SectionTitle({
  label,
  count,
  tone,
}: {
  label: string;
  count: number;
  tone: "wait" | "onsite";
}) {
  return (
    <div className="flex items-center gap-2">
      <span
        className={`size-2.5 rounded-full ${
          tone === "wait" ? "bg-slate-400" : "bg-jb-500"
        }`}
      />
      <h2 className="text-base font-black text-slate-800">{label}</h2>
      <span className="rounded-full bg-slate-100 px-2 py-0.5 text-xs font-bold text-slate-500">
        {count}
      </span>
    </div>
  );
}

function Card({
  card,
  isNew,
  children,
}: {
  card: HandoffCard;
  isNew: boolean;
  children: React.ReactNode;
}) {
  const isCorporate = card.window_type === "corporate";
  return (
    <article
      className={`rounded-2xl border bg-white p-5 shadow-sm ${
        isCorporate
          ? "border-amber-200 border-l-4 border-l-amber-500 bg-amber-50/40"
          : "border-slate-200"
      } ${isNew ? "card-in" : ""}`}
    >
      {/* 고객 */}
      <div className="flex items-center gap-3">
        <span
          className={`flex size-11 items-center justify-center rounded-full ${
            isCorporate ? "bg-amber-100 text-amber-700" : "bg-jb-50 text-jb-600"
          }`}
        >
          <CircleUserRound className="size-7" aria-hidden />
        </span>
        <div className="min-w-0">
          <p className="flex items-center gap-2 text-base font-black text-slate-900">
            {card.customer_name} ({card.customer_age})
            {isCorporate && (
              <span className="rounded-full bg-amber-500 px-2 py-0.5 text-xs font-bold text-white">
                법인 사무
              </span>
            )}
          </p>
          <p className="flex items-center gap-1.5 text-sm text-slate-500">
            <Clock className="size-3.5" aria-hidden />
            대기 {card.ticket_label}번 · {card.eta_text}
          </p>
        </div>
      </div>

      {/* AI 정리 */}
      <div className="mt-4 rounded-xl border border-slate-100 bg-slate-50 p-4">
        <p className="mb-2 flex items-center gap-1.5 text-sm font-black text-jb-700">
          <FileText className="size-4" aria-hidden />
          AI가 정리한 방문 내용
        </p>
        <dl className="divide-y divide-slate-200 text-sm">
          <Row k="방문목적" v={card.purpose} />
          <Row k="특이사항" v={card.special_notes} />
        </dl>
      </div>

      {/* 조언 */}
      {card.advice && (
        <p className="mt-3 flex items-start gap-2 rounded-xl bg-jb-50 p-3 text-sm leading-relaxed text-slate-700">
          <Lightbulb className="mt-0.5 size-4 shrink-0 text-warning" aria-hidden />
          <span>{card.advice}</span>
        </p>
      )}

      {/* 원문 */}
      <p className="mt-3 rounded-lg bg-slate-50 px-3 py-2 text-xs leading-relaxed text-slate-500">
        <span className="font-bold text-slate-600">원문:</span> &ldquo;
        {card.original_message}&rdquo;
      </p>

      {/* 액션 (섹션별) */}
      {children}
    </article>
  );
}

function Row({
  k,
  v,
  highlight,
}: {
  k: string;
  v: string;
  highlight?: boolean;
}) {
  return (
    <div className="flex gap-3 py-2">
      <dt className="w-20 shrink-0 font-bold text-slate-500">{k}</dt>
      <dd className={`flex-1 ${highlight ? "font-bold text-danger" : "text-slate-800"}`}>
        {v}
      </dd>
    </div>
  );
}
