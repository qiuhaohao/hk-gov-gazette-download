# 📑 HK Gazette Downloader

No cap, this tool is bussin' fr fr - helps you yoink gazette docs straight from the Hong Kong gov website 💯

## ✨ What's the tea?

- Search up ANY gazette docs by year + whatever you're looking for
- Auto-downloads PDFs (we love automation bestie)
- Keeps your files organized and looking clean af
- Downloads multiple docs at once because ain't nobody got time to wait
- Respects the server (we're not trying to crash it, periodt)
- Shows you a progress bar because we're not living in the stone age

## 🚀 How to get this bad boy running

1. Yeet this repo onto your computer:
   ```
   git clone https://github.com/qiuhaohao/hk-gov-gazette-download.git
   cd hk-gov-gazette-download
   ```

2. Set up your vibe (virtual environment):
   ```
   python3 -m venv venv
   source venv/bin/activate  # Windows squad use: venv\Scripts\activate
   ```

3. Install the squad (dependencies):
   ```
   pip install -r requirements.txt
   ```

## 💅 How to use this slay

Basic command (it's giving main character energy):
```
python main.py -y YEAR1 -y YEAR2 -q "QUERY" -o OUTPUT_DIRECTORY [OPTIONS]
```

The options are lowkey fire:
- `-y`: Which years you want (stack 'em up bestie)
- `-q`: What you're looking for
- `-o`: Where to save your PDFs
- `-r`: How many times to retry if it flops (default: 3)
- `-w`: How many downloads can run at once (default: 10)
- `-l`: Language choice (default: chinese)

### ⭐ Examples that hit different

#### Chinese search (traditional tingz):
```sh
python main.py -y 2024 -y 2023 -q "公司註冊處處長" -o output_pdfs
```
This one's searching for docs with "公司註冊處處長" from 2023-2024, no cap

#### English search (for the global girlies):
```sh
python main.py -y 2024 -y 2023 -q "Registrar of Companies" -o output_pdfs -l english
```
Same vibe but make it English 💁‍♀️

---

Bestie, if this tool helped you out, don't forget to smash that ⭐ button! And if you're running into any problems, just drop an issue - we don't gatekeep in this community 💅✨