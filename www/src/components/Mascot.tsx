type MascotProps = {
  className?: string;
  /** 둥실 떠다니는 애니메이션 끄기 */
  still?: boolean;
};

/** JB 안심금융 마스코트 — 파란 펭귄 (3D 렌더 이미지). 둥실 애니메이션 (CSS) */
export function Mascot({ className, still }: MascotProps) {
  return (
    // eslint-disable-next-line @next/next/no-img-element
    <img
      src="/mascot.png"
      alt="JB 안심금융 도우미 펭귄"
      draggable={false}
      className={`select-none object-contain ${still ? "" : "mascot-bob"} ${className ?? ""}`}
    />
  );
}
