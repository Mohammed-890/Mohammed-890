<a href="https://mohammed-890.github.io/"><img src="assets/arcade/title.svg" width="100%" alt="Mohammed Banabilh, AI and machine learning engineer"></a>

<p align="center">
  <a href="https://mohammed-890.github.io/"><img src="https://img.shields.io/badge/Play_my_projects-live-ff3fa4?style=for-the-badge&logo=githubpages&logoColor=white" alt="Play my projects live"></a>
  <a href="https://www.linkedin.com/in/mohammed-banabilh-6340553b0/"><img src="https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
  <a href="mailto:banabilh19@gmail.com"><img src="https://img.shields.io/badge/Email-Say_hello-ffe14d?style=for-the-badge&logo=gmail&logoColor=black" alt="Email"></a>
</p>

Final-year **Computer Science with AI** student at Sheffield Hallam University (graduating 2027). I build machine learning systems end to end, from collecting the data to running the model in production with monitoring and automatic retraining, and I build AI tools that work in **Arabic and English**.

## Select a game

<sub>Every cartridge is a real project. Click one to play the demo or read the code.</sub>

<table>
<tr>
<td width="50%"><a href="https://mohammed-890.github.io/nahem-chatbot/"><img src="assets/arcade/nahem.svg" width="100%" alt="Nahem: Arabic ordering chatbot, play the demo"></a></td>
<td width="50%"><a href="https://mohammed-890.github.io/show-me/"><img src="assets/arcade/show-me.svg" width="100%" alt="Show Me: Arabic text to English, play the demo"></a></td>
</tr>
<tr>
<td width="50%"><a href="https://github.com/Mohammed-890/seat-scout"><img src="assets/arcade/seat-scout.svg" width="100%" alt="Seat Scout: AI agent that finds the best stadium seat"></a></td>
<td width="50%"><a href="https://github.com/Mohammed-890/football-butterfly-effect/blob/main/docs/demo.mp4"><img src="assets/arcade/football.svg" width="100%" alt="Football Butterfly Effect: watch the demo"></a></td>
</tr>
<tr>
<td width="50%"><a href="https://github.com/Mohammed-890/worldcup-data-chat"><img src="assets/arcade/worldcup.svg" width="100%" alt="World Cup Data Chat: plain English to SQL"></a></td>
<td width="50%"><a href="https://mohammed-890.github.io/ghost-bus/"><img src="assets/arcade/ghost-bus.svg" width="100%" alt="Ghost Bus Detector: live site"></a></td>
</tr>
</table>

<a href="https://mohammed-890.github.io/ghost-bus/"><img src="assets/ghostbus-live.svg" width="100%" alt="Ghost Bus Detector live high scores"></a>

<!-- game:start -->
## Bonus stage: did this bus turn up?

Every day this asks about a **real departure** from Sheffield, checked by [Ghost Bus Detector](https://github.com/Mohammed-890/ghost-bus) against live GPS.

> **Route 115** (First South Yorkshire), **13:46** on **Tuesday 10 November**
> from Rotherham Interchange/B1 to Laudsdale Road/Lady Oak Road

Did a bus actually run it?

<p align="left"><a href="https://github.com/Mohammed-890/Mohammed-890/issues/new?title=ghostbus%3Af80158%3Aran&body=Just%20press%20%2A%2ASubmit%20new%20issue%2A%2A.%20A%20bot%20replies%20with%20the%20real%20answer%20in%20about%20a%20minute%2C%20adds%20you%20to%20the%20scoreboard%20and%20closes%20this%20issue."><img src="https://img.shields.io/badge/It%20ran-1aa38c?style=for-the-badge" alt="It ran"></a> &nbsp; <a href="https://github.com/Mohammed-890/Mohammed-890/issues/new?title=ghostbus%3Af80158%3Aghost&body=Just%20press%20%2A%2ASubmit%20new%20issue%2A%2A.%20A%20bot%20replies%20with%20the%20real%20answer%20in%20about%20a%20minute%2C%20adds%20you%20to%20the%20scoreboard%20and%20closes%20this%20issue."><img src="https://img.shields.io/badge/It%20never%20came-7b5cff?style=for-the-badge" alt="It never came"></a></p>

<sub>0 guesses today · 0 guesses in total</sub>

<sub>Yesterday's bus (route 95 at 11:25): **it never came**. 0 of 0 guessed right.</sub>
<!-- game:end -->

<img src="assets/arcade/inventory.svg" width="100%" alt="Tools: Python, scikit-learn, pandas, MLflow, FastAPI, Docker, Kubernetes, Helm, Terraform, Argo CD, Prometheus, GitHub Actions, TypeScript, SQL, Java, Three.js">

<details>
<summary><b>Player manual: how Ghost Bus works</b></summary>
<br>


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
<summary><b>Secret levels: more projects</b></summary>
<br>

| Project | What it is |
|---|---|
| [ChurnOps](https://github.com/Mohammed-890/churn-mlops) | Customer churn model behind a tested FastAPI service, Docker and Terraform for AWS ECS. ROC-AUC 0.84 on 1,409 held-out customers. |
| [Sheffield Road Collision ML](https://github.com/Mohammed-890/sheffield-collision-ml) | End-to-end ML on UK road-collision data: classification, regression and clustering. University project, graded a First. |
| AttendFlow | University attendance system: three FastAPI services, PostgreSQL, Redis Streams and a React front end. Software Architecture coursework (private). |
| Onyx AI dashboard | Bilingual multi-client reporting over a live ERP system, built for a retail client (private). |

</details>

<details>
<summary><b>House rules: how I work</b></summary>
<br>


- **Every model gets a baseline.** If it can't beat a simple rule, it isn't ready.
- **Results are measured on data the model hasn't seen**, and each project says what it can't do.
- **If it isn't tested, it isn't done.** Evaluation sets, regression tests and end-to-end tests on every project.

</details>

<a href="https://www.linkedin.com/in/mohammed-banabilh-6340553b0/"><img src="assets/arcade/continue.svg" width="100%" alt="Continue? Open to ML engineering and MLOps internships, and graduate roles from July 2027"></a>

<sub>Pixel font: Press Start 2P (SIL Open Font License).</sub>
