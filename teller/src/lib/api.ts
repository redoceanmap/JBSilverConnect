// JB Silver Connect 창구 단말 API 클라이언트.
// 어르신 앱이 보낸 방문 내용을 GET /queue/entries 로 조회하고,
// 도착 인증(arrive)·호출(call)로 대기열 상태를 전환한다.

const BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE_URL}/api/v1${path}`, { cache: "no-store" });
  if (!res.ok) {
    throw new Error(`요청 실패 (${res.status})`);
  }
  return res.json() as Promise<T>;
}

async function post(path: string): Promise<void> {
  const res = await fetch(`${BASE_URL}/api/v1${path}`, { method: "POST" });
  if (!res.ok) {
    throw new Error(`요청 실패 (${res.status})`);
  }
}

/* ===== 창구 대기열 카드 ===== */
export type QueueStatus = "waiting" | "on_site" | "called";

export type HandoffCard = {
  handoff_id: string;
  customer_name: string;
  customer_age: number;
  ticket_number: number;
  eta_text: string;
  purpose: string;
  target: string;
  amount: string;
  required_docs: string;
  special_notes: string;
  advice: string;
  original_message: string;
  status: QueueStatus;
  remaining_seconds: number;
};

export function listHandoffs(): Promise<HandoffCard[]> {
  return get("/queue/entries");
}

// 대기 → 현장대기
export function confirmArrival(handoffId: string): Promise<void> {
  return post(`/queue/entries/${handoffId}/arrive`);
}

// 현장대기 → 호출
export function callEntry(handoffId: string): Promise<void> {
  return post(`/queue/entries/${handoffId}/call`);
}
