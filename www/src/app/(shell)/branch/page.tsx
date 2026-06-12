"use client";

import { useEffect, useRef, useState } from "react";
import { Users } from "lucide-react";
import { findNearbyBranches, type Branch } from "@/lib/api";

/* eslint-disable @typescript-eslint/no-explicit-any */
declare global {
  interface Window {
    kakao: any;
  }
}

const MAP_KEY = process.env.NEXT_PUBLIC_KAKAO_MAP_KEY ?? "";

function formatDistance(meters: number): string {
  if (meters >= 1000) return `${(meters / 1000).toFixed(1)}km`;
  return `${meters}m`;
}

function initMap(container: HTMLDivElement, lat: number, lng: number) {
  const center = new window.kakao.maps.LatLng(lat, lng);
  const map = new window.kakao.maps.Map(container, { center, level: 5 });

  new window.kakao.maps.Marker({ position: center, map });

  const ps = new window.kakao.maps.services.Places();
  ps.keywordSearch(
    "전북은행",
    (data: any[], status: string) => {
      if (status !== window.kakao.maps.services.Status.OK) return;
      data.slice(0, 5).forEach((place: any) => {
        const pos = new window.kakao.maps.LatLng(place.y, place.x);
        const marker = new window.kakao.maps.Marker({ position: pos, map });
        const info = new window.kakao.maps.InfoWindow({
          content: `<div style="padding:6px 10px;font-size:13px;font-weight:bold;white-space:nowrap">${place.place_name}</div>`,
        });
        window.kakao.maps.event.addListener(marker, "click", () => info.open(map, marker));
      });
    },
    { location: center, radius: 20000, sort: window.kakao.maps.services.SortBy.DISTANCE },
  );
}

export default function BranchPage() {
  const mapRef = useRef<HTMLDivElement>(null);
  const [branches, setBranches] = useState<Branch[] | null>(null);
  const [userPos, setUserPos] = useState<{ lat: number; lng: number } | null>(null);

  // 위치 획득 + 백엔드 지점 목록
  useEffect(() => {
    function load(lat = 35.8242, lng = 127.1086) {
      setUserPos({ lat, lng });
      findNearbyBranches(lat, lng).then(setBranches).catch(() => setBranches([]));
    }
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => load(pos.coords.latitude, pos.coords.longitude),
        () => load(),
      );
    } else {
      load();
    }
  }, []);

  // 카카오맵 SDK 동적 로드 후 지도 초기화
  useEffect(() => {
    if (!userPos || !mapRef.current) return;
    const container = mapRef.current;
    const { lat, lng } = userPos;

    if (window.kakao?.maps) {
      initMap(container, lat, lng);
      return;
    }

    const script = document.createElement("script");
    script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${MAP_KEY}&libraries=services`;
    script.async = true;
    script.onload = () => initMap(container, lat, lng);
    document.head.appendChild(script);

    return () => {
      if (document.head.contains(script)) document.head.removeChild(script);
    };
  }, [userPos]);

  return (
    <>
      {/* 지도 */}
      <div ref={mapRef} className="relative h-64 w-full bg-slate-100" />

      {/* 목록 */}
      <div className="px-5 pb-8 pt-5">
        <h1 className="text-2xl font-black text-slate-900">가까운 지점</h1>
        <p className="mt-1 text-base text-slate-500">마커를 누르면 지점 이름을 볼 수 있어요.</p>

        {!branches && (
          <p className="mt-6 text-lg text-slate-500">위치를 찾고 있어요…</p>
        )}

        {branches && branches.length === 0 && (
          <p className="mt-6 text-lg text-slate-500">주변 지점을 불러오지 못했어요.</p>
        )}

        {branches && branches.length > 0 && (
          <ul className="mt-4 space-y-3">
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
    </>
  );
}
