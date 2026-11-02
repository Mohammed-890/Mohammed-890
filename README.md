<p align="center">
  <img src="assets/banner.svg" width="100%" alt="Mohammed Banabilh. Machine learning and MLOps engineer.">
</p>

<p align="center">
  <a href="https://www.linkedin.com/in/mohammed-banabilh-6340553b0/"><img src="https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
  <a href="mailto:banabilh19@gmail.com"><img src="https://img.shields.io/badge/Email-Say%20hello-b49cff?style=for-the-badge&logo=gmail&logoColor=white" alt="Email"></a>
  <a href="https://mohammed-890.github.io/"><img src="https://img.shields.io/badge/Try%20my%20projects-live%20demos-ff6b2c?style=for-the-badge&logo=githubpages&logoColor=white" alt="Interactive portfolio with live demos"></a>
</p>

Final-year **Computer Science with AI** student at Sheffield Hallam University, graduating in 2027. I build machine learning systems end to end: collecting the data, training and testing the model honestly, and running it in production with monitoring and automatic retraining. I speak **Arabic and English** and build AI tools for both.

**Open to** ML engineering and MLOps internships now, and graduate roles from July 2027.

> **Try them live:** [mohammed-890.github.io](https://mohammed-890.github.io) has an interactive map of everything here, and you can use the Nahem chatbot and Show Me right on the page.

## Featured projects

<sub>Click a card to try it or read the code.</sub>

<table>
<tr>
<td width="50%" valign="top">
<a href="https://mohammed-890.github.io/nahem-chatbot/"><img src="assets/cards/nahem.png" alt="Nahem Assistant"></a>
<br><b><a href="https://mohammed-890.github.io/nahem-chatbot/">Live demo with guided tour</a></b> · <a href="https://github.com/Mohammed-890/nahem-chatbot">Code</a>
<br><sub>JavaScript · Arabic NLP · Google Apps Script · Gemini</sub>
</td>
<td width="50%" valign="top">
<a href="https://mohammed-890.github.io/show-me/"><img src="assets/cards/show-me.png" alt="Show Me"></a>
<br><b><a href="https://mohammed-890.github.io/show-me/">Live demo</a></b> · <a href="https://github.com/Mohammed-890/show-me">Code</a>
<br><sub>JavaScript · OCR (Tesseract) · runs fully in the browser</sub>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<a href="https://github.com/Mohammed-890/seat-scout"><img src="assets/cards/seat-scout.png" alt="Seat Scout"></a>
<br><b><a href="https://github.com/Mohammed-890/seat-scout">Code and screenshots</a></b>
<br><sub>TypeScript · Node.js · Claude API tool use · Three.js · Playwright</sub>
</td>
<td width="50%" valign="top">
<a href="https://github.com/Mohammed-890/football-butterfly-effect"><img src="assets/cards/football.png" alt="Football Butterfly Effect"></a>
<br><b><a href="https://github.com/Mohammed-890/football-butterfly-effect/blob/main/docs/demo.mp4">51-second demo video</a></b> · <a href="https://github.com/Mohammed-890/football-butterfly-effect">Code</a>
<br><sub>Python · NumPy · Elo + Poisson model · Monte Carlo · FastAPI</sub>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<a href="https://github.com/Mohammed-890/worldcup-data-chat"><img src="assets/cards/worldcup.png" alt="World Cup Data Chat"></a>
<br><b><a href="https://github.com/Mohammed-890/worldcup-data-chat">Code</a></b>
<br><sub>Python · SQLite · LLM text-to-SQL · Streamlit</sub>
</td>
<td width="50%" valign="top">
<a href="https://github.com/Mohammed-890/ghost-bus"><img src="assets/cards/ghost-bus.png" alt="Ghost Bus Detector"></a>
<br><b><a href="https://mohammed-890.github.io/ghost-bus/">Live site</a></b> · <a href="https://github.com/Mohammed-890/ghost-bus">Code</a>
<br><sub>Python · scikit-learn · MLflow · FastAPI · Kubernetes · Terraform · Argo CD</sub>
</td>
</tr>
</table>

<details>
<summary><b>How Ghost Bus works</b>, with live numbers (click to open)</summary>
<br>

<!-- ghostbus:start -->
| Ghost Bus, live from Sheffield | |
|---|---|
| Trips judged | **666** |
| Ghost buses found | **1 (0.1%)** |
| Last 7 days | **1 of 666 trips never came** |
| Days collected | **1 (since 1 Nov 2026)** |

<sub>Updated automatically every day from the project's live data · last update 2 Nov 2026</sub>
<!-- ghostbus:end -->

Every bus in England reports its GPS position to the government's Bus Open Data Service. Ghost Bus compares that with the timetable, trip by trip, to find the buses that never came, then predicts which departures are likely to be missed. A trip only counts as a ghost when the live feed and the operator were reporting reliably.

```mermaid
flowchart LR
  F[Live bus GPS<br/>every minute] --> M[Match each<br/>timetabled trip]
  T[Timetable] --> M
  M --> D[Daily results]
  D --> TR[Train challenger]
  TR --> G{Beats the live model<br/>on the same unseen days?}
  G -- yes --> R[MLflow champion]
  G -- no --> X[Rejected, with reason]
  R --> API[FastAPI on Kubernetes]
  D --> MON[Drift and live accuracy]
  MON -- drift or worse accuracy --> TR
```

- **Training and serving share one feature pipeline**, so they can't drift apart.
- **A new model only goes live if it beats the current one** on the same days neither has seen.
- **Retrains itself** on data drift (PSI) or when live accuracy drops.
- **Every push is tested on a real Kubernetes cluster**, including killing a pod while 300 requests come in. None failed.

</details>

<details>
<summary><b>More projects</b></summary>
<br>

| Project | What it is |
|---|---|
| [ChurnOps](https://github.com/Mohammed-890/churn-mlops) | Customer churn model behind a tested FastAPI service, Docker and Terraform for AWS ECS. ROC-AUC 0.84 on 1,409 held-out customers. |
| [Sheffield Road Collision ML](https://github.com/Mohammed-890/sheffield-collision-ml) | End-to-end ML on UK road-collision data: classification, regression and clustering. University project, graded a First. |
| AttendFlow | University attendance system: three FastAPI services, PostgreSQL, Redis Streams and a React front end. Software Architecture coursework (private). |
| Onyx AI dashboard | Bilingual multi-client reporting over a live ERP system, built for a retail client (private). |

</details>

## Tools I use

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white" alt="scikit-learn">
  <img src="https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white" alt="pandas">
  <img src="https://img.shields.io/badge/MLflow-0194E2?style=flat-square&logo=mlflow&logoColor=white" alt="MLflow">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/Kubernetes-326CE5?style=flat-square&logo=kubernetes&logoColor=white" alt="Kubernetes">
  <img src="https://img.shields.io/badge/Helm-0F1689?style=flat-square&logo=helm&logoColor=white" alt="Helm">
  <img src="https://img.shields.io/badge/Terraform-844FBA?style=flat-square&logo=terraform&logoColor=white" alt="Terraform">
  <img src="https://img.shields.io/badge/Argo%20CD-EF7B4D?style=flat-square&logo=argo&logoColor=white" alt="Argo CD">
  <img src="https://img.shields.io/badge/Prometheus-E6522C?style=flat-square&logo=prometheus&logoColor=white" alt="Prometheus">
  <img src="https://img.shields.io/badge/GitHub%20Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white" alt="GitHub Actions">
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white" alt="TypeScript">
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black" alt="JavaScript">
  <img src="https://img.shields.io/badge/SQL-4479A1?style=flat-square&logo=postgresql&logoColor=white" alt="SQL">
  <img src="https://img.shields.io/badge/Java-ED8B00?style=flat-square&logo=openjdk&logoColor=white" alt="Java">
</p>

## How I work

- **Every model gets a baseline.** If it can't beat a simple rule, it isn't ready.
- **Results are measured on data the model hasn't seen**, and each project says what it can't do.
- **If it isn't tested, it isn't done.** Evaluation sets, regression tests and end-to-end tests on every project.
