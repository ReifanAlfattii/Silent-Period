# Semua fungsi untuk menggambar layar. Tidak ada logika game di sini.

import pygame

# warna
LATAR = (13, 11, 8)        # #0D0B08
PANEL = (20, 17, 12)       # #14110C
GARIS = (58, 46, 26)       # #3A2E1A
TEKS = (232, 196, 138)     # #E8C48A
AMBER = (240, 168, 51)     # #F0A833
HIJAU = (134, 192, 106)    # #86C06A
MERAH = (224, 100, 74)     # #E0644A
REDUP = (125, 102, 66)     # amber redup untuk tulisan pelengkap
KERTAS = (27, 23, 16)      # latar lembar sandi

font_kecil = None
font_sedang = None
font_besar = None
font_jumbo = None


def siapkan_font():
    global font_kecil, font_sedang, font_besar, font_jumbo
    font_kecil = pygame.font.SysFont("consolas", 13)
    font_sedang = pygame.font.SysFont("consolas", 16)
    font_besar = pygame.font.SysFont("consolas", 26)
    font_jumbo = pygame.font.SysFont("consolas", 40)


# ------------------------------------------------------------ alat bantu

def tulis(layar, teks, font, warna, x, y, rata="kiri"):
    gambar = font.render(teks, True, warna)
    if rata == "kanan":
        x -= gambar.get_width()
    elif rata == "tengah":
        x -= gambar.get_width() // 2
    layar.blit(gambar, (x, y))
    return gambar.get_width()


def kotak(layar, rect, garis=GARIS, isi=PANEL):
    pygame.draw.rect(layar, isi, rect)
    pygame.draw.rect(layar, garis, rect, 1)


def redupkan(layar, rect, kekuatan):
    tutup = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
    tutup.fill((13, 11, 8, kekuatan))
    layar.blit(tutup, (rect[0], rect[1]))


def lebar_pola(pola, t=8):
    lebar = 0
    for simbol in pola:
        if simbol == ".":
            lebar += t
        else:
            lebar += t * 3
        lebar += t // 2 + 2
    return lebar


