# Biometric Substitution: Analyzing the LFR rollout in London (2023-2025)

This project investigates a potential shift in UK policing tactics: the transition from physical **Stop and Search** to **Live Facial Recognition (LFR)**. Recent statements about the drop in stop and search is brought into question This study hypothesizes that the "volume of search" has not actually decreased, but has instead become "frictionless" and "invisible" through the rapid scaling of biometric surveillance.

### Key Research Questions:

1. **The Substitution Effect:** Does the decline in physical stops correlate geographically with the rollout of LFR vans and permanent cameras?
2. **Environmental Justice:** Are these high-tech "digital searches" disproportionately concentrated in areas of high deprivation (IMD Deciles 1-3)?
3. **Policy Alignment:** Does the "frictionless" nature of LFR bypass the traditional legal protections (PACE 1984) associated with physical searches?

---

## 🏛 Policy & Ethics Context

This analysis is situated within the following UK policy frameworks:

* **The Data (Use and Access) Act 2025:** Evaluating how new AI provisions impact biometric privacy.
* **Home Office Facial Recognition Consultation (2025/26):** Contributing data-driven insights into the "proportionality" of LFR deployments.
* **The "ABC" of Geospatial Ethics:** Ensuring **A**ccountability, identifying **B**ias, and providing **C**larity in location data.

---

## 📊 Data Sources

To ensure reproducibility while respecting file size limits and licensing, raw data is not hosted in this repository. Use the following sources:

* **Policing Data:** [Police.uk Data Portal](https://data.police.uk/) (Metropolitan Police Service).
* **Surveillance Logs:** [Met Police LFR Deployment Records](https://www.met.police.uk/advice/advice-and-information/facial-recognition/live-facial-recognition/).
* **Socio-Economic Data:** [English Indices of Deprivation 2019/2024](https://www.gov.uk/government/statistics/english-indices-of-deprivation-2019).
* **Geospatial Boundaries:** [ONS Open Geography Portal](https://geoportal.statistics.gov.uk/) (LSOA Boundaries).

---

## 🛠 Tech Stack

* **Language:** Python 3.11+ (Jupyter Notebooks)
* **GIS:** QGIS 3.x & GeoPandas
* **Libraries:** `pandas`, `geopandas`, `matplotlib`, `contextily`, `tabula-py`
* **Version Control:** GitHub Desktop

---

## 📜 License

This project is licensed under the **MIT License**.
*Statistical data contains public sector information licensed under the [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).*
