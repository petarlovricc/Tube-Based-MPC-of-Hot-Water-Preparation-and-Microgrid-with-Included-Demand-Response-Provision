# Industry (Medium Manufacturing Plant) — Annual Profiles

## 1. Overview

Ovaj skup podataka opisuje godišnje profile:
- neupravljive potrošnje **električne energije**
- ukupne **potrošnje vode**

za **srednje veliko industrijsko postrojenje** s kombiniranim procesima, HVAC sustavima i sanitarnim potrošačima.

Svi profili su uzorkovani u **15-minutnim intervalima** kroz cijelu 2024. godinu.

---

## 2. Files

### 2.1. Electricity — Non-controllable Load

**Filename:** `noncontrollable_load_annual_profile_Industry.csv`

**Columns:**

| Column                     | Unit | Description                                  |
|---------------------------|------|----------------------------------------------|
| `timestamp`               | –    | Date and time (`%d.%m.%Y %H:%M`)             |
| `Electricity demand (kWh)`| kWh  | Energy consumed in that 15-min interval      |

**Assumptions:**

- Vrsta objekta: **srednje veliko industrijsko postrojenje**
- Glavno radno vrijeme: **06:00 – 18:00**
- Vikendom: smanjen intenzitet rada (~60 %)
- Specifična godišnja potrošnja električne energije:
  - prosječno 250–400 kWh/m²/god (ovisno o industriji)
- Ciljana godišnja potrošnja: **4 000 000 kWh (4,0 GWh)**

**Daily pattern:**
- noćni minimum (0 – 6 h): bazna oprema, hlađenje, sigurnosni sustavi  
- radno vrijeme (6 – 18 h): glavni procesi, strojevi, rasvjeta, ventilacija  
- večernji pad (18 – 22 h): čišćenje, ventilacija, smanjenje pogona  
- vikendom: ~40 % manja potrošnja

**Result:**

- **Ukupna godišnja potrošnja:** **≈ 4 000 000 kWh (4 GWh)**

---

### 2.2. Water — Total Demand

**Filename:** `water_demand_annual_profile_Industry.csv`

**Columns:**

| Column            | Unit | Description                                  |
|------------------|------|----------------------------------------------|
| `timestamp`      | –    | Date and time (`%d.%m.%Y %H:%M`)             |
| `Water demand (m3)` | m³ | Water volume consumed in that 15-min interval |

**Assumptions and Benchmark:**

- Prosječna potrošnja: **100 m³/dan**
- Godišnja potrošnja: **≈ 36 500 m³/god**
- Uključuje:
  - procesnu vodu (rashladni sustavi, ispiranje, čišćenje),
  - sanitarnu i opću potrošnju,
  - tehnološke potrebe tijekom proizvodnje.
- Vikendom: niži intenzitet rada (~60 %)

**Daily pattern:**
- 0 – 6 h: minimalna potrošnja (bazni sustavi, hlađenje)  
- 6 – 18 h: glavni procesi i čišćenje (vrhunac)  
- 18 – 22 h: smanjenje, eventualno pranje i priprema  
- 22 – 24 h: održavanje i minimalni protok

**Result:**

- **Ukupna godišnja potrošnja vode:** **≈ 36 500 m³**

---

## 3. Intended Use

Ovi profili su namijenjeni za:

- simulacije energetskih potreba industrijskih sustava,  
- optimizaciju Multi-Energy System modela (električna energija + voda),  
- integraciju u MILP ili Pyomo optimizacijske modele,  
- analizu interakcija s proizvodnim procesima i fleksibilnim resursima.

Profili su **sintetički**, ali su **skalirani prema industrijskim benchmarkovima** i prilagođeni za realističan dnevni ritam rada.

---

## 4. References (Literatura)

1. **TERI (The Energy and Resources Institute, 2018)** — *Benchmarking Industrial Water Use Efficiency in India*  
   [https://teriin.org/sites/default/files/files/Benchmarking_Industrial_Water_Use_Efficiency_in_India.pdf](https://teriin.org/sites/default/files/files/Benchmarking_Industrial_Water_Use_Efficiency_in_India.pdf)  
   (benchmark specifične potrošnje vode po industrijskim sektorima)

2. **M. Scott et al. (2021)** — *Benchmarking and Identification of Best Practice Associated with Industrial Water Use in the UK*,  
   *Journal of Cleaner Production*, Vol. 320, 128837.  
   (usporedba učinkovitosti potrošnje vode i energetskih potreba u industriji)

3. **U.S. Department of Energy (2023)** — *Energy Use in Manufacturing Sector*  
   [https://www.energy.gov/eere/amo/manufacturing-energy-consumption-survey](https://www.energy.gov/eere/amo/manufacturing-energy-consumption-survey)  
   (benchmark godišnje potrošnje električne energije i radnih obrazaca)

4. **IEA Energy Statistics (2022)** — *Energy Efficiency Indicators by Sector*  
   [https://www.iea.org/data-and-statistics](https://www.iea.org/data-and-statistics)  
   (referentni rasponi potrošnje energije u industriji, 200–500 kWh/m²/god)

---

## 5. Notes

Ovi profili ne uključuju posebne industrijske tehnologije poput elektrolize, kemijske sinteze ili visokotemperaturnih procesa.  
Za takve slučajeve (npr. Power-to-X postrojenja) treba koristiti zaseban, procesno specifičan model potrošnje.

---

**Autor:** Generirano pomoću GPT-5 (OpenAI, 2025)  
**Datum:** 05.11.2025.
