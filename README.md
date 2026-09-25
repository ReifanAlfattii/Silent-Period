# Silent Period

Game operator radio pantai. Dengar kode Morse dari kapal, terjemahkan sendiri,
lalu ketuk balasan pakai Spasi. Detail desain ada di GDD (file .docx).

## Cara menjalankan

Butuh Python 3.10+ dan pygame.

```
pip install -r requirements.txt
python main.py
```

Atau pakai virtual environment supaya tidak bentrok dengan proyek lain:

```
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python main.py
```

## Kontrol

| Tombol    | Fungsi                                        |
|-----------|-----------------------------------------------|
| Spasi     | ketuk Morse (tekan cepat = titik, tahan = strip) |
| Tab       | buka / tutup lembar sandi                     |
| Backspace | hapus                                         |
| Enter     | kirim balasan / lanjut                        |
| R         | putar ulang pesan permintaan                  |
| Esc       | keluar                                        |

## File

- `main.py` loop utama, state, input, ketukan, suara
- `tampilan.py` menggambar layar
- `morse.py` tabel Morse dan jadwal bunyi
- `malam.py` isi cerita tiap malam
