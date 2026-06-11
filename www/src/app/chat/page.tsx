"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { ChevronLeft, Mic, Send, Headset, Ticket, MapPin, X } from "lucide-react";
import { Mascot } from "@/components/Mascot";
import {
  sendChatMessage,
  handoffToStaff,
  createReservation,
  findNearbyBranches,
  type ChatMessage,
  type Reservation,
} from "@/lib/api";
import { useSpeechRecognition } from "@/lib/useSpeechRecognition";

const GREETING: ChatMessage = {
  role: "assistant",
  text: "안녕하세요! 무엇을 도와드릴까요? 말로 하셔도 되고, 글로 적으셔도 돼요. 사투리도 괜찮아요 😊",
};

export default function ChatPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([GREETING]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [handoff, setHandoff] = useState<string | null>(null);
  const [issuing, setIssuing] = useState(false);
  const [ticket, setTicket] = useState<Reservation | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, loading, handoff]);

  async function sendText(text: string) {
    const trimmed = text.trim();
    if (!trimmed || loading) return;
    const next = [...messages, { role: "user" as const, text: trimmed }];
    setMessages(next);
    setInput("");
    setLoading(true);
    try {
      const { reply } = await sendChatMessage(next);
      setMessages([...next, { role: "assistant", text: reply }]);
    } catch {
      setMessages([
        ...next,
        { role: "assistant", text: "죄송해요, 잠시 후 다시 말씀해 주시겠어요?" },
      ]);
    } finally {
      setLoading(false);
    }
  }

  const { supported: micSupported, listening, toggle } = useSpeechRecognition(
    (text) => void sendText(text),
  );

  async function requestHandoff() {
    if (loading) return;
    setLoading(true);
    try {
      const { summary, confirm_message } = await handoffToStaff(messages);
      setHandoff(summary);
      setMessages((prev) => [...prev, { role: "assistant", text: confirm_message }]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: "직원 연결에 실패했어요. 잠시 후 다시 시도해 주세요." },
      ]);
    } finally {
      setLoading(false);
    }
  }

  async function issueTicket() {
    if (issuing) return;
    setIssuing(true);
    try {
      const branches = await findNearbyBranches();
      setTicket(await createReservation("방문 상담", branches[0]?.name));
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: "번호표 발행에 실패했어요. 잠시 후 다시 시도해 주세요." },
      ]);
    } finally {
      setIssuing(false);
    }
  }

  const started = messages.length > 1;
  const lastMessage = messages[messages.length - 1];
  const offersTicket = lastMessage.role === "assistant" && lastMessage.text.includes("번호표");

  return (
    <div className="relative flex h-dvh flex-col overflow-hidden bg-gradient-to-b from-[#0b1026] via-[#141a3a] to-[#241a44] text-white">
      <div className="pointer-events-none absolute left-1/2 top-20 size-[420px] -translate-x-1/2 rounded-full bg-[radial-gradient(circle,rgba(120,160,255,0.3),transparent_65%)] blur-2xl" />

      {/* 상단 바 */}
      <div className="relative flex items-center justify-between px-5 pt-4">
        <Link
          href="/"
          aria-label="뒤로 가기"
          className="flex size-11 items-center justify-center rounded-full border border-white/15 bg-white/10 backdrop-blur active:scale-95"
        >
          <ChevronLeft className="size-7" aria-hidden />
        </Link>
        <span className="flex items-center gap-2 text-base font-semibold text-white/70">
          <Mascot className="size-8" still />
          JB 도우미
        </span>
        <span className="size-11" />
      </div>

      {/* 대화 영역 */}
      <div ref={scrollRef} className="relative flex-1 space-y-4 overflow-y-auto px-5 py-5">
        {!started && (
          <div className="flex flex-col items-center pt-2 text-center">
            <Mascot className="h-44 w-44 drop-shadow-[0_20px_40px_rgba(80,120,255,0.45)]" />
          </div>
        )}

        {messages.map((m, i) => (
          <Bubble key={i} message={m} />
        ))}

        {loading && (
          <div className="flex justify-start">
            <div className="rounded-3xl rounded-bl-md border border-white/15 bg-white/10 px-5 py-3 text-lg text-white/70 backdrop-blur">
              도우미가 생각하고 있어요…
            </div>
          </div>
        )}

        {handoff && (
          <div className="rounded-3xl border border-jb-300/40 bg-jb-700/40 px-5 py-4 backdrop-blur">
            <p className="text-base font-bold text-jb-100">📋 직원에게 전달된 내용</p>
            <p className="mt-2 whitespace-pre-line text-lg leading-relaxed text-white/90">
              {handoff}
            </p>
          </div>
        )}
      </div>

      {/* 번호표 받기 — AI가 번호표를 언급하면 노출 */}
      {offersTicket && (
        <div className="relative px-5 pb-2">
          <button
            type="button"
            onClick={() => void issueTicket()}
            disabled={issuing}
            className="flex w-full items-center justify-center gap-2 rounded-2xl bg-gradient-to-b from-jb-400 to-jb-600 px-5 py-3 text-lg font-bold text-white shadow-[0_10px_30px_-8px_rgba(74,131,192,0.7)] active:scale-[0.98] disabled:opacity-50"
          >
            <Ticket className="size-6" aria-hidden />
            {issuing ? "번호표를 받는 중…" : "번호표 받기"}
          </button>
        </div>
      )}

      {/* 직원 전달 */}
      {started && (
        <div className="relative px-5">
          <button
            type="button"
            onClick={requestHandoff}
            disabled={loading}
            className="flex w-full items-center justify-center gap-2 rounded-2xl border border-white/20 bg-white/10 px-5 py-3 text-lg font-bold text-white backdrop-blur active:scale-[0.98] disabled:opacity-50"
          >
            <Headset className="size-6" aria-hidden />
            가까운 지점 직원에게 전달하기
          </button>
        </div>
      )}

      {/* 번호표 발행 팝업 */}
      {ticket && (
        <div className="absolute inset-0 z-10 flex items-center justify-center bg-black/60 px-6 backdrop-blur-sm">
          <div className="relative w-full max-w-sm rounded-3xl bg-white p-7 text-center text-slate-900 shadow-2xl">
            <button
              type="button"
              onClick={() => setTicket(null)}
              aria-label="닫기"
              className="absolute right-4 top-4 flex size-9 items-center justify-center rounded-full bg-slate-100 text-slate-500 active:scale-95"
            >
              <X className="size-5" aria-hidden />
            </button>
            <span className="mx-auto flex size-14 items-center justify-center rounded-full bg-gradient-to-b from-jb-400 to-jb-700 text-white">
              <Ticket className="size-8" aria-hidden />
            </span>
            {ticket.branch_name && (
              <p className="mt-4 flex items-center justify-center gap-1 text-base text-slate-500">
                <MapPin className="size-4" aria-hidden />
                {ticket.branch_name}
              </p>
            )}
            <p className="mt-1 text-lg text-jb-700">내 번호표</p>
            <p className="mt-1 text-7xl font-black text-jb-700">{ticket.ticket_number}</p>
            <p className="mt-4 text-lg leading-relaxed text-slate-700">{ticket.message}</p>
            <button
              type="button"
              onClick={() => setTicket(null)}
              className="mt-6 w-full rounded-2xl bg-gradient-to-b from-jb-500 to-jb-700 px-6 py-4 text-xl font-bold text-white active:scale-[0.98]"
            >
              확인
            </button>
          </div>
        </div>
      )}

      {/* 입력 바 */}
      <div className="relative flex items-end gap-2 px-5 pb-6 pt-3">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") void sendText(input);
          }}
          placeholder="여기에 말씀을 적어 주세요"
          aria-label="메시지 입력"
          className="h-14 flex-1 rounded-2xl border border-white/20 bg-white/10 px-5 text-lg text-white placeholder:text-white/45 backdrop-blur focus:border-white/40"
        />
        {micSupported && (
          <button
            type="button"
            onClick={toggle}
            aria-label="음성으로 말하기"
            className={`flex size-14 shrink-0 items-center justify-center rounded-2xl border transition active:scale-95 ${
              listening
                ? "border-rose-300 bg-rose-500/80 animate-pulse"
                : "border-white/20 bg-white/10"
            }`}
          >
            <Mic className="size-7" aria-hidden />
          </button>
        )}
        <button
          type="button"
          onClick={() => void sendText(input)}
          disabled={loading || !input.trim()}
          aria-label="보내기"
          className="flex size-14 shrink-0 items-center justify-center rounded-2xl bg-gradient-to-b from-jb-400 to-jb-600 text-white shadow-[0_10px_30px_-8px_rgba(74,131,192,0.7)] active:scale-95 disabled:opacity-40"
        >
          <Send className="size-7" aria-hidden />
        </button>
      </div>
    </div>
  );
}

function Bubble({ message }: { message: ChatMessage }) {
  const isUser = message.role === "user";
  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[82%] whitespace-pre-line rounded-3xl px-5 py-3 text-lg font-medium leading-snug backdrop-blur ${
          isUser
            ? "rounded-br-md bg-gradient-to-b from-jb-400 to-jb-600 text-white"
            : "rounded-bl-md border border-white/15 bg-white/10 text-white"
        }`}
      >
        {message.text}
      </div>
    </div>
  );
}
