import csv
import os
import subprocess

EXE_PATH = os.path.join("build", "windows-debug", "src", "src.exe")

SIZES = [200, 400, 800, 1200, 1600, 2000]
THREADS = [1, 2, 4, 6, 8, 12]
OUTPUT_CSV = "benchmark_results.csv"


def run_benchmark(n, threads):
    cmd = [EXE_PATH, "--bench", str(n), str(threads)]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())


def main():
    print(f"{'Size (N)':<10} | {'Threads':<8} | {'Time (ms)':<12} | {'Speedup':<10} | {'Efficiency':<10}")
    print("-" * 60)

    results = []

    for n in SIZES:
        base_time = None
        for t in THREADS:
            time_ms = run_benchmark(n, t)
            if t == 1:
                base_time = time_ms
                speedup = 1.0
                efficiency = 1.0
            else:
                speedup = base_time / time_ms
                efficiency = speedup / t
            print(f"{n:<10} | {t:<8} | {time_ms:<12.2f} | {speedup:<10.2f} | {efficiency:<10.2f}")
            results.append(
                {
                    "N": n,
                    "Threads": t,
                    "Time_ms": round(time_ms, 2),
                    "Speedup": round(speedup, 2),
                    "Efficiency": round(efficiency, 2),
                }
            )
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["N", "Threads", "Time_ms", "Speedup", "Efficiency"])
        writer.writeheader()
        writer.writerows(results)
    print("-" * 60)
    print(f"Эксперименты завершены. Результаты сохранены в файл: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()