// JB AI Connect 백엔드 API 클라이언트.
// AI(대화·요약)는 Gemini(키 없으면 Mock 폴백), 나머지 기능은 Mock 데이터.

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
// 법인 사무창구 데모 고객(박상호). 법인 번호표는 이 고객으로 발급된다.
export const CORPORATE_USER_ID = "user_park_corp";

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
export type WindowType = "general" | "corporate";

export type Reservation = {
  reservation_id: string;
  ticket_number: number;
  ticket_label: string;
  window_type: WindowType;
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
  window_type: WindowType = "general",
): Promise<Reservation> {
  // 법인 사무 번호표는 법인 고객(박상호)으로 발급해 창구 단말에서 구별된다.
  const user_id = window_type === "corporate" ? CORPORATE_USER_ID : DEMO_USER_ID;
  return post("/reservation/tickets", {
    user_id,
    purpose,
    window_type,
    ...(branch_name ? { branch_name } : {}),
    ...(note ? { note } : {}),
  });
}

export function listReservations(userId: string = DEMO_USER_ID): Promise<Reservation[]> {
  return get(`/reservation/tickets?user_id=${encodeURIComponent(userId)}`);
}

export function cancelReservation(reservationId: string): Promise<Reservation> {
  return post(`/reservation/tickets/${reservationId}/cancel`, {});
}

/* ===== 법인 사무 안내 ===== */
export type CorporateInstitution = {
  name: string;
  kind: string;
  distance_meters: number;
};

export type CorporateTask = {
  task_name: string;
  required_docs: string[];
  estimated_cost: string;
  institutions: CorporateInstitution[];
};

export type CorporateGuidance = {
  message: string;
  tasks: CorporateTask[];
};

export type GuidanceTopic = "corporate" | "mortgage";

export function requestCorporateGuidance(
  latitude = 37.5665,
  longitude = 126.978,
  topic: GuidanceTopic = "corporate",
): Promise<CorporateGuidance> {
  return post("/corporate/guidance", {
    user_id: DEMO_USER_ID,
    latitude,
    longitude,
    topic,
  });
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
