# Silent Period
# Dengar Morse, terjemahkan sendiri, lalu ketuk balasan pakai Spasi.

import array
import math
import random

import pygame

import tampilan
from malam import MALAM
from morse import MORSE, SANDI_MALAM_3, cek_balasan, ke_jadwal, terjemahkan

AMBANG_STRIP = 200   # ms, Spasi ditahan selama ini atau lebih = strip
JEDA_HURUF = 700     # ms, berhenti mengetuk selama ini = huruf selesai

# ------------------------------------------------------------ variabel game

state = "JUDUL"          # JUDUL, MENERIMA, MEMBALAS, LAPORAN, AKHIR
jalan = True
lembar_terbuka = False

malam_ke = 1
data_malam = None
urutan = []              # isi malam ini (pesan, sunyi, minta)
indeks = -1              # posisi di urutan
tunggu_sampai = None     # kalau diisi, tunggu sampai waktu ini lalu lanjut
sunyi_sampai = None      # kalau diisi, sedang periode sunyi
catatan = []             # buku log: semua balasan pemain
frame_lalu = 0

# pesan masuk
jadwal = []
jadwal_indeks = 0
waktu_event = 0          # kapan bunyi/jeda yang sekarang dimulai
sedang_putar = False
pola_masuk = []          # titik-strip yang sudah masuk, satu string per huruf
tertutup = []            # nomor huruf yang tertutup derau (tampil sebagai ?)
sumber = ""

# membalas
draf = []                # pola yang sudah jadi huruf
buffer = ""              # pola huruf yang sedang diketuk
mulai_tekan = None       # kapan Spasi mulai ditekan (None = tidak ditekan)
terakhir_lepas = 0
batas_balas = 0
putar_ulang_sisa = 0

# diisi di siapkan()
layar = None
jam = None
nada_masuk = None
nada_ketuk = None
desis = None
channel_masuk = None
channel_ketuk = None


# ------------------------------------------------------------ suara

def buat_nada(frekuensi, kekuatan):
    # 1 detik gelombang sinus. Frekuensinya bulat, jadi bisa diulang tanpa putus.
    sampel = array.array("h")
    for i in range(44100):
        sampel.append(int(math.sin(2 * math.pi * frekuensi * i / 44100) * 32767 * kekuatan))
    return pygame.mixer.Sound(buffer=sampel)


def buat_desis(kekuatan):
    sampel = array.array("h")
    for i in range(44100):
        sampel.append(int(random.uniform(-1, 1) * 32767 * kekuatan))
    return pygame.mixer.Sound(buffer=sampel)


def atur_desis(nyala):
    if nyala:
        desis.set_volume(1)
    else:
        desis.set_volume(0)


def siapkan():
    global layar, jam, nada_masuk, nada_ketuk, desis, channel_masuk, channel_ketuk
    # harus sebelum pygame.init() supaya bunyi tidak telat
    pygame.mixer.pre_init(44100, -16, 1, 512, allowedchanges=0)
    pygame.init()
    layar = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Silent Period")
    jam = pygame.time.Clock()
    tampilan.siapkan_font()

    nada_masuk = buat_nada(600, 0.25)
    nada_ketuk = buat_nada(500, 0.25)
    desis = buat_desis(0.03)
    channel_masuk = pygame.mixer.Channel(0)
    channel_ketuk = pygame.mixer.Channel(1)
    pygame.mixer.Channel(2).play(desis, loops=-1)


# ------------------------------------------------------------ alur malam

def mulai_malam(nomor):
    global state, malam_ke, data_malam, urutan, indeks, putar_ulang_sisa
    global tunggu_sampai, pola_masuk, sumber, lembar_terbuka
    malam_ke = nomor
    data_malam = MALAM[nomor - 1]
    urutan = list(data_malam["urutan"])   # salinan, karena nanti disisipi pesan akibat
    indeks = -1
    putar_ulang_sisa = data_malam["putar_ulang"]
    pola_masuk = []
    sumber = ""
    lembar_terbuka = False
    state = "MENERIMA"
    atur_desis(True)
    tunggu_sampai = pygame.time.get_ticks() + 2500


def lanjut():
    """Pindah ke isi urutan berikutnya."""
    global indeks, sunyi_sampai, sumber, pola_masuk
    indeks += 1
    if indeks >= len(urutan):
        selesai_malam()
        return
    isi = urutan[indeks]
    if isi["jenis"] == "sunyi":
        atur_desis(False)
        sunyi_sampai = pygame.time.get_ticks() + isi["detik"] * 1000
        pola_masuk = []
        sumber = ""
    else:
        atur_desis(not isi.get("lemah", False))
        sumber = isi.get("dari", data_malam["kapal"])
        putar_pesan(isi)


