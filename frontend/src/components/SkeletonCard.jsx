/**
 * SkeletonCard — pulsing placeholder shown while the Django/SQL query runs.
 *
 * Mirrors the exact geometry of BentoProductCard (image block, title bar,
 * rating dots, price + button row) so the swap from skeleton -> content
 * causes no layout shift. Accepts the same bento `variant` so featured/wide
 * tiles get matching placeholder spans.
 */

/** Class bundles mirroring BentoProductCard's VARIANTS map */
const VARIANTS = {
  default: { cell: "", img: "h-44 sm:h-48" },
  featured: { cell: "sm:col-span-2", img: "h-56 sm:h-72" },
  wide: {
    cell: "xl:col-span-2",
    img: "h-44 sm:h-full sm:w-[45%]",
  },
};

export default function SkeletonCard({ variant = "default" }) {
  const v = VARIANTS[variant] ?? VARIANTS.default;
  const isWide = variant === "wide";

  return (
    <div
      className={`card overflow-hidden ${v.cell}`}
      role="status"
      aria-label="Loading product"
    >
      <div className={`flex ${isWide ? "sm:flex-row-reverse" : "flex-col"}`}>
        {/* Image placeholder */}
        <div className={`skeleton w-full rounded-none ${v.img}`} />

        {/* Text placeholders */}
        <div className="flex flex-1 flex-col gap-3 p-5">
          <div className="skeleton h-2.5 w-16" />            {/* category eyebrow */}
          <div className="skeleton h-4 w-3/4" />             {/* title */}
          <div className="flex gap-1">                        {/* star row */}
            {[...Array(5)].map((_, i) => (
              <div key={i} className="skeleton h-3 w-3 !rounded-full" />
            ))}
          </div>
          <div className="skeleton h-3 w-full max-w-[90%]" /> {/* description */}
          <div className="mt-auto flex items-center justify-between pt-3">
            <div className="skeleton h-5 w-16" />             {/* price */}
            <div className="skeleton h-9 w-28 !rounded-full" />{/* quick-add button */}
          </div>
        </div>
      </div>
    </div>
  );
}
