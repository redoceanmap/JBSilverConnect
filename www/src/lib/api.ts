// JB Silver Connect 백엔드 API 클라이언트.
// AI(대화·요약)는 Gemini(키 없으면 Mock 폴백), 나머지 6개 기능은 Mock 데이터.

const BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

async function post<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${BASE_URL}/api/v1${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    throw new Error(`요청 실패 (${res.status})`);
  }
  return res.json() as Promise<T>;
}

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE_URL}/api/v1${path}`);
  if (!res.ok) {
    throw new Error(`요청 실패 (${res.status})`);
  }
  return res.json() as Promise<T>;
}

const DEMO_USER_ID = "user_kim_sonja";

/* ===== 대화형 AI (Gemini) ===== */
export type ChatRole = "user" | "assistant";
export type ChatMessage = { role: ChatRole; text: string };

export function sendChatMessage(messages: ChatMessage[]): Promise<{ reply: string }> {
  return post("/chat/message", { messages });
}

export function handoffToStaff(
  messages: ChatMessage[],
): Promise<{ summary: string; confirm_message: string }> {
  return post("/chat/handoff", { messages });
}

/* ===== 적금 제안 ===== */
export type SavingsProposal = {
  idle_amount: number;
  monthly_interest: number;
  rate: number;
  ai_message: string;
  agree_label: string;
  reject_label: string;
};

export function proposeSavings(): Promise<SavingsProposal> {
  return post("/savings/propose", { user_id: DEMO_USER_ID });
}

/* ===== 보이스피싱 점검 ===== */
export type PhishingResult = {
  risk_label: string;
  signal_color: string;
  alert_staff: boolean;
  advice: string;
};

export function checkPhishing(message: string): Promise<PhishingResult> {
  return post("/phishing/check", { message });
}

/* ===== 오늘의 안심 브리핑 ===== */
export type Briefing = {
  balance: number;
  weather_description: string;
  temperature: number;
  spoken_text: string;
  audio_size_bytes: number;
};

export function getDailyBriefing(): Promise<Briefing> {
  return post("/briefing/daily", { user_id: DEMO_USER_ID });
}

/* ===== 가까운 지점 ===== */
export type Branch = {
  name: string;
  distance_meters: number;
  waiting_count: number;
};

export function findNearbyBranches(
  latitude = 37.5665,
  longitude = 126.978,
  limit = 3,
): Promise<Branch[]> {
  return post("/branch/nearby", { latitude, longitude, limit });
}

/* ===== 번호표 예약 ===== */
export type Reservation = {
  reservation_id: string;
  ticket_number: number;
  purpose: string;
  message: string;
  status: "active" | "canceled";
  branch_name: string | null;
  note: string | null;
};

export function createReservation(
  purpose: string,
  branch_name?: string,
  note?: string,
): Promise<Reservation> {
  return post("/reservation/tickets", {
    user_id: DEMO_USER_ID,
    purpose,
    ...(branch_name ? { branch_name } : {}),
    ...(note ? { note } : {}),
  });
}

export function listReservations(): Promise<Reservation[]> {
  return get(`/reservation/tickets?user_id=${encodeURIComponent(DEMO_USER_ID)}`);
}

export function cancelReservation(reservationId: string): Promise<Reservation> {
  return post(`/reservation/tickets/${reservationId}/cancel`, {});
}

/* ===== 이자 리포트 ===== */
export type InterestReport = {
  total_interest: number;
  streak_months: number;
  monthly: { month: string; amount: number }[];
};

export function getInterestReport(): Promise<InterestReport> {
  return post("/report/interest", { user_id: DEMO_USER_ID });
}
