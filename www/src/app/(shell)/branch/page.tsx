"use client";

import { useEffect, useRef, useState } from "react";
import { Users } from "lucide-react";
import { findNearbyBranches, type Branch } from "@/lib/api";

/* eslint-disable @typescript-eslint/no-explicit-any */
declare global {
  interface Window {
    naver: any;
  }
}

const MAP_KEY = process.env.NEXT_PUBLIC_NAVER_CLIENT_ID ?? "";

function formatDistance(meters: number): string {
  if (meters >= 1000) return `${(meters / 1000).toFixed(1)}km`;
  return `${meters}m`;
}

export default function BranchPage() {
  const mapRef = useRef<HTMLDivElement>(null);
  const naverMapRef = useRef<any>(null);
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

  // 지도 초기화 — userPos 확보되면 바로 실행 (branches 기다리지 않음)
  useEffect(() => {
    if (!userPos || !mapRef.current) return;
    const container = mapRef.current;
    const { lat, lng } = userPos;

    function initMap() {
      const center = new window.naver.maps.LatLng(lat, lng);
      naverMapRef.current = new window.naver.maps.Map(container, { center, zoom: 14 });
      new window.naver.maps.Marker({ position: center, map: naverMapRef.current });
    }

    if (window.naver?.maps) {
      initMap();
      return;
    }

    const script = document.createElement("script");
    script.src = `https://oapi.map.naver.com/openapi/v3/maps.js?ncpKeyId=${MAP_KEY}`;
    script.onload = initMap;
    document.head.appendChild(script);
  }, [userPos]);

  // 마커 추가 — branches 도착 후 실행
  useEffect(() => {
    if (!branches || !naverMapRef.current || branches.length === 0) return;
    const bounds = new window.naver.maps.LatLngBounds();
    branches.forEach((branch) => {
      const pos = new window.naver.maps.LatLng(branch.latitude, branch.longitude);
      bounds.extend(pos);
      const marker = new window.naver.maps.Marker({ position: pos, map: naverMapRef.current });
      const infoWindow = new window.naver.maps.InfoWindow({
        content: `<div style="padding:6px 10px;font-size:13px;font-weight:bold;white-space:nowrap">${branch.name}</div>`,
      });
      window.naver.maps.Event.addListener(marker, "click", () => {
        if (infoWindow.getMap()) {
          infoWindow.close();
        } else {
          infoWindow.open(naverMapRef.current, marker);
        }
      });
    });
    naverMapRef.current.fitBounds(bounds);
  }, [branches]);

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
