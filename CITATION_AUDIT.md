# Citation audit

Retrieval date: 2026-11-16.
arXiv rows were read from `export.arxiv.org` (Atom API), one record per id.
DOI rows were read from `api.crossref.org`.
PDFs were not opened. A VERIFIED id means the identifier resolved and the title below is the record's title.
It does not mean every number in the literature reviews was checked.
`make check` does not repeat this retrieval. It only checks that every arXiv id and DOI in the tree appears in the table, and that a MISMATCH or UNVERIFIED row is marked beside that id in a source file.

Statistics in the literature reviews that are not quoted in the note column were not re-checked. Treat them as unverified even when the id is VERIFIED. That includes the NoLiMa percentages, the LongBench v2 percentages, and the SLIM "50%+" sentence.

Pages that are not an arXiv id or a DOI (vendor blogs, a CSDN post used as an AAMAS date, Project Vend, Chroma's context-rot page, program-bench PDFs, and similar) were not fetched. Claims that rest only on those URLs are unverified.

| id | status | retrieved title or error | note |
|---|---|---|---|
| 2201.11903 | VERIFIED | Chain-of-Thought Prompting Elicits Reasoning in Large Language Models | 2022-01-28; Jason Wei; Xuezhi Wang; Dale Schuurmans; Maarten Bosma (n=9). Title is Chain-of-Thought Prompting Elicits Reasoning in Large Language Models (Wei et al.). |
| 2303.11366 | VERIFIED | Reflexion: Language Agents with Verbal Reinforcement Learning | 2023-03-20; Noah Shinn; Federico Cassano; Edward Berman; Ashwin Gopinath (n=6). Title starts Reflexion. |
| 2304.03442 | VERIFIED | Generative Agents: Interactive Simulacra of Human Behavior | 2023-04-07; Joon Sung Park; Joseph C. O'Brien; Carrie J. Cai; Meredith Ringel Morris (n=6). Title starts Generative Agents. |
| 2306.05685 | VERIFIED | Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena | 2023-06-09; Lianmin Zheng; Wei-Lin Chiang; Ying Sheng; Siyuan Zhuang (n=13). Title is Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena. |
| 2307.03172 | VERIFIED | Lost in the Middle: How Language Models Use Long Contexts | 2023-07-06; Nelson F. Liu; Kevin Lin; John Hewitt; Ashwin Paranjape (n=7). Title starts Lost in the Middle. |
| 2309.02427 | VERIFIED | Cognitive Architectures for Language Agents | 2023-09-05; Theodore R. Sumers; Shunyu Yao; Karthik Narasimhan; Thomas L. Griffiths (n=4). Title is Cognitive Architectures for Language Agents. |
| 2310.04406 | VERIFIED | Language Agent Tree Search Unifies Reasoning Acting and Planning in Language Models | 2023-10-06; Andy Zhou; Kai Yan; Michal Shlapentokh-Rothman; Haohan Wang (n=5). Title is Language Agent Tree Search (LATS). |
| 2310.11511 | VERIFIED | Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection | 2023-10-17; Akari Asai; Zeqiu Wu; Yizhong Wang; Avirup Sil (n=5). Title starts Self-RAG. |
| 2401.10020 | VERIFIED | Self-Rewarding Language Models | 2024-01-18; Weizhe Yuan; Richard Yuanzhe Pang; Kyunghyun Cho; Xian Li (n=7). Title is Self-Rewarding Language Models. |
| 2401.15884 | VERIFIED | Corrective Retrieval Augmented Generation | 2024-01-29; Shi-Qi Yan; Jia-Chen Gu; Yun Zhu; Zhen-Hua Ling (n=4). Title is Corrective Retrieval Augmented Generation (CRAG). |
| 2402.17753 | VERIFIED | Evaluating Very Long-Term Conversational Memory of LLM Agents | 2024-02-27; Adyasha Maharana; Dong-Ho Lee; Sergey Tulyakov; Mohit Bansal (n=6). Abstract names the LoCoMo dataset. |
| 2404.18796 | VERIFIED | Replacing Judges with Juries: Evaluating LLM Generations with a Panel of Diverse Models | 2024-04-29; Pat Verga; Sebastian Hofstatter; Sophia Althammer; Yixuan Su (n=9). Title is Replacing Judges with Juries (PoLL). |
| 2405.01535 | VERIFIED | Prometheus 2: An Open Source Language Model Specialized in Evaluating Other Language Models | 2024-05-02; Seungone Kim; Juyoung Suk; Shayne Longpre; Bill Yuchen Lin (n=10). Title starts Prometheus 2. |
| 2410.02694 | VERIFIED | HELMET: How to Evaluate Long-Context Language Models Effectively and Thoroughly | 2024-10-03; Howard Yen; Tianyu Gao; Minmin Hou; Ke Ding (n=8). arXiv comment: ICLR 2025. Project page princeton-nlp.github.io/HELMET. Older text said Princeton 2024 ICLR; the comment says ICLR 2025. Abstract: NIAH does not reliably predict downstream performance; the full-context gap widens with length. |
| 2410.10813 | VERIFIED | LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory | 2024-10-14; Di Wu; Hongwei Wang; Wenhao Yu; Yuwei Zhang (n=6). arXiv comment: ICLR 2025. Abstract includes a 30% accuracy drop on memorizing information across sustained interactions. First author Di Wu. LongMemEval-V2 and EverMemBench are not this paper. |
| 2411.15594 | VERIFIED | A Survey on LLM-as-a-Judge | 2024-11-23; Jiawei Gu; Xuhui Jiang; Zhichao Shi; Hexiang Tan (n=16). Title is A Survey on LLM-as-a-Judge. |
| 2412.05579 | VERIFIED | LLMs-as-Judges: A Comprehensive Survey on LLM-based Evaluation Methods | 2024-12-07; Haitao Li; Qian Dong; Junjie Chen; Huixue Su (n=8). Title starts LLMs-as-Judges: A Comprehensive Survey. |
| 2412.15204 | VERIFIED | LongBench v2: Towards Deeper Understanding and Reasoning on Realistic Long-context Multitasks | 2024-12-19; Yushi Bai; Shangqing Tu; Jiajie Zhang; Hao Peng (n=12). Title matches LongBench v2. The 50.1% and 57.7% figures were not re-read from the PDF. |
| 2501.13956 | VERIFIED | Zep: A Temporal Knowledge Graph Architecture for Agent Memory | 2025-01-20; Preston Rasmussen; Pavlo Paliychuk; Travis Beauvais; Jack Ryan (n=5). Title is Zep. The abstract describes Graphiti as Zep's knowledge-graph engine, not as a separate paper. |
| 2502.05167 | VERIFIED | NoLiMa: Long-Context Evaluation Beyond Literal Matching | 2025-02-07; Ali Modarressi; Hanieh Deilamsalehy; Franck Dernoncourt; Trung Bui (n=7). Title is NoLiMa: Long-Context Evaluation Beyond Literal Matching. The 11/13 and 99.3% to 69.7% figures are not in this audit; the PDF was not read. |
| 2502.12110 | VERIFIED | A-MEM: Agentic Memory for LLM Agents | 2025-02-17; Wujiang Xu; Zujie Liang; Kai Mei; Hang Gao (n=6). Title starts A-MEM: Agentic Memory for LLM Agents. |
| 2502.14802 | VERIFIED | From RAG to Memory: Non-Parametric Continual Learning for Large Language Models | 2025-02-20; Bernal Jiménez Gutiérrez; Yiheng Shu; Weijian Qi; Sizhe Zhou (n=5). Abstract names HippoRAG 2. Title is From RAG to Memory: Non-Parametric Continual Learning for Large Language Models. |
| 2502.15840 | VERIFIED | Vending-Bench: A Benchmark for Long-Term Coherence of Autonomous Agents | 2025-02-20; Axel Backlund; Lukas Petersson (n=2). Abstract supports high run variance, meltdown loops, and no clear correlation between failures and a full context window. Author list starts Axel Backlund; Lukas Petersson. The phrase Andon Labs is not in this record. |
| 2503.14499 | VERIFIED | Measuring AI Ability to Complete Long Software Tasks | 2025-03-18; Thomas Kwa; Ben West; Joel Becker; Amy Deng (n=26). Title is Measuring AI Ability to Complete Long Software Tasks (Kwa et al.). Abstract: Claude 3.7 Sonnet 50% time horizon around 50 minutes, on a mix of RE-Bench, HCAST, and shorter tasks. This id is not the RE-Bench paper. Older rows in this repo called it METR RE-Bench; that label was wrong. |
| 2503.16416 | VERIFIED | Survey on Evaluation of LLM-based Agents | 2025-03-20; Asaf Yehudai; Lilach Eden; Alan Li; Guy Uziel (n=8). Title is Survey on Evaluation of LLM-based Agents. |
| 2504.19413 | VERIFIED | Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory | 2025-04-28; Prateek Chhikara; Dev Khant; Saket Aryan; Taranjeet Singh (n=5). Title starts Mem0. |
| 2505.00675 | VERIFIED | Rethinking Memory in LLM based Agents: Representations, Operations, and Emerging Topics | 2025-05-01; Yiming Du; Wenyu Huang; Danna Zheng; Zhaowei Wang (n=8). Title starts Rethinking Memory in LLM based Agents. |
| 2510.18939 | VERIFIED | Lost in the Maze: Overcoming Context Limitations in Long-Horizon Agentic Search | 2025-10-21; Howard Yen; Yoonsang Lee; Ashwin Paranjape; Mengzhou Xia (n=8). Title is Lost in the Maze; the abstract names SLIM (Simple Lightweight Information Management). The abstract does not say that 50%+ of failures are context management. An older link pointed at a Samaya blog URL rather than the arXiv abstract. |
| 2604.11978 | VERIFIED | The Long-Horizon Task Mirage? Diagnosing Where and Why Agentic Systems Break | 2026-04-13; Xinyu Jessica Wang; Haoyue Bai; Yiyou Sun; Haorui Wang (n=10). Title and abstract name HORIZON and a trajectory-grounded LLM-as-a-Judge failure-attribution pipeline (human κ=0.61, human-judge κ=0.84). The abstract does not list planning / memory / historical-error as the category set. That three-way schema is this protocol's, and attributing it to HORIZON is not supported by the retrieved abstract. |
| 2606.30616 | VERIFIED | Scaling the Horizon, Not the Parameters: Reaching Trillion-Parameter Performance with a 35B Agent | 2026-06-29; Lei Bai; Zongsheng Cao; Yang Chen; Zhiyao Cui (n=53). Abstract introduces Agents-A1, a 35B mixture-of-experts model, and compares it with named 1T-parameter models. Qwen as the base model and Shanghai AI Lab as the affiliation are not in the abstract. See the MISMATCH row for the Llama 4 Herd label that used this same id. |
| 2606.30616 | MISMATCH | Scaling the Horizon, Not the Parameters: Reaching Trillion-Parameter Performance with a 35B Agent | LITERATURE_REVIEW_v3.md item 6 titles this id The Llama 4 Herd. The record is the Agents-A1 paper. |
| 10.1016/j.jml.2012.11.001 | VERIFIED | Random effects structure for confirmatory hypothesis testing: Keep it maximal | Crossref: Barr, Levy, Scheepers, Tily; Journal of Memory and Language, 2013. The same bullet also names Matuschek 2017, which is not this DOI. |
| 10.1038/s41562-024-01909-1 | UNVERIFIED | Crossref HTTP 404 on 2026-11-16 | Cited as Lakens 2024, Nature Human Behaviour, Deviations from the registered analysis plan. No replacement DOI was inserted. |
| 10.1136/bmj.m3210 | VERIFIED | Guidelines for clinical trial protocols for interventions involving artificial intelligence: the SPIRIT-AI Extension | Crossref: Rivera, Liu, Chan, Denniston, Calvert; BMJ, 2020. This DOI is not CONSORT-AI. |
| 10.1136/bmj.n71 | VERIFIED | The PRISMA 2020 statement: an updated guideline for reporting systematic reviews | Crossref: Page, McKenzie, Bossuyt, Boutron, Hoffmann, Mulrow, Shamseer, Tetzlaff; BMJ, 2021. |

## Claims that the identifier does not carry

- HORIZON's three category names (planning / memory / historical-error accumulation) are not in the retrieved abstract. The protocol still defines those three categories itself.
- Agents-A1's base model and lab affiliation, as stated in LITERATURE_REVIEW_v3.md, are not in the retrieved abstract.
- Matuschek et al. 2017 is named next to the Barr DOI and has no DOI of its own in this repo.
- CONSORT-AI is named in older sentences next to the SPIRIT-AI DOI. It is a different paper and is not identified here.
- LongMemEval-V2 and EverMemBench are named in the same bullet as LongMemEval (arXiv:2410.10813). They are not that paper.

