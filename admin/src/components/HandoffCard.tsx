import { ClipboardList, Lightbulb } from "lucide-react";
import type { StaffHandoffCard } from "@/lib/api";

function Row({ label, value, danger }: { label: string; value: string; danger?: boolean }) {
  return (
    <div className="flex items-start justify-between gap-4 border-t border-slate-100 py-2.5 first:border-t-0 first:pt-0">
      <span className="shrink-0 text-base font-bold text-slate-500">{label}</span>
      <span className={`text-right text-base font-bold ${danger ? "text-rose-600" : "text-slate-800"}`}>
        {value}
      </span>
    </div>
  );
}

// 어르신 폰(staff=false)과 창구 단말(staff=true)이 공유하는 전달 카드.
// 프로토타입 그대로: 고객정보 + AI 정리 방문내용 + 원문 + AI 조언.
export function HandoffCard({ card, staff }: { card: StaffHandoffCard; staff?: boolean }) {
  return (
    <div className="overflow-hidden rounded-3xl border border-jb-100 bg-white shadow-sm">
      {staff && (
        <div className="flex items-center gap-3 border-b border-slate-100 bg-jb-50/60 px-5 py-4">
          <span className="flex size-11 items-center justify-center rounded-full bg-jb-100 text-2xl">
            👵
          </span>
          <div>
            <p className="text-xl font-black text-slate-900">
              {card.customer_name} ({card.customer_age})
            </p>
            <p className="text-base text-slate-500">
              대기번호 {card.ticket_number}번 · {card.eta_text}
            </p>
          </div>
        </div>
      )}

      <div className="px-5 py-4">
        <p className="flex items-center gap-2 text-base font-bold text-jb-700">
          <ClipboardList className="size-5" aria-hidden />
          AI가 정리한 방문 내용
        </p>
        <div className="mt-3">
          <Row label="방문목적" value={card.purpose} />
          <Row label="대상" value={card.target} />
          <Row label="금액" value={card.amount} />
          <Row label="필요 서류" value={card.required_docs} danger />
          <Row label="특이사항" value={card.special_notes} />
        </div>

        {card.original_message && (
          <div className="mt-4 rounded-2xl bg-slate-50 px-4 py-3">
            <span className="text-base font-bold text-slate-500">원문</span>
            <span className="ml-2 text-base text-slate-600">&ldquo;{card.original_message}&rdquo;</span>
          </div>
        )}
      </div>

      {staff && (
        <div className="flex items-start gap-2 border-t border-slate-100 bg-safe/10 px-5 py-4">
          <Lightbulb className="mt-0.5 size-5 shrink-0 text-safe" aria-hidden />
          <p className="text-base leading-relaxed text-slate-700">{card.advice}</p>
        </div>
      )}
    </div>
  );
}
