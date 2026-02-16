# ZADATAK 3 - ROBOTSKO BUŠENJE

## 📋 Opis zadatka

Program učitava koordinate iz datoteke **KOORDINATE.txt** i izvršava robotsko pozicioniranje i bušenje na svakoj točki.

### Funkcionalnost:
1. Čita datoteku s koordinatama i parametrima bušenja
2. Za svaku liniju parsira: **X, Y, brzina, [dubina]**
3. Pozicionira robota iznad točke (Z=500mm)
4. Buši na zadanu dubinu (default 25mm)
5. Vraća se iznad i nastavlja na sljedeću točku

## 📁 Datoteke

- **`hartl_kresimir_03.kl`** - KAREL program (glavna logika)
- **`HARTL_KRESIMIR_03.ls`** - TP program (izvršavanje bušenja)
- **`KOORDINATE.txt`** - Datoteka s koordinatama (primjer)
- **`README_zadatak_3.md`** - Ovaj dokument s uputama

## 📄 Format datoteke KOORDINATE.txt

### Struktura linije:
```
X Y brzina [dubina]
```

### Parametri:
- **X** - X koordinata [mm]
- **Y** - Y koordinata [mm]
- **brzina** - Brzina bušenja [mm/s]
- **dubina** - Dubina bušenja [mm] - **OPCIONO**, default je 25mm

### Primjer datoteke:
```
150 200 300 50
200 300 200 20
100 100 150
-131.1 -133 211 25
310.15 0 100
161 155 12 40
-50.13 120.15 150
```

### Ograničenja:
- **Maksimalno 200 točaka** u datoteci
- Razmaci između brojeva: **space separator**
- Prazni redovi se *preskakaju*
- Redovi s manje od 3 parametra se *preskakaju*

## 🎯 Način rada programa

### 1. Inicijalizacija
- Postavljanje HOME pozicije (J5=-90°)
- Spremanje u PR[1]
- Pomak robota na HOME

### 2. Čitanje datoteke
- Otvaranje `MC:KOORDINATE.txt`
- Čitanje linija znak po znak
- Parsiranje brojeva (X, Y, brzina, dubina)

### 3. Za svaku točku:
```
a) Postavljanje pozicija:
   - PR[10] = Iznad točke (X, Y, Z=500mm)
   - PR[11] = Točka bušenja (X, Y, Z=500-dubina)

b) Postavljanje brzine:
   - R[10] = brzina [mm/s]

c) Pokretanje TP programa:
   - HARTL_KRESIMIR_03 izvršava bušenje
```

### 4. Završetak
- Zatvaranje datoteke
- Povratak u HOME poziciju
- Ispis broja obrađenih točaka

## 🚀 Korištenje u Roboguide

### 1. PRIPREMA DATOTEKE

#### Opcija A: Ručno kreiranje u kontroleru
1. **Virtual Robot Controller** → Menu
2. **FILE → File Utilities**
3. **Device → Memory Card (MC:)**
4. **[UTIL] → Create File**
5. Ime: `KOORDINATE.txt`
6. **Edit** → Unesi podatke:
   ```
   150 200 300 50
   200 300 200 20
   100 100 150
   ```
7. Spremi i izađi

#### Opcija B: Kopiranje datoteke
1. Pronađi Roboguide MC folder:
   ```
   C:\Users\[USER]\AppData\Local\FANUC\WinOLPC\[Cell Name]\MC\
   ```
2. Kopiraj `KOORDINATE.txt` u taj folder
3. Restartaj Roboguide (ili Refresh u File Utilities)

### 2. UČITAVANJE PROGRAMA

#### A) KAREL program
1. **Tools → Karel Tool**
2. **File → Open** → `hartl_kresimir_03.kl`
3. **Build → Build**
4. **Build → Download to Robot**
5. Program se učitava kao **HARTL_DRILLING.PC**

#### B) TP program
1. **TP Program List**
2. **Edit → Load Program from File**
3. Odaberi `HARTL_KRESIMIR_03.ls`

### 3. PROVJERA PRIJE POKRETANJA

#### ✅ Checklist:
- [ ] Datoteka `KOORDINATE.txt` postoji na **MC:** uređaju
- [ ] KAREL program učitan i kompajliran
- [ ] TP program učitan
- [ ] Robot u TEST modu
- [ ] Group 1 enabled

### 4. POKRETANJE PROGRAMA

#### TEST mod:
1. Drži **[SHIFT]** + **[FWD]** (uključi TEST mod)
2. **Menu → SELECT**
3. **Program Type: KAREL**
4. Odaberi **HARTL_DRILLING**
5. **[SHIFT] + [FWD]** za pokretanje

#### Output na konzoli:
```
========================================
   ROBOTSKO BUSENJE - HARTL
========================================

Pomak na HOME poziciju...
Robot u HOME poziciji.

Otvaranje datoteke: MC:KOORDINATE.txt
Datoteka uspjesno otvorena.

--- PARSIRANJE DATOTEKE ---
[ 1] X=  150.00 Y=  200.00 V= 300.00 D=  50.00
[ 2] X=  200.00 Y=  300.00 V= 200.00 D=  20.00
[ 3] X=  100.00 Y=  100.00 V= 150.00 D=  25.00 (DEFAULT)
[ 4] X= -131.10 Y= -133.00 V= 211.00 D=  25.00
[ 5] X=  310.15 Y=    0.00 V= 100.00 D=  25.00 (DEFAULT)
[ 6] X=  161.00 Y=  155.00 V=  12.00 D=  40.00
[ 7] X=  -50.13 Y=  120.15 V= 150.00 D=  25.00 (DEFAULT)

--- BUSENJE ZAVRSENO ---
Ukupno obradeno tocaka: 7

Povratak u HOME poziciju...
Robot u HOME poziciji.
Program zavrsen.
```

