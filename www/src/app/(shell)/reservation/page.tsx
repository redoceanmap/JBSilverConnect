"use client";

import { useState, useEffect } from "react";
import { Ticket, Check, MapPin, Users, Mic, Building2, FileText } from "lucide-react";
import { createReservation, findNearbyBranches, listReservations, cancelReservation, requestCorporateGuidance, CORPORATE_USER_ID, type Reservation, type Branch, type CorporateGuidance } from "@/lib/api";
import { useSpeechRecognition } from "@/lib/useSpeechRecognition";

const PURPOSES = ["통장 정리", "예금·적금 상담", "공과금 납부", "카드 발급", "법인 사무"];
const CORPORATE_PURPOSE = "법인 사무";

function formatDistance(meters: number): string {
  if (meters >= 1000) return `${(meters / 1000).toFixed(1)}km`;
  return `${meters}m`;
}

export default function ReservationPage() {
  const [branches, setBranches] = useState<Branch[] | null>(null);
  const [selectedBranch, setSelectedBranch] = useState<Branch | null>(null);
  const [purpose, setPurpose] = useState(PURPOSES[0]);
  const [note, setNote] = useState("");
  const [result, setResult] = useState<Reservation | null>(null);
  const [loading, setLoading] = useState(false);
  const [tickets, setTickets] = useState<Reservation[]>([]);
  const [coords, setCoords] = useState<{ lat: number; lng: number } | null>(null);
  const [guidance, setGuidance] = useState<CorporateGuidance | null>(null);

  const { supported: micSupported, listening: noteListen, toggle: noteToggle } = useSpeechRecognition(
    (text) => setNote((prev) => prev ? prev + " " + text : text),
  );

  function refreshTickets() {
    // 일반 고객(김순자)과 법인 사무 고객(박상호)의 번호표를 함께 보여준다.
    Promise.all([listReservations(), listReservations(CORPORATE_USER_ID)])
      .then(([general, corporate]) => setTickets([...general, ...corporate]))
      .catch(() => setTickets([]));
  }

  useEffect(() => {
    function load(lat?: number, lng?: number) {
      findNearbyBranches(lat, lng)
        .then(setBranches)
        .catch(() => setBranches([]));
    }
    if (typeof navigator !== "undefined" && navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          setCoords({ lat: pos.coords.latitude, lng: pos.coords.longitude });
          load(pos.coords.latitude, pos.coords.longitude);
        },
        () => load(),
      );
    } else {
      load();
    }
    refreshTickets();
  }, []);

  async function reserve() {
    if (loading || !selectedBranch) return;
    setLoading(true);
    try {
      const windowType = purpose === CORPORATE_PURPOSE ? "corporate" : "general";
      setResult(await createReservation(purpose, selectedBranch.name, note || undefined, windowType));
      refreshTickets();
      // 법인 사무 번호표는 필요 서류·예상 비용·가까운 발급 기관까지 함께 안내한다.
      if (windowType === "corporate") {
        requestCorporateGuidance(coords?.lat, coords?.lng)
          .then(setGuidance)
          .catch(() => setGuidance(null));
      } else {
        setGuidance(null);
      }
    } catch {
      setResult(null);
    } finally {
      setLoading(false);
    }
  }

  async function cancelTicket(id: string) {
    await cancelReservation(id).catch(() => {});
    refreshTickets();
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
          {/* 예약된 번호표 */}
          {tickets.length > 0 && (
            <div className="mt-6">
              <p className="text-lg font-bold text-slate-700">예약된 번호표</p>
              <ul className="mt-3 space-y-2">
                {tickets.map((t) => {
                  const canceled = t.status === "canceled";
                  return (
                    <li
                      key={t.reservation_id}
                      className={`flex items-center gap-4 rounded-2xl border px-4 py-4 ${
                        canceled ? "border-slate-200 bg-slate-50" : "border-jb-100 bg-jb-50"
                      }`}
                    >
                      <span
                        className={`flex size-12 shrink-0 items-center justify-center rounded-xl text-xl font-black text-white ${
                          canceled
                            ? "bg-slate-300"
                            : t.window_type === "corporate"
                              ? "bg-gradient-to-b from-amber-400 to-amber-600"
                              : "bg-gradient-to-b from-jb-400 to-jb-700"
                        }`}
                      >
                        {t.ticket_label}
                      </span>
                      <div className="min-w-0 flex-1">
                        {t.branch_name && (
                          <p
                            className={`flex items-center gap-1 text-base font-bold ${
                              canceled ? "text-slate-400" : "text-jb-700"
                            }`}
                          >
                            <MapPin className="size-4 shrink-0" aria-hidden />
                            {t.branch_name}
                          </p>
                        )}
                        <p className={`text-base ${canceled ? "text-slate-400" : "text-slate-600"}`}>
                          {t.purpose}
                        </p>
                      </div>
                      {canceled ? (
                        <span className="shrink-0 rounded-xl bg-slate-200 px-4 py-2 text-base font-bold text-slate-500">
                          취소됨
                        </span>
                      ) : (
                        <button
                          type="button"
                          onClick={() => void cancelTicket(t.reservation_id)}
                          className="shrink-0 rounded-xl border-2 border-slate-200 bg-white px-4 py-2 text-base font-bold text-slate-500 active:scale-95"
                        >
                          취소
                        </button>
                      )}
                    </li>
                  );
                })}
              </ul>
            </div>
          )}

          {/* 지점 선택 */}
          <p className="mt-6 text-lg font-bold text-slate-700">어느 지점에 가시나요?</p>
          {!branches && (
            <p className="mt-3 text-lg text-slate-500">가까운 지점을 찾고 있어요…</p>
          )}
          {branches && branches.length === 0 && (
            <p className="mt-3 text-lg text-slate-500">가까운 지점을 찾을 수 없어요.</p>
          )}
          {branches && branches.length > 0 && (
            <ul className="mt-3 space-y-2">
              {branches.map((b) => {
                const active = selectedBranch?.name === b.name;
                return (
                  <li key={b.name}>
                    <button
                      type="button"
                      onClick={() => setSelectedBranch(b)}
                      className={`flex w-full items-center gap-4 rounded-2xl border-2 px-4 py-4 transition active:scale-[0.98] ${
                        active
                          ? "border-jb-500 bg-jb-50"
                          : "border-slate-200 bg-white"
                      }`}
                    >
                      <MapPin
                        className={`size-6 shrink-0 ${active ? "text-jb-600" : "text-slate-400"}`}
                        aria-hidden
                      />
                      <div className="flex-1 text-left">
                        <p className={`text-lg font-bold ${active ? "text-jb-700" : "text-slate-800"}`}>
                          {b.name}
                        </p>
                        <p className="flex items-center gap-2 text-base text-slate-500">
                          <span>{formatDistance(b.distance_meters)}</span>
                          <span>·</span>
                          <Users className="size-4" aria-hidden />
                          <span>대기 {b.waiting_count}명</span>
                        </p>
                      </div>
                      {active && <Check className="size-6 shrink-0 text-jb-600" aria-hidden />}
                    </button>
                  </li>
                );
              })}
            </ul>
          )}

          {/* 방문 목적 */}
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

          {/* 창구 메모 */}
          <p className="mt-6 text-lg font-bold text-slate-700">창구에서 할 말 미리 정리하기</p>
          <p className="mt-1 text-base text-slate-500">직원에게 전달할 내용을 미리 적어두세요.</p>
          <textarea
            value={note}
            onChange={(e) => setNote(e.target.value)}
            placeholder="예: 통장 비밀번호를 잊어버렸어요. 재발급 방법을 알고 싶어요."
            rows={4}
            className="mt-3 w-full resize-none rounded-2xl border-2 border-slate-200 bg-white px-4 py-4 text-lg text-slate-700 outline-none placeholder:text-slate-400 focus:border-jb-400"
          />
          {micSupported && (
            <button
              type="button"
              onClick={noteToggle}
              aria-label="음성으로 입력하기"
              className={`mt-2 flex w-full items-center justify-center gap-3 rounded-2xl border-2 py-4 text-lg font-bold transition active:scale-[0.98] ${
                noteListen
                  ? "animate-pulse border-rose-300 bg-rose-50 text-rose-500"
                  : "border-slate-200 bg-white text-slate-500"
              }`}
            >
              <Mic className="size-6" aria-hidden />
              {noteListen ? "듣는 중… (탭하면 멈춰요)" : "말로 입력하기"}
            </button>
          )}

          <button
            type="button"
            onClick={reserve}
            disabled={loading || !selectedBranch}
            className="mt-6 w-full rounded-2xl bg-gradient-to-b from-jb-500 to-jb-700 px-6 py-5 text-xl font-bold text-white active:scale-[0.98] disabled:opacity-60"
          >
            {loading ? "번호표를 받는 중…" : "번호표 받기"}
          </button>
          {!selectedBranch && branches && branches.length > 0 && (
            <p className="mt-2 text-center text-base text-slate-400">지점을 선택해야 예약할 수 있어요.</p>
          )}
        </>
      )}

      {result && (
        <div className="mt-6 flex flex-col items-center rounded-3xl border border-jb-100 bg-jb-50 p-8 text-center">
          <span className="flex size-14 items-center justify-center rounded-full bg-safe text-white">
            <Check className="size-8" aria-hidden />
          </span>
          {result.branch_name && (
            <p className="mt-4 flex items-center gap-1 text-base text-slate-500">
              <MapPin className="size-4" aria-hidden />
              {result.branch_name}
            </p>
          )}
          <p className="mt-1 text-lg text-jb-700">{result.purpose} · 내 번호표</p>
          <p className="mt-1 text-6xl font-black text-jb-700">{result.ticket_label}</p>
          {result.window_type === "corporate" && (
            <p className="mt-2 rounded-full bg-amber-100 px-3 py-1 text-base font-bold text-amber-700">
              법인 사무 창구 (B 번호로 구별 호출돼요)
            </p>
          )}
          <p className="mt-4 text-lg leading-relaxed text-slate-700">{result.message}</p>
          <p className="mt-4 w-full rounded-2xl bg-white px-4 py-3 text-base font-bold leading-relaxed text-jb-700">
            번호표를 은행 도착해서 안내데스크에 보여주세요.
          </p>
          {result.note && (
            <div className="mt-4 w-full rounded-2xl border border-jb-100 bg-white px-4 py-3 text-left">
              <p className="text-sm font-bold text-slate-500">창구 전달 메모</p>
              <p className="mt-1 text-base text-slate-700">{result.note}</p>
            </div>
          )}

          {/* 법인 사무 안내 — 필요 서류·예상 비용·가까운 발급 기관 */}
          {result.window_type === "corporate" && guidance && (
            <div className="mt-4 w-full rounded-2xl border border-amber-200 bg-amber-50 px-4 py-4 text-left">
              <p className="flex items-center gap-1.5 text-base font-black text-amber-700">
                <Building2 className="size-5 shrink-0" aria-hidden />
                법인 사무 준비 안내
              </p>
              <p className="mt-1 text-sm leading-relaxed text-slate-600">{guidance.message}</p>
              <div className="mt-3 space-y-3">
                {guidance.tasks.map((task) => (
                  <div
                    key={task.task_name}
                    className="rounded-xl border border-amber-100 bg-white px-3 py-3"
                  >
                    <p className="flex items-center gap-1.5 text-base font-bold text-slate-800">
                      <FileText className="size-4 shrink-0 text-amber-500" aria-hidden />
                      {task.task_name}
                    </p>
                    <p className="mt-1 text-sm text-slate-600">
                      필요 서류: {task.required_docs.join(", ")}
                    </p>
                    <p className="text-sm text-slate-600">예상 비용: {task.estimated_cost}</p>
                    <p className="mt-2 text-xs font-bold text-amber-700">발급 기관 (가까운 순)</p>
                    <ul className="mt-1 space-y-1">
                      {task.institutions.map((inst, idx) => (
                        <li
                          key={inst.name}
                          className="flex items-center gap-1 text-sm text-slate-700"
                        >
                          <MapPin className="size-3.5 shrink-0 text-amber-500" aria-hidden />
                          <span className="font-bold">{idx + 1}.</span> {inst.kind} · {inst.name} (
                          {formatDistance(inst.distance_meters)})
                        </li>
                      ))}
                    </ul>
                  </div>
                ))}
              </div>
            </div>
          )}

          <button
            type="button"
            onClick={() => {
              setResult(null);
              setGuidance(null);
            }}
            className="mt-6 w-full rounded-2xl bg-gradient-to-b from-jb-500 to-jb-700 px-6 py-4 text-lg font-bold text-white active:scale-[0.98]"
          >
            내 예약 번호표 보기
          </button>
        </div>
      )}
    </div>
  );
}