def selesai_malam():
    global state, lembar_terbuka
    lembar_terbuka = False
    atur_desis(True)
    if malam_ke < len(MALAM):
        state = "LAPORAN"
    else:
        state = "AKHIR"


# ------------------------------------------------------------ pesan masuk

def putar_pesan(isi):
    global jadwal, jadwal_indeks, waktu_event, sedang_putar, pola_masuk, tertutup
    jadwal = ke_jadwal(isi["teks"], data_malam["satuan"])
    jadwal_indeks = 0
    waktu_event = pygame.time.get_ticks()
    sedang_putar = True
    pola_masuk = [""]
    tertutup = []
    if isi.get("lemah", False):
        nada_masuk.set_volume(0.35)
    else:
        nada_masuk.set_volume(1)
    mulai_bunyi()


def mulai_bunyi():
    jenis = jadwal[jadwal_indeks][0]
    if jenis == "titik" or jenis == "strip":
        channel_masuk.play(nada_masuk, loops=-1)
    else:
        channel_masuk.stop()


def update_pesan():
    global jadwal_indeks, waktu_event, sedang_putar
    while sedang_putar:
        jenis, lama = jadwal[jadwal_indeks]
        if pygame.time.get_ticks() - waktu_event < lama:
            return
        # bunyi/jeda ini sudah selesai. Simbol baru muncul setelah bunyinya habis.
        waktu_event += lama
        if jenis == "titik":
            pola_masuk[-1] += "."
        elif jenis == "strip":
            pola_masuk[-1] += "-"
        elif jenis == "huruf":
            # sebagian huruf tertutup derau, titik-stripnya tetap terlihat
            if random.random() < data_malam["derau"]:
                tertutup.append(len(pola_masuk) - 1)
            pola_masuk.append("")
        elif jenis == "spasi":
            pola_masuk[-1] = " "
            pola_masuk.append("")
        jadwal_indeks += 1
        if jadwal_indeks >= len(jadwal):
            sedang_putar = False
            channel_masuk.stop()
            pesan_selesai()
        else:
            mulai_bunyi()


def pesan_selesai():
    global tunggu_sampai
    if state == "MEMBALAS":        # selesai diputar ulang, tetap membalas
        return
    if urutan[indeks]["jenis"] == "minta":
        mulai_membalas()
    else:
        tunggu_sampai = pygame.time.get_ticks() + 2000


# ------------------------------------------------------------ membalas

def mulai_membalas():
    global state, draf, buffer, mulai_tekan, batas_balas
    state = "MEMBALAS"
    draf = []
    buffer = ""
    mulai_tekan = None
    batas_balas = pygame.time.get_ticks() + data_malam["waktu_balas"] * 1000


def selesai_membalas(hasil):
    global state, tunggu_sampai, mulai_tekan, sedang_putar, draf, buffer
    isi = urutan[indeks]
    mulai_tekan = None           # kalau Spasi masih ditahan, dilepas tanpa menambah simbol
    channel_ketuk.stop()
    sedang_putar = False         # kalau sedang diputar ulang, dihentikan
    channel_masuk.stop()

    balasan = ""
    if hasil != "diam":
        balasan = terjemahkan(draf)    # yang benar-benar terkirim, pakai tabel asli
    nasib = None
    if "nasib" in isi:
        nasib = isi["nasib"][hasil]
    catatan.append({"malam": malam_ke, "dari": sumber, "balasan": balasan, "nasib": nasib})
    draf = []
    buffer = ""

    # sisipkan pesan akibat supaya diputar berikutnya
    posisi = indeks + 1
    for teks in isi.get(hasil, []):
        urutan.insert(posisi, {"jenis": "pesan", "teks": teks, "dari": sumber,
                               "lemah": isi.get("lemah", False)})
        posisi += 1

    state = "MENERIMA"
    tunggu_sampai = pygame.time.get_ticks() + 1500


def tekan_spasi():
    global mulai_tekan
    if mulai_tekan is None and not sedang_putar:
        mulai_tekan = pygame.time.get_ticks()
        channel_ketuk.play(nada_ketuk, loops=-1)


def lepas_spasi():
    global buffer, mulai_tekan, terakhir_lepas
    if mulai_tekan is None:
        return
    lama = pygame.time.get_ticks() - mulai_tekan
    buffer += "-" if lama >= AMBANG_STRIP else "."
    terakhir_lepas = pygame.time.get_ticks()
    mulai_tekan = None
    channel_ketuk.stop()


def tombol_membalas(tombol):
    global buffer, mulai_tekan, putar_ulang_sisa
    if tombol == pygame.K_SPACE:
        tekan_spasi()
    elif tombol == pygame.K_BACKSPACE:
        if buffer:
            buffer = buffer[:-1]
        elif draf:
            draf.pop()
    elif tombol == pygame.K_RETURN:
        if buffer:
            draf.append(buffer)
            buffer = ""
        if draf:
            selesai_membalas(cek_balasan(draf, urutan[indeks]["jawaban"]))
    elif tombol == pygame.K_r:
        if putar_ulang_sisa > 0 and not sedang_putar:
            putar_ulang_sisa -= 1
            mulai_tekan = None
            channel_ketuk.stop()
            putar_pesan(urutan[indeks])


