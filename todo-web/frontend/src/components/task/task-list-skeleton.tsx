export function TaskListSkeleton() {
  return (
    <div className="space-y-3">
      {[...Array(5)].map((_, i) => (
        <div key={i} className="card animate-pulse">
          <div className="flex items-start gap-3">
            <div className="w-5 h-5 bg-gray-200 rounded-full" />
            <div className="flex-1">
              <div className="h-4 bg-gray-200 rounded w-3/4" />
              <div className="mt-2 h-3 bg-gray-200 rounded w-1/2" />
              <div className="mt-3 flex gap-2">
                <div className="h-5 bg-gray-200 rounded w-20" />
                <div className="h-5 bg-gray-200 rounded w-16" />
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
