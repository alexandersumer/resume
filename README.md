# Alexander Sumer

Sydney, NSW, Australia · [GitHub](https://github.com/alexandersumer) · [LinkedIn](https://www.linkedin.com/in/alexandersumer)

*AI platform engineer at Atlassian. Reliability and performance of chat and agent AI systems supporting all Atlassian's AI products and integrations.*

## Experience

### Atlassian · Sydney, Australia
**Senior Software Engineer, AI Platform** · *Nov 2019 – Present*

- Promoted to Senior within two years, now operating at Principal level. Highest change throughput, review volume, and lowest incident rate in the org while leading 9 engineers across three projects.
- **Autonomous Browser Agent:** Led 5 engineers (including 2 seniors) building a system where a vision-language model (Gemini) interprets browser screenshots and returns coordinate-based commands via Playwright/CDP. Designed warm pod pools for sub-second session start, HMAC-signed routing, and per-session container isolation. Topped internal evals; completed complex compliance workflows end-to-end.
- **Agent Sandbox:** Built a new execution platform supporting session hibernation with disk-backed state, 20 GB persistent volumes, and hardware-level isolation via KATA Containers (lightweight VMs). Replaced a legacy service that had no file system and scaled poorly (linear namespace scan). Agents can now generate files, produce charts, and resume across sessions.
- **Unified AI Platform Architecture:** Leading 5 engineers (including 1 principal) to raise reliability horizontally across all AI products, reducing average incident time to recovery from 10 hours to 1. Moved the platform from a synchronous monolith to a reactive, non-blocking architecture using Kotlin Coroutines. Unified HTTP clients across all integrations with standardised request caching. Added a two-tier cache that cut redundant network calls by 90%.
- Built a rollout service for Atlassian's third-largest monorepo, automating safe progressive deployments and improving release reliability for hundreds of engineers.
- **Jira Issue Service:** Built from inception a 99.999%-reliability, low-latency platform service powering multiple Atlassian products. Proposed and gained Principal-level buy-in for a persistence layer on the Mercury Cache library. Led the real-time Issue Event Stream with at-least-once delivery. Parallelized authorization checks for a 20× P90 latency improvement. Redesigned queries and caching to cut P99 latency from 10s to 200ms for the largest customers.

**Sympli** · Developer · *Oct 2018 – Jul 2019*

Built a server-side form generator (JSON → React) for electronic real estate transactions, a serverless healthcheck service (Lambda, SNS), and introduced unit testing standards across the team.

**WiseTech Global** · Associate Developer · *Aug 2017 – Sep 2018*

Built a coordinate-based distance/time matrix API with algorithm selection based on graph structure. Replaced SQL literals with table-valued parameters for a 4× query performance improvement.

## Education

### University of New South Wales · Sydney, Australia
**Bachelor of Computer Science** · *Jul 2016 – May 2020*

- Teaching assistant for COMP2521 Algorithms and Data Structures.
- Volunteer C++ developer on rUNSWift (UNSW SPL robotics team). Worked on ball detection using the Kalman Filter.
- Competitive programming: 2017 ANZAC Round 2, 2018 NZPC, weekly ACM ICPC training.

## Skills & Interests

**Technologies:** Kubernetes, AWS, Kafka, gRPC, Gemini, Playwright, Kotlin, Java, TypeScript, Python, Go
**Interests:** AI, volleyball, cooking, fitness, good conversations
