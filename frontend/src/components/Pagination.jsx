export default function Pagination({ page, pages, onPage }) {
  if (pages <= 1) return null;
  const nums = Array.from({ length: pages }, (_, i) => i + 1);

  return (
    <nav className="mt-10 flex items-center justify-center gap-2">
      <button
        disabled={page === 1}
        onClick={() => onPage(page - 1)}
        className="btn-outline !px-3 !py-1.5"
      >
        Prev
      </button>
      {nums.map((n) => (
        <button
          key={n}
          onClick={() => onPage(n)}
          className={`h-9 w-9 rounded-lg text-sm font-semibold transition ${
            n === page
              ? "bg-indigo-500 text-white"
              : "bg-slate-800 text-slate-600 hover:bg-indigo-50"
          }`}
        >
          {n}
        </button>
      ))}
      <button
        disabled={page === pages}
        onClick={() => onPage(page + 1)}
        className="btn-outline !px-3 !py-1.5"
      >
        Next
      </button>
    </nav>
  );
}
