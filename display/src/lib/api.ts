// JB AI Connect 고객 호출 전광판 API 클라이언트.
// 창구 단말(teller)이 호출(call)한 고객을 GET /queue/entries 에서 status==="called" 로 골라 보여준다.

const BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export type QueueStatus = "waiting" | "on_site" | "called";
export type WindowType = "general" | "corporate";

export type CallCard = {
  handoff_id: string;
  customer_name: string;
  ticket_label: string;
  window_type: WindowType;
  status: QueueStatus;
  remaining_seconds: number;
};

export async function listCalledEntries(): Promise<CallCard[]> {
  const res = await fetch(`${BASE_URL}/api/v1/queue/entries`, { cache: "no-store" });
  if (!res.ok) {
    throw new Error(`요청 실패 (${res.status})`);
  }
  const entries = (await res.json()) as CallCard[];
  // 호출된 고객만, 최근 호출(잔여 시간이 큰 순)이 위로 오도록 정렬한다.
  return entries
    .filter((entry) => entry.status === "called")
    .sort((a, b) => b.remaining_seconds - a.remaining_seconds);
}