# ------------------------------------------------------------ loop

def proses_event(event):
    global jalan, lembar_terbuka
    if event.type == pygame.QUIT:
        jalan = False
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            jalan = False
        elif event.key == pygame.K_TAB and (state == "MENERIMA" or state == "MEMBALAS"):
            lembar_terbuka = not lembar_terbuka
        elif event.key == pygame.K_RETURN and state == "JUDUL":
            mulai_malam(1)
        elif event.key == pygame.K_RETURN and state == "LAPORAN":
            mulai_malam(malam_ke + 1)
        elif event.key == pygame.K_RETURN and state == "AKHIR":
            jalan = False
        elif state == "MEMBALAS":
            tombol_membalas(event.key)
    elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
        lepas_spasi()


def update():
    global tunggu_sampai, sunyi_sampai, buffer, batas_balas, frame_lalu
    sekarang = pygame.time.get_ticks()
    selisih = sekarang - frame_lalu
    frame_lalu = sekarang
    if state == "MENERIMA":
        if tunggu_sampai is not None:
            if sekarang >= tunggu_sampai:
                tunggu_sampai = None
                lanjut()
        elif sunyi_sampai is not None:
            if sekarang >= sunyi_sampai:
                sunyi_sampai = None
                lanjut()
        elif sedang_putar:
            update_pesan()
    elif state == "MEMBALAS":
        if sedang_putar:
            update_pesan()
            batas_balas += selisih     # waktu balas berhenti selama diputar ulang
        # huruf selesai kalau pemain berhenti mengetuk cukup lama
        if buffer and mulai_tekan is None and sekarang - terakhir_lepas >= JEDA_HURUF:
            draf.append(buffer)
            buffer = ""
        if sekarang >= batas_balas:
            selesai_membalas("diam")


def gambar():
    layar.fill(tampilan.LATAR)
    if state == "JUDUL":
        tampilan.gambar_judul(layar)
    elif state == "LAPORAN":
        entri_malam = [e for e in catatan if e["malam"] == malam_ke]
        terpakai = data_malam["putar_ulang"] - putar_ulang_sisa
        tampilan.gambar_laporan(layar, malam_ke, entri_malam, terpakai, data_malam["putar_ulang"])
    elif state == "AKHIR":
        tampilan.gambar_akhir(layar, catatan)
    else:
        gambar_meja()


def gambar_meja():
    sekarang = pygame.time.get_ticks()
    membalas = state == "MEMBALAS"
    tabel = SANDI_MALAM_3 if data_malam["lembar_salah"] else MORSE
    lampu = sedang_putar and jadwal[jadwal_indeks][0] in ("titik", "strip")
    sisa_putar = putar_ulang_sisa if membalas else None
    isi_meter = 0
    if mulai_tekan is not None:
        isi_meter = min((sekarang - mulai_tekan) / (AMBANG_STRIP * 2), 1)

    tampilan.gambar_kepala(layar, malam_ke)
    tampilan.gambar_sinyal(layar, sumber, pola_masuk, tertutup, tabel, sedang_putar, lampu,
                           sunyi_sampai is not None, sisa_putar)
    tampilan.gambar_peta(layar, data_malam["peta"], data_malam["karang"], tabel)
    tampilan.gambar_jendela(layar, membalas, max(batas_balas - sekarang, 0),
                            data_malam["waktu_balas"] * 1000)
    tampilan.gambar_pemancar(layar, membalas, mulai_tekan is not None, isi_meter,
                             draf, buffer, tabel)

    # bagian yang bukan giliran pemain dibuat redup
    if membalas:
        tampilan.redupkan(layar, (0, 50, 1280, 206), 90)
        petunjuk = ("TAB lembar sandi    SPASI ketuk (tahan = strip)    BACKSPACE hapus    "
                    "ENTER kirim    R putar ulang (sisa " + str(putar_ulang_sisa) + ")")
    else:
        tampilan.redupkan(layar, (0, 520, 1280, 160), 170)
        petunjuk = "TAB lembar sandi    SPASI ketuk (nonaktif saat menerima)    ESC keluar"
    tampilan.gambar_status(layar, petunjuk, "MALAM " + str(malam_ke) + " / 3")

    if lembar_terbuka:
        tampilan.gambar_lembar(layar, tabel)


def main():
    siapkan()
    while jalan:
        for event in pygame.event.get():
            proses_event(event)
        update()
        gambar()
        pygame.display.flip()
        jam.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
