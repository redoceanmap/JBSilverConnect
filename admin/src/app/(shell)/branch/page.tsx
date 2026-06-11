"use client";

import { useEffect, useState } from "react";
import { MapPin, Users } from "lucide-react";
import { findNearbyBranches, type Branch } from "@/lib/api";

function formatDistance(meters: number): string {
  if (meters >= 1000) return `${(meters / 1000).toFixed(1)}km`;
  return `${meters}m`;
}

export default function BranchPage() {
  const [branches, setBranches] = useState<Branch[] | null>(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    function load(lat?: number, lng?: number) {
      findNearbyBranches(lat, lng)
        .then(setBranches)
        .catch(() => setError(true));
    }
    if (typeof navigator !== "undefined" && navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => load(pos.coords.latitude, pos.coords.longitude),
        () => load(),
      );
    } else {
      load();
    }
  }, []);

  return (
    <div className="px-5 pb-8 pt-4">
      <span className="flex size-16 items-center justify-center rounded-2xl bg-gradient-to-b from-emerald-300 to-emerald-500 text-white shadow-sm">
        <MapPin className="size-9" aria-hidden />
      </span>
      <h1 className="mt-4 text-3xl font-black text-slate-900">가까운 지점 찾기</h1>
      <p className="mt-2 text-lg text-slate-600">
        내 위치에서 가까운 지점과 현재 대기 인원을 보여드려요.
      </p>

      {error && (
        <p className="mt-6 rounded-2xl bg-danger/10 px-5 py-4 text-lg font-semibold text-danger">
          지점을 불러오지 못했어요.
        </p>
      )}

      {!branches && !error && (
        <p className="mt-6 text-lg text-slate-500">가까운 지점을 찾고 있어요…</p>
      )}

      {branches && (
        <ul className="mt-6 space-y-3">
          {branches.map((b, i) => (
            <li key={b.name} className="card flex items-center gap-4 rounded-3xl p-5">
              <span className="flex size-12 shrink-0 items-center justify-center rounded-2xl bg-jb-50 text-xl font-black text-jb-700">
                {i + 1}
              </span>
              <div className="flex-1">
                <p className="text-xl font-bold text-slate-900">{b.name}</p>
                <p className="text-lg text-slate-500">{formatDistance(b.distance_meters)}</p>
              </div>
              <div className="flex flex-col items-center text-jb-700">
                <Users className="size-6" aria-hidden />
                <span className="text-lg font-bold">{b.waiting_count}명</span>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
