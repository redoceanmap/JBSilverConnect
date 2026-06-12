import { Ticket, MapPin, type LucideIcon } from "lucide-react";

export type Feature = {
  slug: string;
  href: string;
  title: string;
  short: string;
  description: string;
  icon: LucideIcon;
};

export const features: Feature[] = [
  {
    slug: "reservation",
    href: "/reservation",
    title: "지점 번호표 예약",
    short: "기다림 없이 미리",
    description: "지점에 가기 전에 번호표를 미리 받아 기다리는 시간을 줄이세요.",
    icon: Ticket,
  },
  {
    slug: "branch",
    href: "/branch",
    title: "가까운 지점 찾기",
    short: "대기 인원까지 한눈에",
    description: "내 위치에서 가장 가까운 지점과 현재 대기 인원을 보여드려요.",
    icon: MapPin,
  },
];
