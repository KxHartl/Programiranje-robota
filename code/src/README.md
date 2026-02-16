# PROGRAMIRANJE ROBOTA - FANUC KAREL

**Autor:** Krešimir Hartl  
**Datum:** 2026-02-12  
**Platforma:** FANUC Roboguide + KAREL programski jezik

---

## 📚 Sadržaj

Ovo je kompletno rješenje za tri zadatka iz kolegija **Programiranje robota**:

1. **[Zadatak 1 - Paletizacija](#zadatak-1---paletizacija)** (25 bodova)
2. **[Zadatak 2 - Data Logger sa TELNET](#zadatak-2---data-logger-sa-telnet)** (15+15 bodova)
3. **[Zadatak 3 - Robotsko bušenje](#zadatak-3---robotsko-bušenje)** (25 bodova)

**Ukupno:** 80 bodova

---

## 📂 Struktura projekta

```
src/
├── zadatak_1/
│   ├── hartl_kresimir_01.kl       # KAREL program - paletizacija
│   ├── HARTL_KRESIMIR_01.ls       # TP program - gibanje
│   └── README_zadatak_1.md        # Upute za Zadatak 1
│
├── zadatak_2/
│   ├── hartl_kresimir_02_main.kl  # KAREL program - glavni
│   ├── hartl_kresimir_02_logger.kl # KAREL program - data logger
│   └── README_zadatak_2.md        # Upute za Zadatak 2
│
├── zadatak_3/
│   ├── hartl_kresimir_03.kl       # KAREL program - bušenje
│   ├── HARTL_KRESIMIR_03.ls       # TP program - izvršavanje
│   ├── KOORDINATE.txt             # Testna datoteka s koordinatama
│   └── README_zadatak_3.md        # Upute za Zadatak 3
│
└── README.md                      # Ovaj dokument
```

---

## 🎯 ZADATAK 1 - Paletizacija

### 📋 Opis
Program generira koordinate za **16 paletnih mjesta** i sprema ih u pozicijske registre PR[20]-PR[35]. Korisnik unosi ID paletnog mjesta (1-16), korisnički koordinatni sustav (8 ili 9) i brzinu izvođenja (10-100%). Nakon unosa, robot se pozicionira na odabrano mjesto.

### 📁 Datoteke
- `hartl_kresimir_01.kl` - KAREL program
- `HARTL_KRESIMIR_01.ls` - TP program

### 🎮 Funkcionalnost
- ✅ Automatsko generiranje 4×4 mreže paletnih mjesta
- ✅ Razmak: 100mm × 100mm
- ✅ User screen za unos parametara
- ✅ Validacija unosa
- ✅ Opcija zadržavanja prethodnih vrijednosti (unos `0`)
- ✅ Prekid programa (unos `999`)

### 🚀 Brzi start
```bash
1. Otvori Karel Tool → Build → Download
2. Učitaj HARTL_KRESIMIR_01.ls
3. Postavi PR[1] kao HOME poziciju
4. SELECT → KAREL → HARTL_PALETIZATION
5. Pokreni program i unesi parametre
```

📖 **[Detaljne upute →](zadatak_1/README_zadatak_1.md)**

---

## 🎯 ZADATAK 2 - Data Logger sa TELNET

### 📋 Opis
Glavni program (`hartl_main`) upravlja izvršavanjem paletizacijskog programa i data loggera koji šalje podatke o statusu robota preko TELNET veze. Podaci se šalju:
- Pri završetku gibanja robota (FLG[1]=OFF)
- Kontinuirano svakih 10ms (ako je FLG[2]=ON)

### 📁 Datoteke
- `hartl_kresimir_02_main.kl` - Glavni program
- `hartl_kresimir_02_logger.kl` - Data logger

**Napomena:** Zahtijeva programe iz Zadatka 1!

### 🎮 Funkcionalnost
- ✅ Multi-tasking s RUN_TASK
- ✅ TELNET komunikacija (CONS:)
- ✅ Slanje datum/vrijeme, TCP pozicija, zglobne pozicije
- ✅ Kontrola preko FLAG-ova
- ✅ Kontinuirano ili triggered slanje podataka

### 📊 Poslani podatci
```
- Datum i vrijeme (dan, mjesec, godina, sat, minuta, sekunda)
- FAST_CLOCK vremenska oznaka
- Aktivni UFRAME broj
- XYZ pozicija TCP-a
- WPR orijentacija
- J1-J6 zglobne pozicije
```

### 🚀 Brzi start
```bash
1. Učitaj programe iz Zadatka 1
2. Otvori Karel Tool → Build → Download (oba programa)
3. Otvori TELNET vezu ili koristi Roboguide konzolu
4. Postavi FLG[7]=ON, FLG[2]=ON/OFF
5. SELECT → KAREL → HARTL_MAIN
6. Prati podatke u TELNET konzoli
```

📖 **[Detaljne upute →](zadatak_2/README_zadatak_2.md)**

---

## 🎯 ZADATAK 3 - Robotsko bušenje

### 📋 Opis
Program čita koordinate iz datoteke **KOORDINATE.txt** i izvršava robotsko pozicioniranje i bušenje. Za svaku točku: čita X, Y, brzinu i [opcionalnu] dubinu, generira pozicije i poziva TP program za izvršavanje bušenja.

### 📁 Datoteke
- `hartl_kresimir_03.kl` - KAREL program
- `HARTL_KRESIMIR_03.ls` - TP program
- `KOORDINATE.txt` - Primjer datoteke s koordinatama

### 🎮 Funkcionalnost
- ✅ Čitanje iz MC:KOORDINATE.txt
- ✅ Parsiranje koordinata (X Y brzina [dubina])
- ✅ Default dubina 25mm ako nije navedena
- ✅ Maksimalno 200 točaka
- ✅ Automatska HOME pozicija (J5=-90°)
- ✅ Pozicioniranje: JOINT move iznad + LINEAR move na točku

### 📄 Format datoteke
```
150 200 300 50      # X Y brzina dubina
200 300 200 20      # X Y brzina dubina
100 100 150         # X Y brzina (default dubina 25mm)
-131.1 -133 211 25
310.15 0 100
161 155 12 40
-50.13 120.15 150
```

### 🚀 Brzi start
```bash
1. Kopiraj KOORDINATE.txt na MC: device
2. Otvori Karel Tool → Build → Download
3. Učitaj HARTL_KRESIMIR_03.ls
4. SELECT → KAREL → HARTL_DRILLING
5. Program čita datoteku i izvršava bušenje
```

📖 **[Detaljne upute →](zadatak_3/README_zadatak_3.md)**

---

## 🛠️ Opće upute za korištenje

### Preduvjeti

#### Software:
- **FANUC Roboguide** (verzija 9.0 ili novija)
- **Karel Tool** (uključen u Roboguide)

#### Robot model:
- **M-10iA** ili kompatibilan model
- 6-osni industrijski robot

### Učitavanje programa u Roboguide

#### 1. KAREL programi (.kl datoteke)

```bash
1. Tools → Karel Tool
2. File → Open → Odaberi .kl datoteku
3. Build → Build (kompajliranje)
4. Provjeri Output prozor za greške
5. Build → Download to Robot
6. Program je sada u kontroleru (.PC datoteka)
```

#### 2. TP programi (.ls datoteke)

```bash
1. TP Program List (u Roboguide glavnom prozoru)
2. Edit → Load Program from File
3. Odaberi .ls datoteku
4. Program se učitava u kontroler
```

### Pokretanje KAREL programa

```bash
1. Postavi robot u TEST mod: [SHIFT] + [FWD]
2. Menu → SELECT
3. Program Type → KAREL
4. Odaberi program iz liste
5. [SHIFT] + [FWD] za pokretanje
```

### Debugging

#### Prikaz outputa:
```bash
Menu → STATUS → Program Status
ili
Tools → WinOLPC Console (u Roboguide-u)
```

#### Provjera registara:
```bash
Menu → Data → Position Reg (pozicijski registri)
Menu → Data → Number Reg (brojčani registri)
Menu → Data → Flag (flagovi)
```

---

## 🔧 Registri i resursi

### Position Registers (PR)

| Registar | Zadatak | Opis |
|----------|---------|------|
| PR[1] | 1, 3 | HOME pozicija |
| PR[10] | 3 | Pozicija iznad točke bušenja |
| PR[11] | 3 | Pozicija bušenja |
| PR[20-35] | 1, 2 | Paletna mjesta #1-16 |

### Number Registers (R)

| Registar | Zadatak | Opis |
|----------|---------|------|
| R[1] | 1, 2 | Brzina izvođenja [%] |
| R[2] | 1, 2 | ID pozicijskog registra |
| R[3] | 1, 2 | Broj UFRAME-a |
| R[10] | 3 | Brzina bušenja [mm/s] |

### Flagovi (FLG)

| Flag | Zadatak | Opis |
|------|---------|------|
| FLG[1] | 2 | Detekcija pokreta robota |
| FLG[2] | 2 | Kontinuirano slanje podataka |
| FLG[7] | 2 | Kontrola glavne petlje |
| FLG[10] | 2, 3 | Interni kontrolni flag |
| FLG[20] | 2 | Header ispis (data logger) |

---

## 🐛 Troubleshooting

### Problem: "Program not found"
**Rješenje:**
- Provjeri je li program kompajliran i downloadan
- Provjeri ime programa u KAREL kodu (CONST TP_PROGRAM_NAME)
- Ponovno učitaj .ls program

### Problem: "File not found - KOORDINATE.txt"
**Rješenje:**
- Kopiraj datoteku na MC: device
- Provjeri ime datoteke (velika slova!)
- Path: `MC:KOORDINATE.txt`

### Problem: Robot se ne pomiče
**Rješenje:**
- Provjeri je li robot u TEST modu
- Menu → Setup → Controlled Start → Enable robot
- Provjeri soft limits

### Problem: "Invalid Configuration"
**Rješenje:**
- Promijeni `CNV_STR_CONF('NUT000', ...)` na odgovarajuću konfiguraciju
- Provjeri: Menu → Utility → Vision → Config browser

### Problem: TELNET ne pokazuje podatke
**Rješenje:**
- Koristi Roboguide WinOLPC Console
- Provjeri IP adresu kontrolera
- Provjeri je li FLAG[7]=ON i FLAG[10]=ON

---

## 📝 Kodne konvencije

### Imenovanje varijabli
- **Engleski jezik** za sve nazive varijabli
- **snake_case** za varijable: `drill_speed`, `point_counter`
- **UPPER_CASE** za konstante: `MAX_POINTS`, `DEFAULT_DEPTH`

### Komentari
- **Hrvatski jezik** za sve komentare
- Svaki program ima header s opisom zadatka
- Svaka sekcija označena separatorom: `-- ===...===`

### Struktura
```karel
PROGRAM naziv
%DIREKTIVE

CONST
    -- Konstante

VAR
    -- Varijable

BEGIN
    -- === SEKCIJA 1 ===
    -- Kod...
    
    -- === SEKCIJA 2 ===
    -- Kod...
    
END naziv
```

---

## ✅ Checklist za predaju

### Zadatak 1:
- [ ] `hartl_kresimir_01.kl` kompajliran
- [ ] `HARTL_KRESIMIR_01.ls` učitan
- [ ] Testiran s različitim parametrima
- [ ] Validacija unosa radi ispravno

### Zadatak 2:
- [ ] `hartl_kresimir_02_main.kl` kompajliran
- [ ] `hartl_kresimir_02_logger.kl` kompajliran
- [ ] TELNET veza testirana
- [ ] Oba moda rada testirana (kontinuirano/triggered)

### Zadatak 3:
- [ ] `hartl_kresimir_03.kl` kompajliran
- [ ] `HARTL_KRESIMIR_03.ls` učitan
- [ ] `KOORDINATE.txt` kopiran na MC:
- [ ] Testirano s primjer podacima

### Dokumentacija:
- [ ] README.md (glavni)
- [ ] README_zadatak_1.md
- [ ] README_zadatak_2.md
- [ ] README_zadatak_3.md

---

## 📞 Kontakt i podrška

Za pitanja i podršku:
- **Email:** kresimir.hartl@fsb.hr (izmisljena adresa)
- **GitHub:** (link ako postoji)

---

## 📜 Licenca

Ovaj projekt je kreiran u svrhu edukacije za kolegij **Programiranje robota** na FSB-u.

---

## 🙏 Zahvale

Zahvale kolegama čija su rješenja poslužila kao referenca:
- Ivan Noršić
- Antonio Ćuk

Njihovi primjeri su bili korisni za razumijevanje strukture i funkcionalnosti programa.

---

**Kreirano:** 2026-02-12  
**Verzija:** 1.0  
**Status:** ✅ Kompletno
