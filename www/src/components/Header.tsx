import Link from "next/link";
import { ShieldCheck } from "lucide-react";

export function Header() {
  return (
    <header className="glass sticky top-0 z-50 border-x-0 border-t-0">
      <div className="flex items-center px-5 py-3">
        <Link href="/" className="flex items-center gap-2.5">
          <span className="flex size-10 items-center justify-center rounded-2xl bg-gradient-to-b from-jb-500 to-jb-700 text-white shadow-glass">
            <ShieldCheck className="size-6" aria-hidden />
          </span>
          <span className="text-xl font-black text-jb-700">JB 안심금융</span>
        </Link>
      </div>
    </header>
  );
}
