# PyDM - Python Download Manager

**PyDM** (Python Download Manager) is a simple yet powerful multithreaded file downloader written in Python. It supports resuming downloads, retrying on failures, and accelerating downloads by splitting the file into parts and downloading them in parallel.

---

## 🚀 Features

- Multi-threaded file downloading
- Resume support using metadata
- Retry mechanism on failure
- Merges all parts after successful download
- Simple CLI interface
- Progress bar for total and per-thread download status

---

## 🧰 Requirements

- Python 3.7+
- Works cross-platform (Linux, macOS, Windows)
- No third-party dependencies

---

## 🛠️ How to Use

1. **Clone this repository**

    ```bash
    git clone https://github.com/bsthen/PyDM.git
    cd PyDM
    ```

2. **Run the downloader**

    ```bash
    python pydm.py <URL>
    ```

    **Example:**

    ```bash
    python pydm.py https://example.com/large-file.zip
    ```

3. **Or run without an argument to be prompted:**

    ```bash
    python pydm.py
    ```

## 📂 Output

- Downloads the file in multiple .tmp chunks.
- Tracks metadata in meta_parts/ folder.
- Merges into the final file upon success.
- Cleans up all temp files and metadata automatically.

## 🔒 License

```text
MIT License

Copyright (c) 2025 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights 
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
copies of the Software, and to permit persons to whom the Software is 
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in 
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
SOFTWARE.
```
