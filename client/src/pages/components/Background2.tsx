import { Boxes } from "../../ui/background-boxes";

export function BackgroundBoxes() {
  return (
    <div className="fixed inset-0 w-full overflow-hidden bg-slate-900 flex flex-col items-center justify-center rounded-lg -z-10">
      {/* <div className="absolute inset-0 w-full h-full bg-slate-900 z-20 [mask-image:radial-gradient(transparent,white)] pointer-events-none" /> */}
      <Boxes />
    </div>
  );
}
