# Commercial (Shopping Mall) — Annual Profiles

## 1. Overview

Ovaj skup podataka opisuje godišnje profile:
- neupravljive potrošnje **električne energije**
- ukupne **potrošnje vode**

za reprezentativni **šoping centar (Commercial hub)**.

Svi profili su uzorkovani u **15-minutnim intervalima** kroz cijelu 2024. godinu.

---

## 2. Files

### 2.1. Electricity — Non-controllable Load

**Filename:** `noncontrollable_load_annual_profile_Commercial.csv`

**Columns:**

| Column                     | Unit | Description                                  |
|---------------------------|------|----------------------------------------------|
| `timestamp`               | –    | Date and time (`%d.%m.%Y %H:%M`)             |
| `Electricity demand (kWh)`| kWh  | Energy consumed in that 15-min interval      |

**Assumptions:**

- Floor area: **25 000 m²**
- Specific annual electricity use: **350 kWh/m²/year**
- Target annual consumption: **8,75 GWh**
- Daily profile:
  - visoka potrošnja od **08:00 – 22:00** (radno vrijeme centra)
  - niža potrošnja noću (osiguranje, rasvjeta, ventilacija)
  - vikendom povećanje (~15 %) tijekom vršnih sati

**Result:**

- **Ukupna godišnja potrošnja:** **8 750 000 kWh ≈ 8,75 GWh**

---

### 2.2. Water — Total Demand

**Filename:** `water_demand_annual_profile_Commercial.csv`

**Columns:**

| Column            | Unit | Description                                  |
|------------------|------|----------------------------------------------|
| `timestamp`      | –    | Date and time (`%d.%m.%Y %H:%M`)             |
| `Water demand (m3)` | m³ | Water volume consumed in that 15-min interval |

**Assumptions and Benchmark:**

- Water use intensity (WUI): **5 L/m²/day**  
  - 3 L/m²/day osnovna potrošnja (sanitarije, čišćenje)  
  - +2 L/m²/day dodatno za restorane, food court i hlađenje  
- Floor area: **25 000 m²**
- Dnevna voda:
  \[
  5 × 25 000 = 125 000 \text{ L/day} = 125 \text{ m³/day}
  \]
- Godišnja voda:
  \[
  125 × 365 = 45 625 \text{ m³/year}
  \]

**Daily pattern:**

- vrlo niska potrošnja noću (0 – 6 h)
- rast od 6 – 9 h
- glavni vrh **09 – 21 h** (radno vrijeme)
- manji porast u kasnim satima (čišćenje)
- vikendom povećanje intenziteta

**Result:**

- **Ukupna godišnja potrošnja vode:** **45 625 m³**

---

## 3. Intended Use

Ovi profili su namijenjeni za:

- simulacije energetskih i vodnih potreba komercijalnih zgrada,
- testiranje upravljanja energijom/vodom na razini „Commercial hub-a“,
- integraciju u modele Multi-Energy System ili MILP optimizacije.

Profili su **sintetički**, ali kalibrirani prema stvarnim **water-use** i **electricity-use intensity** pokazateljima iz literature.

---

## 4. References (Literatura)

1. **Uisce Éireann (Irish Water)** — *Business Conservation Tips: Retail Sector*,  
   [https://www.water.ie/conservation/business/business-conservation-tips/retail](https://www.water.ie/conservation/business/business-conservation-tips/retail)  
   (prikazuje prosječne pokazatelje potrošnje vode za trgovačke objekte, ~3 L/m²/dan)

2. **Better Buildings Partnership (UK)** — *Real Estate Environmental Benchmarks Report 2020*,  
   [https://www.betterbuildingspartnership.co.uk/sites/default/files/media/attachment/2020%20Real%20Estate%20Environmental%20Benchmarks_2.pdf](https://www.betterbuildingspartnership.co.uk/sites/default/files/media/attachment/2020%20Real%20Estate%20Environmental%20Benchmarks_2.pdf)  
   (navodi raspon potrošnje električne energije 200–400 kWh/m²/god za shopping centre)

3. **U.S. Energy Information Administration (CBECS 2012)** — *Commercial Buildings Energy Consumption Survey*,  
   [https://www.eia.gov/consumption/commercial/reports/2012/water](https://www.eia.gov/consumption/commercial/reports/2012/water)  
   (benchmark potrošnje vode i energije za velike komercijalne zgrade)

4. **U.S. EPA (2024)** — *Benchmarking Water Use in Commercial Buildings (WaterSense)*,  
   [https://www.epa.gov/system/files/documents/2024-03/ws-commercial-bmp-watersenseatwork_section2.3_benchmarking.pdf](https://www.epa.gov/system/files/documents/2024-03/ws-commercial-bmp-watersenseatwork_section2.3_benchmarking.pdf)  
   (vodič za intenzitet potrošnje vode – Water Use Intensity, WUI)

---

## 5. Notes

Ako se želi simulirati manji ili energetski učinkovitiji šoping centar (npr. 2,4 GWh godišnje),  
profil se može jednostavno **skalirati** množenjem svih vrijednosti u stupcu `Electricity demand (kWh)`  
faktorom:

\[
f = \frac{2.414.792}{8.750.000} \approx 0.276
\]

što daje isti oblik profila, ali nižu ukupnu potrošnju.

---

**Autor:** Generirano pomoću GPT-5 (OpenAI, 2025)  
**Datum:** 05.11.2025.
