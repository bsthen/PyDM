import os
import sys
import time
import json
import threading
import urllib.parse
import urllib.request

# Get URL from command line or input
if len(sys.argv) > 1:
    video_url = sys.argv[1]
else:
    video_url = input("Enter A URL File to download: ").strip()

output_file = os.path.basename(urllib.parse.urlparse(video_url).path)
num_threads = 8
max_retries = 5
meta_folder = "meta_parts"

os.makedirs(meta_folder, exist_ok=True)

req = urllib.request.Request(video_url, method="HEAD", headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as response:
    file_size = int(response.headers["Content-Length"])
print(f"📦 File size: {file_size / (1024*1024):.2f} MB")

chunk_size = file_size // num_threads
lock = threading.Lock()
progress = [0] * num_threads

def save_meta(index, downloaded):
    meta_path = os.path.join(meta_folder, f"part_{index}.json")
    with open(meta_path, "w") as f:
        json.dump({"downloaded": downloaded}, f)

def load_meta(index):
    meta_path = os.path.join(meta_folder, f"part_{index}.json")
    if os.path.exists(meta_path):
        with open(meta_path, "r") as f:
            data = json.load(f)
            return data.get("downloaded", 0)
    return 0

def download_range(start, end, index):
    part_path = f"part_{index}.tmp"
    retries = 0
    downloaded = load_meta(index)
    real_start = start + downloaded
    total_length = end - start + 1

    while retries < max_retries:
        try:
            req = urllib.request.Request(
                video_url,
                headers={
                    "User-Agent": "Mozilla/5.0",
                    "Range": f"bytes={real_start}-{end}"
                }
            )
            with urllib.request.urlopen(req) as response:
                mode = "ab" if os.path.exists(part_path) else "wb"
                with open(part_path, mode) as f:
                    while True:
                        chunk = response.read(256 * 1024)
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded += len(chunk)
                        real_start += len(chunk)
                        with lock:
                            progress[index] = downloaded
                        save_meta(index, downloaded)

            # print(f"\n✅ Thread {index + 1} finished.")
            return
        except Exception as e:
            retries += 1
            print(f"\n⚠️ Thread {index + 1} error {e}, retry {retries}/{max_retries}")
            time.sleep(1)
    print(f"\n❌ Thread {index + 1} failed after {max_retries} retries.")

def print_progress():
    while any(t.is_alive() for t in threads):
        with lock:
            total_downloaded = sum(progress)
            percent = total_downloaded * 100 / file_size
            downloaded_mb = total_downloaded / (1024*1024)
            total_mb = file_size / (1024*1024)
            sys.stdout.write(f"\r📊 Progress: {percent:.2f}% ({downloaded_mb:.2f} MB / {total_mb:.2f} MB)")
            sys.stdout.flush()
        time.sleep(0.5)

threads = []
for i in range(num_threads):
    start = i * chunk_size
    end = file_size - 1 if i == num_threads - 1 else (start + chunk_size - 1)
    t = threading.Thread(target=download_range, args=(start, end, i))
    threads.append(t)
    t.start()

monitor = threading.Thread(target=print_progress)
monitor.start()

for t in threads:
    t.join()
monitor.join()

try:
    # Merge files
    with open(output_file, "wb") as outfile:
        for i in range(num_threads):
            part_path = f"part_{i}.tmp"
            if os.path.exists(part_path):
                with open(part_path, "rb") as infile:
                    outfile.write(infile.read())

    print(f"\n🎉 Download complete: {output_file}")
except Exception as e:
    print(f"\n❌ Failed to merge parts: {e}")
finally:
    # Cleanup temp files
    for i in range(num_threads):
        part_path = f"part_{i}.tmp"
        meta_path = os.path.join(meta_folder, f"part_{i}.json")
        if os.path.exists(part_path):
            os.remove(part_path)
        if os.path.exists(meta_path):
            os.remove(meta_path)

    # Remove meta_parts folder if empty
    if os.path.exists(meta_folder) and not os.listdir(meta_folder):
        os.rmdir(meta_folder)