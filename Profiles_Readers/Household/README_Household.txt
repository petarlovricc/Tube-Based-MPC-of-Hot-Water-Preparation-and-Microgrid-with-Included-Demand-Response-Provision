# Household (4-person Home) — Annual Profiles

## 1. Overview

Ovaj skup podataka opisuje godišnje profile:
- neupravljive potrošnje **električne energije**
- ukupne **potrošnje tople vode**

za **standardno kućanstvo s 4 osobe**.

Svi profili su uzorkovani u **15-minutnim intervalima** kroz cijelu 2024. godinu.

---

## 2. Files

### 2.1. Electricity — Non-controllable Load

**Filename:** `noncontrollable_load_annual_profile_Household.csv`

**Columns:**

| Column                     | Unit | Description                                  |
|---------------------------|------|----------------------------------------------|
| `timestamp`               | –    | Date and time (`%d.%m.%Y %H:%M`)             |
| `Electricity demand (kWh)`| kWh  | Energy consumed in that 15-min interval      |

**Assumptions:**

- Broj članova kućanstva: **4 osobe**
- Tipično kućanstvo bez električnog grijanja
- Specifična godišnja potrošnja: **3 500 kWh/god**
- Tipični dnevni profil:
  - noćni minimum (0 – 6 h): ~0,05–0,1 kWh/15min  
  - jutarnji vrh (6 – 9 h): ~0,3–0,6 kWh/15min  
  - dnevna stabilizacija (10 – 17 h): ~0,1–0,2 kWh/15min  
  - večernji vrh (18 – 22 h): ~0,4–0,8 kWh/15min  
  - kasni pad (22 – 24 h): ~0,1–0,2 kWh/15min

**Result:**

- **Ukupna godišnja potrošnja električne energije:** **≈ 3 500 kWh (3,5 MWh)**  
  što odgovara realnim vrijednostima za četveročlano kućanstvo bez električnog grijanja.

---

### 2.2. Water — Hot Water Demand

**Filename:** `water_demand_annual_profile_Household.csv`

**Columns:**

| Column            | Unit | Description                                  |
|------------------|------|----------------------------------------------|
| `timestamp`      | –    | Date and time (`%d.%m.%Y %H:%M`)             |
| `Hot water demand (m3)` | m³ | Volume of *hot water* consumed in that 15-min interval |

**Assumptions and Benchmark:**

- Broj osoba: **4**
- Prosječna dnevna potrošnja vode: **150 L/osobu/dan**  
  → ukupno 600 L/dan po kućanstvu
- Udio tople vode: **30–40 %**  
  → oko **200–240 L/dan** tople vode = **0,2–0,24 m³/dan**
- Bojler: **200 L** (ograničenje po intervalu ≤ 200 L)
- Ciljana godišnja potrošnja: **≈ 60 m³/god (60 000 L)**

**Daily pattern:**

- vrlo niska potrošnja noću (0 – 5 h)
- jutarnji vrh (6 – 9 h): tuširanje i higijena  
- srednji pad (10 – 17 h): minimalna aktivnost  
- večernji vrh (18 – 22 h): pranje suđa, tuševi, kuhanje  
- vikendom: blago povećanje potrošnje tijekom dana

**Result:**

- **Ukupna godišnja potrošnja tople vode:** **≈ 60 m³ (60 000 L)**  
- maksimalna potrošnja u intervalu ≤ **200 L/15min**

---

## 3. Intended Use

Ovi profili su namijenjeni za:

- simulacije potrošnje energije i tople vode u stambenim sektorima,  
- testiranje energetskih upravljačkih sustava (EMS) u Multi-Energy kontekstu,  
- modeliranje fleksibilnih i nefleksibilnih potrošača u MILP optimizacijama.

Profili su **sintetički**, ali su kalibrirani prema realnim statistikama za kućanstva u EU.

---

## 4. References (Literatura)

1. **P. F. De Oliveira et al. (2023)** — *Characterizing Hot-Water Consumption at Household and Fixture-Level*,  
   *Water* 2023, 17(13), 1906.  
   [https://www.mdpi.com/2073-4441/17/13/1906](https://www.mdpi.com/2073-4441/17/13/1906)  
   (navodi prosječnu potrošnju ~106,7 L/osobu/dan, od čega ~33,9 L tople vode)

2. **G. S. Vieira et al. (2017)** — *Review of Domestic Hot Water Consumption Profiles for Different Building Types*,  
   *Renewable and Sustainable Energy Reviews*, Vol. 74, pp. 1119–1139.  
   (analiza obrazaca potrošnje tople vode za stambene objekte)

3. **Eurostat (2024)** — *Energy Consumption in Households*  
   [https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Energy_consumption_in_households](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Energy_consumption_in_households)  
   (navodi prosječnu godišnju električnu potrošnju kućanstava u EU između 3–5 MWh)

4. **U.S. Energy Information Administration (RECS 2020)** — *Residential Energy Consumption Survey*  
   [https://www.eia.gov/consumption/residential](https://www.eia.gov/consumption/residential)  
   (benchmark podaci o strukturi dnevnih profila i udjelima tople vode)

---

## 5. Notes

Ako kućanstvo ima električno grijanje vode, električnu energiju za zagrijavanje možeš izračunati iz profila tople vode prema formuli:

\[
Q = \rho \, c_p \, V \, \Delta T
\]

Za ΔT = 35 K i gustoću vode = 1 kg/L:

\[
Q_{1L} = 0.0406\text{ kWh/L}
\]
\[
Q_{day} = V_{day} \cdot 0.0406
\]

Primjer: 200 L tople vode → 8,1 kWh toplinske energije dnevno (~3 MWh/god).

---

**Autor:** Generirano pomoću GPT-5 (OpenAI, 2025)  
**Datum:** 05.11.2025.
