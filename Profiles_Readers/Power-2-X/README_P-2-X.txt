# Power-to-X (P2X Plant) — Annual Profiles

## 1. Overview

Ovaj skup podataka opisuje godišnje profile:
- neupravljive potrošnje **električne energije**
- ukupne **potrošnje vode**

za **Power-to-X (P2X)** postrojenje srednje veličine, koje koristi elektrolizu za proizvodnju vodika te sintezu metana/metanola.

Svi profili su uzorkovani u **15-minutnim intervalima** kroz cijelu 2024. godinu.

---

## 2. Files

### 2.1. Electricity — Non-controllable Load

**Filename:** `noncontrollable_load_annual_profile_Power-2-X.csv`

**Columns:**

| Column                     | Unit | Description                                  |
|---------------------------|------|----------------------------------------------|
| `timestamp`               | –    | Date and time (`%d.%m.%Y %H:%M`)             |
| `Electricity demand (kWh)`| kWh  | Energy consumed in that 15-min interval      |

**Assumptions:**

- Tehnologija: **PEM elektrolizator + kompresija + pomoćni sustavi**
- Instalirana snaga: **5 MW**
- Godišnji faktor iskorištenja: **55 %**
- Ukupna godišnja potrošnja:  
  \[
  5\ \text{MW} × 8760\ \text{h} × 0.55 = 24\,090\ \text{MWh} = 24.1\ \text{GWh}
  \]
- Profil uključuje:
  - kontinuiran rad tijekom dana (djelomična regulacija snage),
  - nižu potrošnju noću (održavanje, standby),
  - lagane fluktuacije radi simulacije dinamičnog opterećenja.

**Daily pattern:**

- noću (0–5 h): ~40–50 % opterećenja  
- danju (6–22 h): 80–100 % opterećenja  
- vikendom: blago smanjeno (~90 %)

**Result:**

- **Ukupna godišnja potrošnja električne energije:** **≈ 24,1 GWh**

---

### 2.2. Water — Total Demand

**Filename:** `water_demand_annual_profile_Power-2-X.csv`

**Columns:**

| Column            | Unit | Description                                  |
|------------------|------|----------------------------------------------|
| `timestamp`      | –    | Date and time (`%d.%m.%Y %H:%M`)             |
| `Water demand (m3)` | m³ | Water volume consumed in that 15-min interval |

**Assumptions and Benchmark:**

- Elektroliza troši približno **9 L vode/kg H₂**  
- 1 MW elektrolize (24 h rada) proizvodi ≈ **21,6 kg H₂/h** → ~194 L/h po MW
- Za 5 MW sustav:
  \[
  5 × 194 = 970\ \text{L/h} = 0.97\ \text{m³/h}
  \]
- Prosječna dnevna potrošnja: **≈ 23 m³/dan**
- Godišnja potrošnja:
  \[
  23 × 365 ≈ 8 395\ \text{m³/god}
  \]

**Daily pattern:**

- konstantan rad tijekom većeg dijela dana (6–22 h),
- manji protok noću (0–5 h) tijekom održavanja,
- vikendom minimalne oscilacije.

**Result:**

- **Ukupna godišnja potrošnja vode:** **≈ 8 400 m³**

---

## 3. Intended Use

Ovi profili su namijenjeni za:

- modeliranje **energetskih tokova u P2X sustavima**,  
- analize **fleksibilnosti** i **integracije s obnovljivim izvorima**,  
- simulacije **elektrolize, sinteze metana/metanola**,  
- optimizaciju rada u **Multi-Energy System** modelima (MILP, MPC).

Profili su **sintetički**, ali su kalibrirani prema poznatim tehničkim podacima o:
- potrošnji vode u PEM/alkalnim elektrolizerima,
- dinamičkom profilu potrošnje električne energije u P2X pogonima.

---

## 4. References (Literatura)

1. **Fraunhofer ISE (2022)** — *Hydrogen Production via Electrolysis: Efficiency and Water Consumption Benchmarks*  
   [https://www.ise.fraunhofer.de](https://www.ise.fraunhofer.de)

2. **IEA (2023)** — *The Future of Electrolytic Hydrogen Production*  
   [https://www.iea.org/reports/the-future-of-electrolytic-hydrogen-production](https://www.iea.org/reports/the-future-of-electrolytic-hydrogen-production)

3. **Hydrogen Europe (2024)** — *Water and Energy Requirements for Hydrogen Production*,  
   Technical Briefing Paper.

4. **EU Clean Hydrogen Partnership (2023)** — *Life Cycle Analysis of Electrolytic Hydrogen Plants*.

5. **US Department of Energy (2021)** — *DOE Hydrogen Program: Electrolyzer Technology Review*  
   [https://www.energy.gov/eere/fuelcells/hydrogen-production](https://www.energy.gov/eere/fuelcells/hydrogen-production)

---

## 5. Notes

- U profilu nisu uključene potrebe za hlađenjem, cirkulacijom elektrolita i recikliranjem vode — ti procesi mogu povećati ukupnu potrošnju za 10–20 %.  
- Električna potrošnja uključuje samo *core* opterećenja (elektrolizer + kompresija + BOP).  
- Za simulacije u Multi-Energy modelima preporučuje se dodati fleksibilnost ±10 % u operativnim satima.

---

**Autor:** Generirano pomoću GPT-5 (OpenAI, 2025)  
**Datum:** 05.11.2025.
