# Tabel Morse dan fungsi-fungsi kecil untuk mengolahnya.

MORSE = {
    ".-": "A", "-...": "B", "-.-.": "C", "-..": "D", ".": "E",
    "..-.": "F", "--.": "G", "....": "H", "..": "I", ".---": "J",
    "-.-": "K", ".-..": "L", "--": "M", "-.": "N", "---": "O",
    ".--.": "P", "--.-": "Q", ".-.": "R", "...": "S", "-": "T",
    "..-": "U", "...-": "V", ".--": "W", "-..-": "X", "-.--": "Y",
    "--..": "Z",
    "-----": "0", ".----": "1", "..---": "2", "...--": "3", "....-": "4",
    ".....": "5", "-....": "6", "--...": "7", "---..": "8", "----.": "9",
}
KE_MORSE = {huruf: pola for pola, huruf in MORSE.items()}

# Malam 3: salinan untuk lembar sandi dan draf. Tabel asli tidak disentuh,
# jadi yang benar-benar terkirim tetap dibaca pakai MORSE.
SANDI_MALAM_3 = dict(MORSE)
del SANDI_MALAM_3["..---"]
SANDI_MALAM_3["..--."] = "2"


def ke_jadwal(teks, satuan):
    """Ubah teks jadi daftar (jenis, lama dalam ms) untuk diputar."""
    jadwal = []
    for huruf in teks:
        if huruf == " ":
            jadwal.append(("spasi", satuan * 4))   # total jeda kata = 7 satuan
            continue
        for simbol in KE_MORSE[huruf]:
            if simbol == ".":
                jadwal.append(("titik", satuan))
            else:
                jadwal.append(("strip", satuan * 3))
            jadwal.append(("jeda", satuan))
        jadwal.append(("huruf", satuan * 2))       # total jeda huruf = 3 satuan
    return jadwal


def terjemahkan(draf, tabel=MORSE):
    """Ubah daftar pola jadi teks. Pola yang tidak ada di tabel jadi '?'."""
    teks = ""
    for pola in draf:
        teks += tabel.get(pola, "?")
    return teks


def cek_balasan(draf, jawaban):
    if not draf:
        return "diam"
    if jawaban is None:        # sinyal tak dikenal: balasan apa pun dihitung
        return "dibalas"
    if terjemahkan(draf) == jawaban:
        return "benar"
    return "salah"
