import {
  PiggyBank,
  Ticket,
  ShieldAlert,
  Sun,
  MapPin,
  LineChart,
  type LucideIcon,
} from "lucide-react";

export type Feature = {
  slug: string;
  href: string;
  title: string;
  short: string;
  description: string;
  icon: LucideIcon;
};

/** 백엔드 6개 컨텍스트와 1:1 대응하는 어르신용 기능 카드 메타데이터 */
export const features: Feature[] = [
  {
    slug: "savings",
    href: "/savings",
    title: "여윳돈 적금 제안",
    short: "안 쓰는 돈, 똑똑하게",
    description: "통장에 잠자는 여윳돈을 AI가 찾아 알맞은 적금을 제안해 드려요.",
    icon: PiggyBank,
  },
  {
    slug: "phishing",
    href: "/phishing",
    title: "보이스피싱 확인",
    short: "수상한 전화·문자 점검",
    description: "받은 전화나 문자가 위험한지 신호등 색으로 알기 쉽게 알려드려요.",
    icon: ShieldAlert,
  },
  {
    slug: "briefing",
    href: "/briefing",
    title: "오늘의 안심 브리핑",
    short: "잔액과 날씨를 음성으로",
    description: "오늘 잔액과 날씨를 음성으로 들려드리는 하루 시작 브리핑입니다.",
    icon: Sun,
  },
  {
    slug: "branch",
    href: "/branch",
    title: "가까운 지점 찾기",
    short: "대기 인원까지 한눈에",
    description: "내 위치에서 가장 가까운 지점과 현재 대기 인원을 보여드려요.",
    icon: MapPin,
  },
  {
    slug: "reservation",
    href: "/reservation",
    title: "지점 번호표 예약",
    short: "기다림 없이 미리",
    description: "지점에 가기 전에 번호표를 미리 받아 기다리는 시간을 줄이세요.",
    icon: Ticket,
  },
  {
    slug: "report",
    href: "/report",
    title: "이자 리포트",
    short: "받은 이자를 한눈에",
    description: "그동안 받은 이자와 연속으로 이자가 들어온 개월을 정리해 드려요.",
    icon: LineChart,
  },
];
