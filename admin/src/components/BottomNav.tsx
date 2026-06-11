"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Home, MessageCircle, Sun, Ticket, MapPin } from "lucide-react";

const tabs = [
  { href: "/", label: "홈", icon: Home },
  { href: "/chat", label: "대화", icon: MessageCircle },
  { href: "/briefing", label: "브리핑", icon: Sun },
  { href: "/reservation", label: "예약", icon: Ticket },
  { href: "/branch", label: "지점", icon: MapPin },
];

export function BottomNav() {
  const pathname = usePathname();

  return (
    <nav aria-label="주요 메뉴" className="sticky bottom-0 z-50 px-3 pb-3 pt-2">
      <ul className="glass shadow-glass flex rounded-[26px] px-1.5 py-1.5">
        {tabs.map((tab) => {
          const active =
            tab.href === "/"
              ? pathname === "/"
              : pathname.startsWith(tab.href);
          return (
            <li key={tab.href} className="flex-1">
              <Link
                href={tab.href}
                aria-current={active ? "page" : undefined}
                className={`flex flex-col items-center gap-0.5 rounded-[20px] py-2 text-sm font-bold transition ${
                  active
                    ? "bg-gradient-to-b from-jb-500 to-jb-700 text-white shadow-glass"
                    : "text-slate-500"
                }`}
              >
                <tab.icon
                  className="size-6"
                  strokeWidth={active ? 2.5 : 2}
                  aria-hidden
                />
                {tab.label}
              </Link>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}