### 5. ANIMACIJA U 3D PRIKAZU

Prati robota u Roboguide 3D prozoru:
1. Robot ide na HOME (J5=-90°)
2. Za svaku točku:
   - Pomak IZNAD točke (Z=500mm) - JOINT move
   - Spuštanje na točku (LINEAR move)
   - Povratak GORE (LINEAR move)
3. Povratak u HOME

## 🔧 Registri

### Position Registers (PR)
- **PR[1]** - HOME pozicija (postavlja program automatski)
- **PR[10]** - Pozicija iznad točke (approach)
- **PR[11]** - Pozicija bušenja (drill)

### Number Registers (R)
- **R[10]** - Brzina bušenja [mm/s]

## ⚙️ Prilagodba parametara

### Promjena default dubine

U KAREL programu:
```karel
CONST
    DEFAULT_DEPTH = 25.0  -- Promijeni na željenu vrijednost [mm]
```

### Promjena visine pristupa

```karel
CONST
    APPROACH_HEIGHT = 500  -- Visina iznad točke [mm]
```

### Promjena maksimalnog broja točaka

```karel
CONST
    MAX_POINTS = 200  -- Povećaj ako treba više točaka
```

### Promjena konfiguracije robota

```karel
CNV_STR_CONF('NUT000', robot_config, status)
-- Promijeni 'NUT000' na odgovarajuću konfiguraciju
-- Npr: 'FUT000', 'NUT001', itd.
```

## 🐛 Mogući problemi

### Problem: "File not found - KOORDINATE.txt"
**Rješenje:**
- Provjeri je li datoteka u **MC:** folderu
- Ime mora biti točno `KOORDINATE.txt` (velika slova)
- Provjeri putanju u CONST dijelu KAREL programa

### Problem: "Program HARTL_KRESIMIR_03 not found"
**Rješenje:**
- Učitaj .ls program u TP Program List
- Provjeri ime programa u .ls datoteci

### Problem: Robot se ne pomiče ili SRVO alarm
**Rješenje:**
- Provjeri je li robot u TEST modu
- Provjeri je li Group 1 enabled: **Menu → Setup → Controlled Start**
- Provjeri soft limits i radno područje

### Problem: "Invalid Configuration NUT000"
**Rješenje:**
- Provjeri dostupne konfiguracije: **Menu → Utility → Vision → Config browser**
- Promijeni u KAREL programu na odgovarajuću

### Problem: Pozicije izvan dosega
**Rješenje:**
- Prilagodi koordinate u KOORDINATE.txt
- Za M-10iA, ograničenja su otprilike:
  - X: ±1100mm
  - Y: ±1100mm
  - Z: 0-1400mm

### Problem: Parsiranje ne radi (preskaču se linije)
**Rješenje:**
- Provjeri da su brojevi razdvojeni **space karakterom**
- Ukloni tabulatore i extra praznine
- Svaka linija mora imati barem 3 broja (X, Y, brzina)

## 📊 Shema pozicioniranja

```
        ↑ Z
        |
        |   Approach (PR[10])
        |   Z = 500mm
        |        ↓
        |        ↓ LINEAR (brzina iz datoteke)
        |        ↓
        |   Drill (PR[11])
        |   Z = 500 - dubina
        |        ↑
        |        ↑ LINEAR (200 mm/s)
        |        ↑
        +--------+-------→ X,Y
         (X, Y iz datoteke)
```

## 📝 Napomene

- **HOME pozicija:** Automatski se postavlja, ne treba ručno definirati PR[1]
- **Konfiguracija:** NUT000 = No flip, Elbow Up, Tool up, Turn 0
- **Brzina pristupa:** Joint move, 100% brzine
- **Brzina bušenja:** LINEAR move, iz datoteke
- **Brzina povratka:** LINEAR move, 200 mm/s (fixed)
- **UFRAME:** Koristi se UFRAME[0] (world coordinates)
- **UTOOL:** Koristi se UTOOL[0] (TCP na flanši)

## 🧪 TEST podatci

Za testiranje, koristi primjer `KOORDINATE.txt`:
```
150 200 300 50
200 300 200 20
100 100 150
-131.1 -133 211 25
310.15 0 100
161 155 12 40
-50.13 120.15 150
```

**Očekivani rezultat:**
- 7 točaka obrađeno
- 3 točke s default dubinom (25mm)
- 4 točke s custom dubinom

## 💡 Napredne mogućnosti

### Dodavanje tool offseta

U TP programu dodaj:
```
3:  TOOL_OFFSET,PR[11]=PR[20]    ;
```

### Dodavanje pauze nakon bušenja

U TP programu dodaj:
```
7:  DELAY 500    ;  -- Pauza 500ms
```

### Promjena orijentacije alata

U ROUTINE `drill_at_point`:
```karel
approach_pos.W = 0    -- Promijeni orijentaciju
approach_pos.P = 0
approach_pos.R = 90   -- Npr. alat pod 90°
```

---

**Autor:** Krešimir Hartl  
**Datum:** 2026-02-12  
**Zadatak:** Roboguide-FANUC Zadatak 3 - Robotsko bušenje