def gambar_pola(layar, pola, x, y, warna, t=8):
    # titik = lingkaran, strip = kotak membulat
    for simbol in pola:
        if simbol == ".":
            pygame.draw.circle(layar, warna, (x + t // 2, y + t // 2), t // 2)
            x += t
        else:
            pygame.draw.rect(layar, warna, (x, y, t * 3, t), border_radius=t // 2)
            x += t * 3
        x += t // 2 + 2


def titik_hijau(layar, teks, x_kanan, y):
    # tulisan status hijau dengan bulatan kecil di depannya, rata kanan
    lebar = tulis(layar, teks, font_kecil, HIJAU, x_kanan, y, "kanan")
    pygame.draw.circle(layar, HIJAU, (x_kanan - lebar - 10, y + 8), 3)


# ------------------------------------------------------------ bingkai

def gambar_kepala(layar, malam_ke):
    tulis(layar, "STASIUN PANTAI TANJUNG — POS 12", font_kecil, AMBER, 26, 18)
    tulis(layar, "MALAM " + str(malam_ke) + " / 3  ·  KABUT TEBAL  ·  500 kHz",
          font_kecil, TEKS, 1254, 18, "kanan")
    pygame.draw.line(layar, GARIS, (26, 44), (1254, 44))


def gambar_status(layar, kiri, kanan):
    pygame.draw.rect(layar, AMBER, (0, 688, 1280, 32))
    tulis(layar, kiri, font_kecil, LATAR, 26, 697)
    tulis(layar, kanan, font_kecil, LATAR, 1254, 697, "kanan")


# ------------------------------------------------------------ bagian atas

def gambar_sinyal(layar, sumber, pola_masuk, tertutup, tabel, sedang_putar, lampu, sunyi, sisa_putar):
    tulis(layar, "[ SINYAL MASUK ]", font_kecil, REDUP, 26, 56)
    if sedang_putar:
        titik_hijau(layar, "MENERIMA — " + sumber, 1254, 56)
    elif sumber:
        tulis(layar, "SELESAI — " + sumber, font_kecil, REDUP, 1254, 56, "kanan")

    kotak(layar, (26, 76, 1228, 176))

    # lampu sinyal, menyala selama ada nada
    if lampu:
        pygame.draw.circle(layar, (80, 54, 14), (54, 108), 15)
        pygame.draw.circle(layar, AMBER, (54, 108), 8)
    else:
        pygame.draw.circle(layar, GARIS, (54, 108), 8)

    if sunyi:
        pygame.draw.line(layar, GARIS, (90, 170), (1230, 170), 2)
        tulis(layar, "PERIODE SUNYI", font_sedang, REDUP, 660, 128, "tengah")
        return

    # titik-strip per huruf dengan hurufnya di bawah, pindah baris kalau tidak muat
    x, y = 86, 96
    for nomor, grup in enumerate(pola_masuk):
        if grup == "":
            continue
        if grup == " ":
            x += 26
            continue
        lebar = lebar_pola(grup, 10)
        if x + lebar > 1234:
            x = 86
            y += 46
        tengah = x + lebar // 2
        if nomor == len(pola_masuk) - 1:
            gambar_pola(layar, grup, x, y, AMBER, 10)       # huruf yang sedang masuk
        elif nomor in tertutup:
            gambar_pola(layar, grup, x, y, TEKS, 10)
            tulis(layar, "?", font_sedang, AMBER, tengah, y + 16, "tengah")
        else:
            gambar_pola(layar, grup, x, y, TEKS, 10)
            tulis(layar, tabel.get(grup, "?"), font_sedang, TEKS, tengah, y + 16, "tengah")
        x += lebar + 20

    if sisa_putar is not None:
        tulis(layar, "R putar ulang (sisa " + str(sisa_putar) + ")",
              font_kecil, REDUP, 1238, 228, "kanan")


# ------------------------------------------------------------ bagian tengah

def baris_peta(layar, kiri, kanan, y, warna):
    lebar_kiri = tulis(layar, kiri, font_sedang, warna, 50, y)
    lebar_kanan = font_sedang.size(kanan)[0]
    x = 50 + lebar_kiri + 12
    while x < 470 - lebar_kanan - 12:
        pygame.draw.circle(layar, GARIS, (x, y + 11), 1)
        x += 8
    tulis(layar, kanan, font_sedang, warna, 470, y, "kanan")


def gambar_peta(layar, peta, karang, tabel):
    tulis(layar, "[ CATATAN PETA ]", font_kecil, REDUP, 26, 268)
    kotak(layar, (26, 288, 800, 222))
    y = 310
    for kiri, kanan in peta:
        baris_peta(layar, kiri, kanan, y, TEKS)
        y += 32
    if karang:
        baris_peta(layar, "Awas: gugusan karang di arah", karang, y, MERAH)

    # sandi angka selalu kelihatan, jadi membalas tidak perlu buka lembar sandi
    pygame.draw.line(layar, GARIS, (496, 306), (496, 450))
    tulis(layar, "SANDI ANGKA", font_kecil, REDUP, 516, 300)
    ke_pola = {huruf: pola for pola, huruf in tabel.items()}
    for angka in range(10):
        x = 516 + (angka // 5) * 150
        y = 324 + (angka % 5) * 26
        tulis(layar, str(angka), font_sedang, TEKS, x, y)
        gambar_pola(layar, ke_pola[str(angka)], x + 22, y + 6, TEKS, 6)

    pygame.draw.line(layar, GARIS, (50, 470), (800, 470))
    tulis(layar, "Balasanmu dicatat di buku log stasiun. Apa yang kamu ketuk, itu yang tercatat.",
          font_kecil, REDUP, 50, 482)


def gambar_jendela(layar, membalas, sisa_ms, total_ms):
    tulis(layar, "[ JENDELA BALASAN ]", font_kecil, REDUP, 846, 268)
    kotak(layar, (846, 288, 408, 222))
    if not membalas:
        tulis(layar, "--:--", font_jumbo, GARIS, 1050, 330, "tengah")
        tulis(layar, "menunggu permintaan", font_kecil, REDUP, 1050, 410, "tengah")
        return

    detik = (sisa_ms + 999) // 1000
    warna = AMBER
    warna_teks = REDUP
    if detik <= 10:
        warna = MERAH
        warna_teks = MERAH
    waktu = str(detik // 60).zfill(2) + ":" + str(detik % 60).zfill(2)
    tulis(layar, waktu, font_jumbo, warna, 1050, 322, "tengah")
    pygame.draw.rect(layar, GARIS, (870, 390, 360, 6))
    pygame.draw.rect(layar, warna, (870, 390, int(360 * sisa_ms / total_ms), 6))
    tulis(layar, "Sinyal kapal melemah.", font_kecil, warna_teks, 1050, 420, "tengah")
    tulis(layar, "Setelah ini mereka tidak akan mendengarmu.", font_kecil, warna_teks, 1050, 440, "tengah")


# ------------------------------------------------------------ bagian bawah

def gambar_pemancar(layar, membalas, ditekan, isi_meter, draf, buffer, tabel):
    if membalas:
        tulis(layar, "[ PEMANCAR — AKTIF ]", font_kecil, AMBER, 26, 528)
        titik_hijau(layar, "SALURAN TERBUKA", 1254, 528)
    else:
        tulis(layar, "[ PEMANCAR — MENUNGGU GILIRAN ]", font_kecil, REDUP, 26, 528)
    kotak(layar, (26, 548, 1228, 124))

    # kunci SPASI, turun 3 piksel saat ditekan
    if ditekan:
        kotak(layar, (48, 575, 160, 58), AMBER, (58, 40, 12))
        tulis(layar, "SPASI", font_sedang, AMBER, 128, 594, "tengah")
        pygame.draw.circle(layar, AMBER, (58, 654), 5)
    else:
        kotak(layar, (48, 572, 160, 58), REDUP)
        tulis(layar, "SPASI", font_sedang, TEKS if membalas else REDUP, 128, 591, "tengah")
        pygame.draw.circle(layar, GARIS, (58, 654), 5)
    tulis(layar, "memancar", font_kecil, REDUP, 70, 646)

    # meter panjang ketukan, garis di tengah = batas strip
    tulis(layar, "PANJANG KETUKAN", font_kecil, REDUP, 232, 572)
    pygame.draw.rect(layar, GARIS, (232, 596, 130, 12))
    pygame.draw.rect(layar, AMBER, (232, 596, int(130 * isi_meter), 12))
    pygame.draw.line(layar, TEKS, (297, 590), (297, 613), 2)
    tulis(layar, "lewat garis = strip", font_kecil, HIJAU, 232, 620)

    # draf balasan: pola di atas, huruf di bawah
    tulis(layar, "DRAF BALASAN", font_kecil, REDUP, 392, 558)
    pygame.draw.rect(layar, GARIS, (392, 578, 640, 80), 1)
    grup = list(draf)
    if buffer:
        grup.append(buffer)
    if not grup:
        tulis(layar, "balasan kosong", font_sedang, REDUP, 410, 608)
    lebar = [max(lebar_pola(g, 7), 16) + 22 for g in grup]
    while sum(lebar) > 490:        # kalau kepanjangan, yang paling awal disembunyikan
        grup.pop(0)
        lebar.pop(0)
    x = 410
    for i in range(len(grup)):
        aktif = buffer and i == len(grup) - 1
        warna = AMBER if aktif else TEKS
        gambar_pola(layar, grup[i], x, 594, warna, 7)
        if aktif:
            pygame.draw.rect(layar, AMBER, (x, 614, 14, 26))
        else:
            tulis(layar, tabel.get(grup[i], "?"), font_besar, TEKS, x, 610)
        x += lebar[i]
    tersusun = ""
    for pola in draf:
        tersusun += tabel.get(pola, "?")
    tulis(layar, "tersusun:", font_kecil, REDUP, 1016, 592, "kanan")
    tulis(layar, tersusun, font_besar, TEKS, 1016, 610, "kanan")

    # tombol
    kotak(layar, (1050, 572, 184, 36))
    tulis(layar, "BACKSPACE hapus", font_kecil, TEKS if membalas else REDUP, 1142, 582, "tengah")
    if membalas and grup:
        pygame.draw.rect(layar, AMBER, (1050, 616, 184, 42))
        tulis(layar, "ENTER kirim", font_sedang, LATAR, 1142, 628, "tengah")
    else:
        kotak(layar, (1050, 616, 184, 42))
        tulis(layar, "ENTER kirim", font_sedang, REDUP, 1142, 628, "tengah")


# ------------------------------------------------------------ lembar sandi

def gambar_lembar(layar, tabel):
    redupkan(layar, (0, 0, 1280, 720), 225)
    kotak(layar, (86, 30, 1108, 660), GARIS, KERTAS)
    ke_pola = {huruf: pola for pola, huruf in tabel.items()}

    tulis(layar, "LEMBAR SANDI MORSE", font_besar, TEKS, 120, 58)
    tulis(layar, "DINAS PERHUBUNGAN LAUT — POS 12 — CETAKAN 1932", font_kecil, REDUP, 120, 98)
    tulis(layar, "ditinggalkan operator sebelumnya", font_kecil, MERAH, 1160, 98, "kanan")
    pygame.draw.line(layar, GARIS, (120, 124), (1160, 124))

    # huruf A-Z dalam tiga kolom
    for i, huruf in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        x = 122 + (i // 9) * 236
        y = 146 + (i % 9) * 28
        tulis(layar, huruf, font_sedang, TEKS, x, y)
        pola = ke_pola[huruf]
        gambar_pola(layar, pola, x + 200 - lebar_pola(pola, 7), y + 6, TEKS, 7)

    pygame.draw.line(layar, GARIS, (830, 146), (830, 628))

    tulis(layar, "ANGKA", font_kecil, REDUP, 858, 146)
    for i in range(10):
        y = 168 + i * 25
        tulis(layar, str(i), font_sedang, TEKS, 858, y)
        pola = ke_pola[str(i)]
        gambar_pola(layar, pola, 1158 - lebar_pola(pola, 7), y + 6, TEKS, 7)

    pygame.draw.line(layar, GARIS, (858, 424), (1160, 424))
    tulis(layar, "ISYARAT", font_kecil, REDUP, 858, 436)
    isyarat = [("SOS", "...---..."), ("K — ganti", "-.-"), ("AR — habis", ".-.-.")]
    for i in range(len(isyarat)):
        nama, pola = isyarat[i]
        y = 458 + i * 25
        tulis(layar, nama, font_sedang, TEKS, 858, y)
        gambar_pola(layar, pola, 1158 - lebar_pola(pola, 7), y + 6, TEKS, 7)

    # coretan operator sebelumnya
    tulis(layar, "huruf yg sering dipakai = paling", font_sedang, MERAH, 858, 548)
    tulis(layar, "pendek. E dan T cuma satu ketukan.", font_sedang, MERAH, 858, 568)
    tulis(layar, "kalau ragu, dengarkan iramanya,", font_sedang, MERAH, 858, 598)
    tulis(layar, "jangan dihitung.", font_sedang, MERAH, 858, 618)

    pygame.draw.line(layar, GARIS, (120, 642), (1160, 642))
    tulis(layar, "Selama lembar ini terbuka, kamu tidak bisa melihat sinyal masuk.",
          font_kecil, REDUP, 120, 658)
    kotak(layar, (1040, 650, 120, 28), REDUP, KERTAS)
    tulis(layar, "TAB tutup", font_kecil, TEKS, 1100, 656, "tengah")


# ------------------------------------------------------------ layar lain

def gambar_judul(layar):
    tulis(layar, "SILENT PERIOD", font_jumbo, AMBER, 640, 230, "tengah")
    tulis(layar, "STASIUN PANTAI TANJUNG — POS 12", font_kecil, REDUP, 640, 290, "tengah")
    tulis(layar, "Kabut turun tiga malam berturut-turut. Kapal-kapal hanya punya radio.",
          font_sedang, TEKS, 640, 350, "tengah")
    tulis(layar, "Kamu satu-satunya yang mendengar. Apa yang kamu ketuk, itu yang mereka terima.",
          font_sedang, TEKS, 640, 374, "tengah")
    tulis(layar, "ENTER mulai        ESC keluar", font_sedang, AMBER, 640, 450, "tengah")
    tulis(layar, "Pakai headphone. Game ini dimainkan dengan mendengar.",
          font_kecil, REDUP, 640, 650, "tengah")


def gambar_laporan(layar, malam_ke, entri_malam, putar_terpakai, putar_total):
    gambar_kepala(layar, malam_ke)
    kotak(layar, (240, 100, 800, 500))
    tulis(layar, "LAPORAN SHIFT — MALAM " + str(malam_ke), font_besar, TEKS, 280, 130)
    pygame.draw.line(layar, GARIS, (280, 176), (1000, 176))

    y = 200
    for entri in entri_malam:
        balasan = entri["balasan"] if entri["balasan"] else "tidak ada"
        tulis(layar, "Kapal", font_sedang, REDUP, 280, y)
        tulis(layar, entri["dari"], font_sedang, TEKS, 540, y)
        tulis(layar, "Balasan terkirim", font_sedang, REDUP, 280, y + 30)
        tulis(layar, balasan, font_sedang, TEKS, 540, y + 30)
        y += 60
    tulis(layar, "Putar ulang terpakai", font_sedang, REDUP, 280, y)
    tulis(layar, str(putar_terpakai) + " dari " + str(putar_total), font_sedang, TEKS, 540, y)

    tulis(layar, "CATATAN", font_kecil, REDUP, 280, 350)
    y = 374
    for entri in entri_malam:
        tulis(layar, entri["dari"] + " " + entri["nasib"] + ".", font_besar, AMBER, 280, y)
        y += 38

    tulis(layar, "ENTER lanjut ke malam " + str(malam_ke + 1), font_sedang, AMBER, 280, 548)
    gambar_status(layar, "ENTER lanjut    ESC keluar", "MALAM " + str(malam_ke) + " / 3")


def gambar_akhir(layar, catatan):
    tulis(layar, "BUKU LOG STASIUN — POS 12", font_besar, TEKS, 120, 80)
    tulis(layar, "Pagi hari. Kabut sudah naik.", font_kecil, REDUP, 120, 120)
    pygame.draw.line(layar, GARIS, (120, 150), (1160, 150))

    y = 180
    for entri in catatan:
        tulis(layar, "MALAM " + str(entri["malam"]), font_kecil, REDUP, 120, y + 2)
        if entri["nasib"] is None:
            # sinyal yang tidak ada di manifes
            tulis(layar, "sumber tidak terdaftar", font_sedang, TEKS, 220, y)
            if entri["balasan"]:
                teks = "balasan dari Pos 12: " + entri["balasan"]
            else:
                teks = "tidak ada balasan"
            tulis(layar, teks, font_sedang, AMBER, 520, y)
        else:
            balasan = entri["balasan"] if entri["balasan"] else "tidak ada"
            tulis(layar, entri["dari"], font_sedang, TEKS, 220, y)
            tulis(layar, "balasan: " + balasan, font_sedang, TEKS, 520, y)
            tulis(layar, entri["nasib"], font_sedang, TEKS, 760, y)
        y += 40

    pygame.draw.line(layar, GARIS, (120, y + 10), (1160, y + 10))
    tulis(layar, "Manifes malam itu hanya mencatat satu kapal.", font_sedang, TEKS, 120, y + 34)
    gambar_status(layar, "ENTER keluar", "POS 12")
