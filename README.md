# Urban Traffic Spatiotemporal Feature Extraction and Visualization Based on Taxi GPS Data
## Project Overview
This project explores spatiotemporal travel patterns of taxis in Jinan, China, using large‑scale GPS trajectory records. We aim to discover spatial hotspots of taxi pick‑ups and temporal rhythm differences between weekdays and weekends, and deliver visual outputs for audiences without technical backgrounds.

## Research Question
What are the spatiotemporal structural patterns of Jinan taxi trips from September 12 to September 18, 2013? How can we communicate these mobility patterns through clear visualization? We further study demand gaps on workdays versus weekends, spatial clustering of boarding hotspots, and whether two hotspot measurement methods give consistent results after map‑matching.

## Dataset Source and Usage Permissions
The primary dataset contains around 243 million GPS records from about 7400 licensed Jinan taxis across seven consecutive days. Vehicle IDs are fully de‑identified. No personal information of drivers or passengers is included. The dataset is downloaded from an open teaching data service.

We also use hourly historical weather data from Open‑Meteo Historical Weather API under its non‑commercial license. All datasets are used for academic research only. We aggregate all outputs at grid, road‑segment and district levels; no individual vehicle full activity history will be exposed.

Datasets link: https://uofmacau-my.sharepoint.com/:u:/g/personal/mc65922_um_edu_mo/IQB2_Lhli2_zSYcF9Lti-cqfAdRahw52flxncBAzwV2yiaw?e=CgLRF1

## Methods and Tools Used
For data processing, we use PySpark and Python libraries including Pandas, NumPy, SciPy and scikit‑learn. Core processing steps include record deduplication, coordinate correction, speed filtering, and valid passenger‑trip extraction based on the occupancy bit from the TFLAG field.

We apply grid‑based density calculation to avoid DBSCAN clustering chaining issues in dense city centres, and detect pick‑up hotspots from high‑density grid cells. KD‑tree spatial indexing supports geometric map‑matching to snap boarding points onto real road segments.

For analysis, we build hourly taxi‑demand time‑series and separate supply‑side effects (such as taxi shift‑change) from real travel demand. We handle confounding factors when testing correlation between travel volume and weather conditions.

Visualization is built with Matplotlib, ECharts and Baidu Maps API. Outputs include static log‑scale density heatmaps, weekday‑weekend demand line charts, animated spatial heatmaps and an offline‑usable interactive web dashboard.

## Key Findings
First, taxi pick‑up locations show extremely uneven spatial distribution. Most boarding events concentrate within central urban districts of Jinan. Second, weekday and weekend travel timelines show clear differences. A sharp demand drop near 17:00 on weekdays is mainly caused by taxi driver shift change (supply‑side change), not reduced passenger travel willingness. Third, direct correlation between humidity and travel demand is misleading because both follow the daily 24‑hour cycle. After removing diurnal periodic effects, their correlation direction reverses.

## Project Limitation
The study week had almost no rainfall. We cannot test how rainfall influences taxi travel demand using this dataset. In addition, street‑name reverse geocoding uses modern map resources, which may not perfectly match the 2013 urban street layout.

## Instructions for Running the Analysis
1. Place the extracted dataset under the path `\Jntaxi\static\data\`
2. Put the `dc` folder into `\anaconda3\Lib\site-packages\` (adjust the Anaconda path according to your local computer environment)
3. Open the `Jntaxi` project in PyCharm. Enter `python manage.py runserver` in the console. Then open `http://127.0.0.1:8000/` in your web browser.
