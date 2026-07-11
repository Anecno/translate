# translate-v2 — Codex Local Notes

This file is public-maintained and should not be overwritten by upstream syncs without review.

## 2026-05-27 Runtime Guardrail: Three-Layer Scoring Is Mandatory

- The §3.2 fourteen-dimension scoring schema is not a flat checklist. Every
  formal relay prompt, baton review, round archive, checkpoint report, and
  final `Translation-report.md` must preserve the nested three-layer structure:
  Layer A / `scores.language`, Layer B / `scores.literary`, and Layer C /
  `scores.cultural`, followed by `aggregate`.
- A flat `scores_14d` table is invalid for formal translate-v2 scoring even if
  it contains fourteen rows. It may appear only as quoted accident evidence
  from a prior baton, with an explicit note that the next baton must re-score
  under the three-layer schema. Do not ask downstream members to continue,
  inherit, or "lightly fix" a flat score table.
- Field names in newly prepared prompts should prefer `scores` or
  `scores_three_layer`, not `scores_14d`, because the latter has repeatedly
  induced flat outputs. If an external member returns `scores_14d`, Codex must
  treat the score section as schema-noncompliant and request/perform a
  three-layer re-score before using it as N-1/N-2 evidence.
- Short texts do not waive this requirement. `imagery_rhetoric`,
  `prosody_compensation`, `allusion_intertext`, and similar dimensions may be
  marked `N/A with reason`, but they must remain inside their proper layer.
- Before sending a Web/manual relay prompt or claiming a report/checkpoint is
  formal, run or satisfy `scripts/translate_v2_contract_gate.py` with an action/verification line
  that explicitly names `scores.language`, `scores.literary`, and
  `scores.cultural`. A gate payload that only says "14 维评分" is insufficient.
- In every baton prompt, §3.1 translation principles must be at the top as the
  generation compass and §3.2 three-layer scoring must be at the bottom as the
  post-hoc yardstick. Do not merge, reorder, or let either section perform the
  other's function.

## 2026-05-27 Runtime Guardrail: Artifact Contracts Are Mandatory

- Formal relay execution is not complete after a baton prompt or a single gate
  fix. Codex conductor duties include Web/raw capture, combined round archive,
  checkpoint/resume state, even-round divergence/non-divergence analysis, and
  final `Translation-report.md` generation only after the final-output gate.
- `scripts/translate_v2_contract_gate.py` must be used as an artifact contract gate, not only as
  a prompt checklist. A formal relay prompt/dispatch must name the downstream
  obligations: raw capture, one combined round archive, user checkpoint,
  R2/R4/R6 divergence-analysis gate, and final-output/report gate.
- A round archive is invalid unless it can stand alone as a handoff input:
  `<reply-drop>` path, five-baton trajectory, raw capture
  index, convergence index, checkpoint state, resume state, next-step inputs,
  Chinese main narrative, and syntax/morphology analysis when a candidate is
  presented.
- R2/R4/R6 divergence/non-divergence analysis is mandatory on even rounds, but
  it does not require a separate report file. Prefer embedding it as a
  dedicated section inside that even round's combined round archive unless the
  user asks for a standalone report or the run needs one for readability. If
  there is no real divergence or a candidate converges early, write a
  non-divergence / early-convergence reason analysis instead of omitting the
  function.
- A final `Translation-report.md` is invalid unless it preserves the complete
  sample-level skeleton: metadata, source/context anchors, final translation,
  relay trajectory, baseline comparison, three-layer scoring, detailed
  syntax/morphology, direct-vs-conversion audit, highlights/prosody, research
  TODO, compliance self-check, artifact list, and Chinese main narrative.
- 小D/本地 prep-helper 生成的 `译前上下文包` 也是正式输入门禁对象；每个接力成员的
  raw capture / 用户粘贴棒次输出也是正式 N-1/N-2 证据对象。二者都必须中文主叙述：
  分析、审查、评分、理由、收敛探针、raw wrapper 标题和说明必须中文；候选译文保留目标语；
  schema keys、状态常量、模型名、路径、必要英文参考样本可保留。缺这一层时不得把 prep
  包转交用户审阅，不得把单棒 raw 用作下一棒输入、round archive、checkpoint 或最终报告依据。
- After writing any formal Markdown artifact, run
  `<tools-root>/scripts/translate_v2_artifact_lint.py --type <type>
  <path>` before using it as evidence, N-1/N-2, checkpoint state, divergence
  analysis, or final report. Valid `<type>` values are `prompt-package`,
  `prep-package`, `baton-raw`, `round-archive`, `checkpoint`,
  `divergence-report`, and `final-report`.
  Run `--type prep-package` on 小D/本地译前上下文包；run `--type baton-raw`
  immediately after each member raw capture. For Antique Game tasks, also run
  `the Antique Game Within Game companion skill/scripts/lint_chinese_main_artifact.py`
  on prep/raw Markdown when it will feed the relay. If either lint blocks,
  repair the wrapper or re-request a Chinese-main baton before using it.
  For even-round combined archives that embed R2/R4/R6 divergence or
  non-divergence analysis, run the archive lint with `--even-round`; use
  `--type divergence-report` only for an optional standalone divergence file.
- The artifact lint is deliberately stricter than "file exists": it checks the
  actual Markdown content for flat `scores_14d`, missing three-layer scores,
  missing artifact-specific sections, `N/A` without reason, missing
  syntax/morphology anchors, missing non-divergence/early-convergence reasoning
  in even-round reports, and missing final-report skeleton items.

### Required Contents By Artifact Type

- Treat this subsection as the executable report contract. The matching lint
  type names are `prompt-package`, `prep-package`, `baton-raw`,
  `round-archive`, `checkpoint`, `divergence-report`, and `final-report`; use exactly these values with
  `<tools-root>/scripts/translate_v2_artifact_lint.py --type`.
- Formal relay prompt / dispatch package must include: current Codex-fork baton
  order, N-1/N-2 context rule, §3.1 principles at the top, three-layer
  `scores.language` / `scores.literary` / `scores.cultural` + `aggregate`,
  raw-capture requirement, combined round-archive requirement, user checkpoint
  stop, R2/R4/R6 divergence-analysis gate, and final-output/report gate.
- 译前上下文包必须包括：prep package 身份、源文边界、目标语、用户约束、上下文锚点、
  章节报告扫描状态、用户审阅状态，并保持中文主叙述。
- 单棒 raw capture 必须包括：raw 落档身份、成员、棒次、候选、N-1/N-2 审查或修订理由、
  三层评分结构、收敛探针，并保持中文主叙述。
- Codex 如果也是接力链成员之一，它的 baton raw 必须和其他成员同格式同骨架，而不是
  conductor 摘要、争议点摘录、web evidence raw 或 round archive 替代物。Codex 成员 raw
  至少必须包括：N-1/N-2 审计、完整候选译文（能让下一棒直接评价）、相对上一棒的继承/必须改项或
  争议点矩阵、三层评分、收敛探针、明确 next-baton handoff。若 Codex 是某轮最后一棒，
  下一轮第一棒的 handoff 必须写明它要评价的 N-1/N-2，例如当前 Web/Hybrid R2B1 哈基米
  应评价 `N-1 = Codex R1B5` 与 `N-2 = 小G R1B4`。反向阻断：不得把轮末合并档、
  web-access 证据 raw、几句样例或争议摘要当作 Codex 成员报告；不得让下一棒没有可评价的
  Codex 完整候选。
- Combined round archive must include: `<reply-drop>` path,
  all five baton outputs in baton order, raw capture index, convergence index,
  checkpoint state, resume state, next-step inputs, Chinese main narrative, and
  syntax/morphology analysis whenever a candidate is presented for review.
  On R2/R4/R6 even rounds, the combined archive may and normally should also
  contain the divergence/non-divergence analysis section; in that case no
  separate divergence report file is required.
- Checkpoint summary/report must include: explicit stop-and-wait state, user
  options (continue / revise / Deep Research / accept or close out), current
  round and baton, latest candidate, locked user decisions, open disputes,
  next-baton prompt inputs, round archive path, research TODOs, and strict
  exact-text convergence state.
- R2/R4/R6 divergence or non-divergence section/report must include:
  even-round marker, dispute trajectory, candidate trajectory,
  convergence-vs-divergence judgment, N-1/N-2 drift analysis, catalyst / AI
  mirror-risk analysis, explicit non-divergence or early-convergence reason
  when applicable, syntax/morphology analysis, and checkpoint advice. This may
  be an embedded section in the even-round combined archive or an optional
  standalone report.
- Final `Translation-report.md` must include: final-output gate evidence,
  separate translation-only `Translation*.txt` reference, metadata, source and
  context anchors, complete user input, the prep context package summary
  (for 《古董局中局》 tasks this includes the 小D 译前上下文包摘要版 when used),
  an explicit input-boundary note distinguishing context from source text,
  final translation, relay trajectory, Google/DeepL baseline comparison when
  available, three-layer scoring with `S_norm`, detailed syntax/morphology,
  direct-vs-conversion audit, translation highlights, sound/prosody notes,
  research TODO or `N/A`, compliance self-check, artifact list, and Chinese
  main narrative.
- 2026-07-04 bilingual Antique rule: for 《古董局中局》 Japanese translation tasks
  where the user gives Chinese source/input plus English translation/reference
  points, the final `Translation-report.md` must include a dedicated
  `english_section. It must preserve all material points from
  the English side, divergence axes against the Chinese source/input, and how
  each point affected or did not affect the Japanese final choices. Do not
  compress the English side into "style only", omit it from the final report,
  or treat it as subordinate to Chinese source text. This section is later KB
  backfill input, but the primary capture point is before 小D prepares the
  `译前上下文包`.
- Every artifact type that presents a candidate or final translation must use
  the full syntax/morphology minimum from `spec-v0.3.12.md`, not a title-only
  placeholder: sentence overview, approximate literal back-translation,
  phrase/particle/honorific breakdown, dependency JSON with source alignment,
  lexical morphology table, strategy tags, and direct-vs-conversion audit.
  Short source text requires finer granularity, not a shorter report.
- USER_SOURCE 2026-07-05: after the rebuilt archive still used a shallow
  formulaic syntax/morphology shell, the user corrected that even aside from
  source incompleteness, the syntax/morphology analysis itself was
  unacceptable and should already have had a gate. Exact claim: `句法构词分析`
  cannot be satisfied by a six-field table whose rows repeat generic phrases
  such as `source-lock OK`, generic `root=疑問句/述語句`, generic particle/
  honorific wording, or a copy-pasted Addition/Omission/Free rewriting sentence.
  Derived executable rule: every per-line or per-line-group detail block must
  name the actual predicate/root or sentence function for that line, cite
  concrete target-language tokens and morphology/particle/honorific/register
  choices, and make the direct-vs-conversion audit point to the specific source
  anchor and translation choice under review. The overview table may summarize,
  but it cannot contain a repeated placeholder judgment as the only "analysis."
  For long dialogue passages, D-level line groups require source-specific
  syntax/morphology discussion; short lines require sharper granularity, not a
  shorter empty report. Negative blocker / anti-rule: do not pass an artifact
  merely because it has headings for `译句 / 近似直译 / root / 构词 / 源文锚点 /
  直译与转换审计`; do not reuse boilerplate rows, repeated root values, repeated
  morphology cells, repeated direct-conversion audit text, or `R2 can polish`
  placeholders as a substitute for analysis depth. Machine check:
  `scripts/translate_v2_artifact_lint.py --type round-archive` and
  `--type final-report` now block repeated syntax/morphology boilerplate and
  too-thin per-line fields; the current bad rebuilt surface must report
  `TRANSLATE_V2_ARTIFACT_LINT_STATUS=BLOCKED`, while a rebuilt archive with
  line-specific roots, morphology, and audit cells must report OK before it can
  be used as N-1/N-2 or handoff evidence.
## 2026-05-27 Runtime Guardrail: Author Reference Samples Are Optional Dual Evidence

- The user may sometimes provide their own translation in another language
  (often English) as an author reference sample, but this is optional. Do not
  require or imply that every translation task must include the user's English
  version or any second-language reference.
- When both the source text and an author reference translation are provided,
  treat them as dual authorial evidence, not as a master/subordinate pair and
  not as a crude split where one "locks facts" and the other "locks style".
  Both may contain factual/information boundaries and both may reveal creative
  strategy, rhythm, voice, compression, and aesthetic handfeel.
- The two samples may deliberately use different creative routes. Example
  pattern: the Chinese source may lean toward film/novel dialogue while the
  user's English reference may lean toward raw real-life speech. Do not force
  them into one identical style. Extract the shared scene function, character
  relation, information density, explicit/implicit balance, tone pressure, and
  sound/cadence intent; then choose the target-language route that best fits
  the requested genre and target-language conventions.
- If the samples diverge, record the divergence axis explicitly before drafting
  or scoring: cinematic vs raw speech, literary vs documentary, complete
  grammar vs controlled fragments, high cadence vs plainness, compression vs
  fuller line, foreignizing vs domesticating, etc. The final translation may
  follow the source route, the author-reference route, or a third target-
  language route, but the choice must be justified against the source anchors
  and the user's stated intent.
- Do not let an author reference translation override hard red lines. It is
  high-priority author evidence for intent and technique, but the final target
  text must still avoid Addition, Omission, Mistranslation, Hallucination,
  unlicensed background expansion, or unanchored changes to who knows/feels/
  does what.

## 2026-07-05 Research Intake Guardrail: Audience And Medium Before Style Rules

- Translation research, Deep Research reports, web-access captures, social
  platform notes, and member reports are evidence, not automatic rules. Before
  using them in any translate-v2 prompt, style sheet, prep package, baton brief,
  or final report, classify each point as `MUST_RECORD`,
  `PENDING_STYLE_EVIDENCE`, or `MUST_NOT_RECORD`.
- A point can become `MUST_RECORD` only when it is a user rule/correction,
  a source-authoritative fact, a verified recurring failure gate, or a direct
  artifact contract. A member-only recommendation, social-platform sample,
  edition-specific publishing habit, or provisional style suggestion stays
  `PENDING_STYLE_EVIDENCE` unless the user explicitly adopts it for the active
  task.
- Always separate audience and medium before applying style advice: source
  manuscript, embedded foreign-language dialogue inside a Chinese novel,
  Japanese-reader publication, character list, audiobook/subtitle/voice acting,
  editorial style sheet, terminology memo, official documents, and social/admin
  identity use are different surfaces. Advice from one surface may be cited as
  background for another, but it may not override the active surface.
- For Chinese names in Japanese translation research, keep three layers
  separate: written form, reading, and ruby/furigana. General reusable evidence:
  Chinese names in Japanese prose often use Japanese-usable kanji forms rather
  than raw simplified Chinese or blind traditionalization; readings may be
  Japanese on-yomi or Chinese local-sound katakana depending on medium and
  style sheet; ruby frequency is an editorial decision, not the name
  translation itself.
- Project-specific override: when `the Antique Game Within Game companion skill` is active, its
  user-locked Chinese-reader rule wins. For 《古董局中局》 embedded Japanese
  dialogue, the current default is no ruby/furigana/pinyin/phonetic assistance
  in body text; reading information belongs in prep notes, term memos, or
  user-requested appendices unless the user opens a specific exception.
- Anti-rule: do not convert a crooked or overbroad research report into a
  locked style rule merely because it contains useful facts. Do not turn
  “Japanese readers may benefit from ruby/person lists” into “every Chinese
  novel translation must add ruby,” and do not turn Chinese students'
  real-name/visa/name-card reading choices from social platforms into
  publishing or fiction-dialogue rules.
- Required prompt/report wording when research is used: name the surface
  (`current Chinese novel body`, `hypothetical Japanese-reader edition`,
  `character list`, `audiobook`, etc.), the status
  (`LOCKED_USER`, `PENDING_STYLE_EVIDENCE`, or `MUST_NOT_RECORD`), and the
  blocker that prevents over-application. Missing that disposition makes the
  research unsafe as downstream relay evidence.

## 2026-07-05 Dialogue Spoken-Form Guardrail: Chinese-Reader vs Japanese-Reader Surfaces

- `USER_SOURCE`: 2026-07-05 user clarification after Chinese-name/ruby
  research: in the user's current fiction, Japanese personal names have so far
  used Japanese readings. If the user later wants a Chinese name in Japanese
  dialogue to be pronounced in Chinese local sound, a Chinese-reader work whose
  Japanese dialogue is followed by Chinese translation may write katakana-only,
  not corresponding Japanese kanji plus ruby. For a Japanese-reader work, also
  in character dialogue, the preferred local-sound surface is
  `フー・チンタオ（胡錦濤）`, not `胡錦濤（フー・チンタオ）`.
- `EXACT_CLAIM`: both cases are character dialogue. In dialogue, the text
  outside parentheses is what is spoken/read; parenthetical text is identity
  explanation or annotation. Chinese-reader embedded dialogue does not need
  ruby/furigana/pinyin/phonetic aid to teach pronunciation when a Chinese
  translation follows. If local sound is intended, write the spoken sound
  directly as the dialogue surface.
- `DERIVED_RULE`: Any translate-v2 prompt, style sheet, prep package, baton
  brief, or final report that discusses Chinese names, readings, ruby, or
  katakana in dialogue must first classify the audience surface:
  `Chinese-reader embedded dialogue`, `Japanese-reader dialogue edition`, or
  `non-dialogue reference/annotation`.
  - For Chinese-reader embedded dialogue with following Chinese translation:
    default remains no ruby/furigana/pinyin/phonetic assistance in body text;
    current/default names keep their established Japanese readings unless the
    user explicitly opens a local-sound exception. If the user explicitly wants
    Chinese local sound, write the spoken form directly as katakana-only
    dialogue text, e.g. `フー・チンタオ`.
  - For Japanese-reader character dialogue where Chinese local sound is the
    intended spoken sound: write katakana outside and kanji identity inside,
    e.g. `フー・チンタオ（胡錦濤）`.
  - `胡錦濤（フー・チンタオ）` belongs to reference/news/annotation-style surfaces
    only when that is explicitly the desired medium. In dialogue, it puts kanji
    in the spoken slot and defaults the line toward Japanese kanji reading.
- `ANTI_RULE / NOT_AUTHORIZED`: Do not globalize katakana-only to all names; do
  not add ruby/furigana to Chinese-reader body text merely because a name has a
  Chinese local sound; do not use kanji-outside plus kana parenthetical for
  local-sound dialogue unless the user explicitly asks for a non-dialogue
  reference/annotation style; do not treat this as a bibliography, character
  list, news, or official-identity rule.
- `SCOPE/STATUS`: `MUST_RECORD` for translate-v2 dialogue style decisions,
  prompts, prep packages, member instructions, reports, and reviews involving
  Chinese names/readings/ruby/katakana in character dialogue. For
  `the Antique Game Within Game companion skill`, the project-specific locked rule in that skill
  remains the direct project authority; this section is the cross-translation
  reusable surface gate.
- `MACHINE/MANUAL PREFLIGHT`: Before sending or accepting any translate-v2
  surface that discusses Chinese names in dialogue, state: audience surface,
  spoken-form order, whether the user explicitly requested local sound, and the
  anti-rule that prevents ruby or kanji-outside leakage. The execution gate in
  `<tools-root>/scripts/translate_v2_contract_gate.py` must block the bad fixtures
  below and pass the good fixtures below.
- `BAD FIXTURE / EXPECT BLOCKED`: Chinese-reader embedded dialogue says
  Chinese local sound should be written as Japanese kanji plus ruby or
  `胡錦濤（フー・チンタオ）`; Japanese-reader character dialogue intending Chinese
  local sound writes `胡錦濤（フー・チンタオ）` as the line.
- `GOOD FIXTURE / EXPECT OK`: Chinese-reader embedded dialogue keeps body text
  no-ruby and, only when the user explicitly wants Chinese local sound, writes
  katakana-only spoken text such as `フー・チンタオ`; Japanese-reader character
  dialogue intending Chinese local sound writes `フー・チンタオ（胡錦濤）`.

## 2026-05-27 Runtime Guardrail: Sound And Cadence Are Cross-Genre Quality

- Check sound and cadence in every translation, not only poetry. A good target
  text often wins because it reads aloud well: sentence length alternates,
  stresses land cleanly, pauses feel placed, and clauses have momentum.
- For fiction/dialogue and film-like lines, oral smoothness can justify lexical
  choices that are not dictionary-nearest. Example pattern: a word such as
  "honestly" may carry tone and cadence better than a heavier literal option
  if it preserves meaning and makes the line sound like real screen dialogue.
- Track sentence-length design at passage level. Avoid making every sentence
  equally long, equally complete, or equally compressed. Long-short contrast,
  staggered rhythm, and breath control can be part of fidelity when the source
  or target genre wants literary/script readability.
- Track wording, phrase, construction, and sentence-pattern echo at passage
  level. Reusing the same word, phrase, syntactic construction, connector,
  condition marker, reporting verb, address term, or sentence frame can be good
  when it creates intentional cohesion, callback, pressure, motif, comedy,
  ritual cadence, or character voice; do not erase useful echo just for
  variety. But do not let an entire passage mechanically repeat the same word,
  phrase, construction, or sentence pattern until the prose goes flat. Example:
  if `if` has already saturated a long English reference/passage, a
  source-compatible alternative such as `given` may be better when it preserves
  the intended reasoning/probing flavor and avoids monotonous repetition.
- Repetition review must be passage-level and source-bound: ask whether the
  repeated word/phrase/construction/sentence pattern is doing artistic or
  discourse work, and whether varying it would preserve meaning, character
  voice, logic, and rhythm. Anti-rule: do not ban repeated wording globally, do
  not force thesaurus or syntax variation that breaks a deliberate echo, and do
  not keep repeating a dictionary-correct word, phrase, or frame just because
  each isolated sentence can defend it.
- Look for accidental useful sound structures: anaphora, epistrophe, chain
  repetition / 顶针, internal rhyme, light end rhyme, alliteration, assonance,
  consonance, and parallel cadence. Preserve or recreate them when they fit the
  target genre.
- Sound beauty is not a license to drift. Do not force rhyme, alliteration,
  顶针, slogan-like punch, or pretty cadence if it changes meaning, adds
  emotion, weakens academic/legal precision, or violates Addition/Omission/
  Mistranslation/Hallucination.
- Scoring must treat dead, same-length, translationese rhythm as a possible
  `rhythm_prosody`, `voice_register`, `fluency_mechanics`, or
  `reader_reachability` issue, even in non-poetry genres.

## 2026-05-27 Runtime Guardrail: Translation Is Constrained Re-Creation

- Treat translation as constrained re-creation, not lexical transport. The
  target text must read as a publishable/usable instance of its target genre:
  novel dialogue must read like novel dialogue, prose like prose, academic
  writing like academic writing, legal/technical writing like controlled
  professional text.
- The constraint boundary is strict: no Addition, Omission, Mistranslation, or
  Hallucination; do not add background facts, motives, explanations, emotions,
  or plot knowledge that the source has not expressed or strongly licensed.
  But inside that boundary, allow target-language sentence restructuring,
  cadence design, discourse particles, tone re-creation, idiom replacement,
  and information-order adjustment when the genre requires it.
- Preserve rhetorical and logical relations, not necessarily source surface
  order. Target-language order may differ from source order when meaning,
  emphasis, emotional/rhetorical pressure, who-does-what, causality, and
  information hierarchy remain intact and the target reads better. Example:
  Chinese `A 不说，还 B` may become `B, not to mention A` when the additive or
  escalating pressure survives. Anti-rule: do not call order reversal an error
  solely because source order differs; also do not use this flexibility to
  invert causality, change focus, erase escalation, or demote a source-important
  item into a weaker position.
- Do not execute "literal-first" as word-order copying or line-by-line
  mechanical repair. Its correct meaning is: preserve recoverable meaning,
  information density, explicit/implicit balance, rhetoric, and auditable source
  anchors. A translation can be faithful while changing syntax substantially if
  the target genre demands that shape.
- Genre route before drafting and scoring:
  - fiction/dialogue: character voice, scene pressure, subtext, breath, and
    literary readability are core fidelity signals;
  - literary prose/essay: rhythm, image continuity, sentence-group breath, and
    aesthetic density may justify larger syntactic re-composition;
  - academic paper: conceptual boundaries, argument relations, hedge strength,
    citation stance, and terminology consistency outrank literary elegance;
  - legal/technical/contract: definitions, conditions, scope, negation,
    enumeration, and traceability outrank elegance; creative latitude is low.
- Do not punish a high-quality literary translation merely because it is not
  surface-literal. Penalize it only when the creative move breaks the red lines,
  changes who knows/feels/does what, changes rhetorical force, or makes the
  source no longer auditable.
- Conversely, do not reward "complete coverage" if the target text is not
  genre-credible. A translation that contains all dictionary meanings but reads
  like a gloss, school exercise, UN speech, or syntax autopsy can be a major
  `voice_register`, `strategy_coherence`, or `reader_reachability` failure.

## 2026-05-27 Runtime Guardrail: Spoken Register Is Not Formal Completeness

- For any translation task with dialogue, live speech, chat, oral argument,
  interview, testimony, negotiation, character speech, or a source line that is
  already in the target language / a foreign language inside the story, run a
  spoken-register preflight before drafting or scoring.
- Do not equate "good target language" with complete schoolbook grammar,
  polished business prose, conference-speech cadence, or mature formal
  politeness. Native and fluent speech often uses fragments, ellipsis,
  restarts, compressed word groups, discourse particles, dropped subjects, and
  pragmatic shortcuts. These may be required for fidelity.
- "Fluency" in oral scenes means immediate processability and believable
  speech, not full written syntax. A broken but clear phrase can be better than
  a grammatically complete sentence if the source/character demands clipped,
  non-native, improvised, or socially pressured speech.
- This is not an instruction to break all dialogue. If the user/source is
  aiming for polished film-dialogue beauty, dramatic clarity, controlled
  literary speech, or a character who naturally speaks in complete sentences,
  keep grammar substantially complete and let rhythm, word choice, and line
  breaks carry the oral quality. Over-fragmentation, fake casualness, or
  needless broken grammar is also a `voice_register` defect.
- When a character speaks a non-native language, code-switches, or the source
  deliberately contains non-standard target-language wording, first decide
  whether the brokenness is an authorial/character strategy. Preserve controlled
  non-native or fragmentary voice unless the user asks for standardization.
  Only repair points that block comprehension, create unintended meaning, or
  contradict the intended character voice.
- Reject "UN speech / business email / school composition" upgrades in
  ordinary oral scenes: phrases that are correct but over-complete,
  over-polite, HR-like, explanatory, or written-register must be marked as
  `voice_register` / `fluency_mechanics` / `reader_reachability` issues, often
  major when they make a character sound unlike themselves.
- For scoring, do not award high `fluency_mechanics` merely because grammar is
  standard. Check target-language spoken naturalness, breath length, sentence
  fragments, turn-taking, relationship pressure, age/status fit, and whether a
  native/fluent listener would hear it as live speech rather than a prepared
  statement.
- For scoring, also do not punish complete grammar by itself. Penalize it only
  when it creates school-composition, UN-speech, business-email, or
  over-polished effects against the requested oral style. If the requested mode
  is cinematic dialogue, clean grammar plus sharp cadence can be correct.
- This guardrail is global, not Antique-only and not English-only. Apply it to
  Japanese, English, Chinese, and any target language. For Japanese specifically,
  beware of over-layered `いただければと存じます` / mature business-keigo in
  youth or live-scene dialogue unless the character's role genuinely calls for
  it.

## 2026-05-09 Codex Localization

- Core algorithm remains `spec-v0.3.12.md`.
- `SKILL.md` is a Codex fork entrypoint, not the CC-side long runtime manual.
- Normal Codex operation must not read Claude Code `claude-mem` or
  `<claude-config>/projects/.../memory`.
- Automatic relay should use `ask_cc` for the CC baton. The user does not want
  copy/paste prompt relay into CC.
- If `ask_cc` fails, treat it as an infrastructure/login blocker, not as a
  reason to silently remove CC from the relay.
- 2026-05-09 user decision: in the Codex-led fork, swap Codex and CC positions.
  Normal chain is `哈士奇 -> 小D -> CC -> 逗比 -> Codex conductor`.
- Codex conductor is the final baton and report owner: it writes R2/R4/R6...
  divergence analysis reports and the final `Translation-report.md`.
- `ask_codex` is no longer a routine relay baton; reserve it for explicit side
  reviews or extra Codex perspectives.
- Codex fork precedence: `SKILL.md` overrides upstream `spec-v0.3.12.md` for
  actor names, relay order, whiteboard paths, memory access, and report owner.
  The spec remains authoritative for the translation algorithm and artifact
  content schema.
- Primary final outputs for ordinary translate-v2 tasks live under
  `<translate-output-root>/`.
- 2026-05-21 project override: when a task also triggers
  `the Antique Game Within Game companion skill` for 《古董局中局》, final translation-only files and
  final analysis reports live under the chapter subdirectory matching the local
  adjusted layout:
  `<translate-output-root>/《古董局中局》/<部章>/`.
  Existing folders include `第一部第三章`, `第一部第四章`, and `第一部第八章`.
  These are examples only, not fallback targets. Derive `<部章>` from the
  current target chapter path/title, chapter card, or explicit user scene
  location; never reuse the previous Antique Game chapter directory. Create the
  matching `<部章>` folder if missing. If the current chapter cannot be
  determined, stop and ask/locate it before writing final files. This override
  is only for final `Translation*.txt` and `Translation-report*.md`
  deliverables; other translation tasks still output directly under `output/`.
- 2026-05-21 Antique project prep addendum: when 小D is used to draft a
  `译前上下文包`, give it the corresponding Antique chapter output directory
  above and require it to inspect all existing `*Translation-report*.md` files
  in that chapter directory. Translation prep and chapter ingestion use the
  same report-reading rule: group reports by exact source passage/task
  identity, then read the latest report in every distinct group (filename
  timestamp preferred, else mtime). Only duplicate reports for the same
  source/task collapse to one latest report. Do not take one latest report for
  the whole chapter, and do not filter to only the current target passage. If
  the chapter has no reports, record `NO_TRANSLATION_REPORTS_FOR_THIS_CHAPTER`.
  Do not feed it a pile of report `.md` files.
- 2026-05-25 Antique project execution gate: when a translate-v2 task also
  triggers `the Antique Game Within Game companion skill`, rereading skill files is not enough.
  Before any 小D prep prompt, Web/manual relay prompt, or user-facing
  `译前上下文包`, Codex must execute the Antique 2026-05-25 checklist in
  `the Antique Game Within Game companion skill/NOTES.md`: include
  manuscript root, official KB root, target chapter path/title, matching
  chapter output/report directory, all-report-groups rule, source/task
  latest-per-group rule, source-boundary rule, reply-drop/output path, and
  canonical template/script status. If the
  canonical prep script cannot run or lacks the chapter card, record the
  blocker explicitly instead of silently freeforming.
- 2026-05-27 Antique side-door anti-regression: the prep state machine also
  binds Codex's own answers and Web relay prompts. For 《古董局中局》 translation,
  Codex must not output a local translation recommendation, write a Web Relay
  R1/R1B1 prompt, dispatch a formal relay, or create final translation files
  until a `译前上下文包` has been verified by Codex and audited/corrected by the
  user. This is true even if 小D is not mentioned in the current turn. Accident
  review/root-cause answers are allowed only when the action explicitly says
  no translation, no prompt, and no dispatch. The executable regression marker
  is `antique-translation-prep-state-not-user-audited` in
  `<tools-root>/scripts/translate_v2_contract_gate.py`.
- 2026-05-27 full-restart correction: if the user explicitly says `重开 tab`,
  full restart, or no handover, do not write `<desktop>/prompt-codex.txt` and
  present it as translate-v2 progress, delivery, or next-tab continuity. The
  scratch prompt path remains valid only for an immediate current manual-relay
  action. If the user rejects prompt落档 as a side channel, delete the file and
  do not treat it as relay state.
- 2026-05-27 Non-Antique boundary: this side-door gate is project-scoped, not
  a global translation restriction. Ordinary non-《古董局中局》 translation tasks
  may still produce a direct answer or formal `translate-v2` relay prompt under
  normal `translate-v2` rules. The gate should activate only for a positive
  Antique context (`the Antique Game Within Game companion skill` active, or the task actually about
  《古董局中局》 / Antique Game). Negative phrases such as `非古董局中局`, `不是古董局中局`,
  and `not antique` are exclusion evidence, not project triggers.
- Default output behavior: create new task-specific files in the selected
  output directory
  (for example `YYYYMMDD-HHMMSS-{topic}-Translation.txt` and
  `YYYYMMDD-HHMMSS-{topic}-Translation-report.md`). Do not overwrite existing
  `Translation.txt` / `Translation-report.md` unless the user explicitly asks
  to overwrite. This rule was changed by user decision on 2026-05-14 after
  repeated CC-side mistakes made versioned outputs preferable.
- 2026-05-22 final-output gate: do not create final `Translation*.txt` or
  `Translation-report*.md` merely because a relay reached strict convergence or
  a baton recommended finalization. Step 5 may run only after one of two
  explicit user-confirmed states:
  (1) strict three-baton convergence has been reached and, at checkpoint, the
  user says they are satisfied / accepts / asks to close out; or
  (2) the round ends without convergence, but the user compares the candidates,
  chooses the most satisfactory translation, and asks to use it as final.
  Otherwise stop at checkpoint and keep any written materials as round/archive
  or provisional artifacts, not official final outputs.
- Mirror `<desktop>/Translation.txt` only as an explicit convenience
  copy when useful/requested.
- For long translation runs, every round checkpoint should include a compact
  resume state so automatic context compaction cannot lose the next-baton
  prompt inputs or user-locked decisions.

## 2026-05-25 Runtime Guardrail: Web Relay Is Default

- Per user decision on 2026-05-25, `translate-v2` defaults to `网页版接力`.
  Do not ask a channel-choice question when the user has not specified a
  channel; record the runtime channel as default `网页版接力`.
- Use `CLI 端接力` only when the user explicitly says `CLI 端接力`,
  `CLI 版接力链`, `走 CLI`, or equivalent for that task. Do not infer CLI from
  habit, automation convenience, local file access, or previous runs.
- Web Relay Mode is an endpoint mapping layer, not a different translation
  algorithm. Keep serial baton order, N-1/N-2 context, §3.1 principles, 14-
  dimension scoring, round archives, checkpointing, convergence, and final
  report schema unchanged.
- In the Codex fork, normal CLI chain is
  `哈士奇 -> 小D -> CC -> 逗比 -> Codex conductor`; Web/Hybrid Relay Mode maps
  this to `哈基米 -> 小D -> 小克 -> 小G -> Qoder` unless the user explicitly names a
  different endpoint for a baton. User correction on 2026-07-06 supersedes the
  2026-07-05 `... -> Codex` chain: this is now the default manual-relay chain;
  包子 and Codex exit the ordinary relay-member chain unless explicitly named,
  小G is the fourth baton, Qoder is the fifth baton, and Codex remains conductor
  for prompt packaging, linting, raw-capture verification, combined round
  archives, checkpoint judgment, divergence analysis, final reports, and
  user-facing synthesis.
- 2026-07-05 user correction: 老D / DeepSeek Web must be removed from the
  default translation relay second-baton slot and replaced by 小D. Reason:
  老D had no usable联网/search mode in the observed route but still produced
  apparent `NotebookLM` / dictionary / ordinary-search "补查" claims, making
  the result capability-mismatched rather than valid evidence. Positive rule:
  future prompts use `哈基米 -> 小D -> 小克 -> 小G -> Qoder`. Negative blocker:
  do not send dictionary- or web-search-dependent补查 tasks to 老D; do not
  treat 老D claims of lookup/search evidence as valid unless a current preflight
  proves the exact route has the required联网/词典 capability. Old
  `哈基米 -> 老D -> 小克 -> 包子 -> 小G` may appear only as rejected/deprecated
  history.
- USER_SOURCE 2026-07-06: user changed the future default Web/Hybrid relay
  chain to `哈基米 -> 小D -> 小克 -> 小G -> Qoder`, explicitly replacing Codex as
  the fifth relay-chain member because the user does not trust the two ChatGPT
  members inside the relay. Exact claim: Qoder must not be lazy; Qoder must use
  its `web-access` skill/route, search source-language and target-language
  websites that other members cannot easily access, search comprehensively, and
  write the results comprehensively, "和哈基米那边查词典一个道理". Derived
  executable rule: all future ordinary Web/Hybrid relay prompt packages,
  handovers, round archives, and lint fixtures must use
  `哈基米 -> 小D -> 小克 -> 小G -> Qoder`. Qoder fifth-baton prompts must include a
  conspicuous no-lazy web-access research contract: use web-access; cover both
  source-language and target-language sources/platforms; include hard-to-access
  or real-user/social platforms such as 小红书 where relevant; enumerate every
  disputed segment/term/register/honorific/source-boundary issue checked; mark
  misses as not found / cannot verify; and list all searched items, chosen and
  rejected evidence, remaining risk, and source URLs/notes. Negative blocker /
  anti-rule: do not leave Codex as the live fifth baton in the default chain; do
  not use Qoder as a thin local-file reviewer; do not allow Qoder to claim
  "查了但不列全" or provide only sample findings; do not let Codex perform the
  fifth-baton web-access pass by default; Codex may only conduct, lint, file,
  archive, and synthesize unless explicitly named as a relay member. Scope:
  future translate-v2 ordinary Web/Hybrid Relay Mode, MUST_RECORD. Machine
  check: `scripts/translate_v2_artifact_lint.py --type prompt-package` blocks live
  default chains ending in Codex and blocks Qoder fifth-baton prompts missing
  web-access/no-lazy/full-list requirements; `--type baton-raw` blocks Qoder raw
  that lacks web-access/source-language/target-language/comprehensive checked
  records.
- 2026-06-23 哈基米 NotebookLM 目标语词典升级：在普通 `网页版接力`
  中，哈基米 / Gemini Web 作为第一棒时必须充分利用 NotebookLM 的目标语词典。
  对不确定的翻译点（词汇、搭配、习语、语域、关键术语、重要理解点等），prompt
  必须要求哈基米先查目标语种的 NotebookLM 词典：中译英查英文词典，日译中查中文
  词典，其他语种按“目标语种是什么就查哪种语言词典”的同一规则执行。当前已接入
  中文、英语、日语词典；未来新增语种后自动纳入该规则。若目标语种尚未接入
  NotebookLM 词典，不强制查词典，哈基米按旧流程翻译。若目标语词典已接入但查不到，
  允许在普通联网搜索中查目标语用法证据；若原文释义、语义边界、典故、概念或事实指涉
  不明确，也允许哈基米普通联网确认源文理解。反向阻断：不得查源语词典冒充目标语词典；
  不得因为中/英/日是当前例子就把规则锁死成三语专用；不得让联网搜索或词典结果覆盖
  用户、源文、上下文、术语表、剧情事实或作者意图，也不得给源文额外添加无证含义。
- 2026-07-05 用户补充：NotebookLM 实际使用是一个语种一个笔记本；哈基米 prompt
  面向目标语笔记本提问即可。不要在给哈基米的复制块里把中文/英文/日语词典写成可切换的
  多选项，尤其不要让“当前已接入中文、英语、日语”喧宾夺主。正向要求：写清本任务目标语
  对应的具体词典区（如日译时直接在日语词典区问），并把需要查词典的具体日语问题逐项列出。
  反向阻断：不得把目标语词典说成“只用于不确定用法”的可选工具，也不得用泛泛 fallback
  代替针对源文、译前上下文包和用户说明提炼出的必查清单。
- 2026-07-05 用户再次纠偏：上述 NotebookLM 目标语词典强制只适用于哈基米
  / Gemini Web 第一棒。除哈基米外，小D、小克、包子、小G等后续成员不强制查
  NotebookLM 词典；后续棒应发挥各自通道优势，使用普通联网、日语在线辞書、语料、
  机构/法律/新闻用例、专业术语平台或其它可访问来源核验。prompt 可以要求后续棒
  审计哈基米是否漏查，但不得让它们背“哈基米词典必查清单”，也不得把不能访问的
  NotebookLM/网页写成已查证据；能力不足时写 `CANNOT_VERIFY_BY_THIS_CHANNEL`。
- 哈基米 Web prompt-package 必须显式写出上述词典分支和 fallback。实际 prompt
  写出后，运行
  `<tools-root>/scripts/translate_v2_artifact_lint.py --type prompt-package <path>`；
  缺 NotebookLM、目标语词典、目标语未接入降级、查不到后普通联网搜索 fallback、
  原文释义不明确时可联网确认的边界、或源语词典反向阻断时，不得发送给哈基米。
- Do not treat Web Relay Mode as web Deep Research. Deep Research remains a
  separate user-approved startup/checkpoint action.

## 2026-05-15 Runtime Guardrail: Web Relay Preflight Is Mandatory

- Before any `网页版接力` baton is sent, run a visible preflight checklist and
  record the result in the working notes/round archive:
  1. Baton order is `哈基米 -> 小D -> 小克 -> 小G -> Qoder`; Qoder is the fifth
     ordinary Web relay baton, not Codex, not a sixth extra baton, and not Deep
     Research unless the user separately triggers research. Qoder's fifth baton
     must use web-access and must provide a full, listed research/check record.
  2. Use the user's already prepared tab when they say they opened/configured
     one. Do not open a fresh tab for that member unless the existing tab is
     unusable or the user asks. A fresh tab is a fresh configuration state.
  3. Model/mode/capability must be verified for the actual endpoint. For 小D,
     use the established private/local 小D route appropriate to manual relay.
     For 小克 use the highest visible model such as Opus/Adaptive when
     available; for 包子 use the strongest ordinary chat mode and do not switch
     into Deep Research/translation-tool shortcuts. Do not substitute 老D for
     小D unless the user explicitly re-authorizes and a fresh capability
     preflight proves the exact 老D route can perform the required lookup/search.
  4. If the web UI has no explicit thinking-effort control, do not block the
     relay; record "no visible thinking control" in the archive. If it does,
     use the next-highest thinking amount unless the user says otherwise.
  5. Before clicking send, read back the input box and verify the full prompt is
     present: source text, target language, context constraints, N-1/N-2 where
     applicable, three-layer 14-dimension scoring instructions,
     `scores.language` / `scores.literary` / `scores.cultural` + `aggregate`,
     `S_raw/S_norm`, and
     checkpoint/convergence fields. If any required field is missing, do not
     send.
  6. After clicking send, verify the input box cleared and the page transcript
     contains the full prompt, not just the first paragraph. If only a prefix
     was sent, stop immediately and mark the attempt polluted.
  7. After the web member finishes, immediately write a raw capture under
     `<reply-drop>/` before dispatching the next baton. The raw
     file must include UTC timestamp, member/baton, page title/URL when
     available, full visible prompt/reply text, and validation flags for the
     required schema fields. Immediately run
     `<tools-root>/scripts/translate_v2_artifact_lint.py --type baton-raw <raw-file>`;
     for Antique Game tasks also run
     `the Antique Game Within Game companion skill/scripts/lint_chinese_main_artifact.py <raw-file>`.
     Missing raw capture or missing/pending/BLOCKED raw language lint means the
     baton is not yet eligible to become N-1/N-2.
  8. A baton is official only if preflight, post-send verification, raw
     capture落档, and `baton-raw` artifact lint all pass.
     Otherwise it is a polluted attempt and must not be used as N-1/N-2.

## 2026-05-14 Runtime Guardrail: 14-Dimension Scoring Is Mandatory

- A relay round is not a formal `translate-v2` round unless it applies the
  spec's three-layer 14-dimension scoring/review schema:
  `scores.language` / `scores.literary` / `scores.cultural` + `aggregate`.
- A relay round is also not formal unless each baton prompt includes §3.1
  translation principles at the top as the generation direction: 信达雅,
  constrained re-creation, genre routing, preservation of source information
  density / explicit-implicit balance / rhetorical function / auditable source
  anchors, Addition/Omission/Free Rewriting red lines, and structural or
  functional correspondence for later syntax/morphology analysis.
- R1 baton 1 must compare Google/DeepL drafts with the three-layer
  14-dimension scoring framework before producing its polished candidate.
- Baton 2+ must review the previous candidate through the same scoring/review
  framework before producing a revision.
- Relay prompts must preserve the previous two batons' translation results in
  full. Older batons can be summarized. If full commentary/scoring cannot fit
  or causes interface pressure, commentary may be summarized, but key issues,
  aggregate scores, and convergence state must remain.
- On API member timeout/disconnect during relay, retry the same model with the
  same thinking/effort once, allowing a long wait before declaring failure. If
  the retry also fails, stop API retries and switch to user-assisted manual
  relay. Do not step down to a faster/lower model unless the user explicitly
  asks for that fallback.
- Round archives, checkpoint handovers/summaries, even-round divergence reports,
  and final translation analysis reports must use Chinese as the main narrative
  language unless the user explicitly asks otherwise. This includes headings,
  baton summaries, review notes, checkpoint judgments, and next-baton package
  explanations. Necessary technical terms and schema labels such as
  `checkpoint`, `Issue list`, `S_norm`, model names, paths, and scoring field
  names may remain English when translating them would be awkward. Only
  translated text remains in the requested target language. Before reporting a
  round complete, self-check artifact language and repair any English-main
  archive text immediately; the user has repeatedly flagged this, so treat it as
  a hard operating rule, not a style preference.
- If a conductor accidentally runs a lightweight "简评 + 候选 + 取舍" relay
  without the three-layer 14-dimension schema, mark it as an informal trial, do
  not count it as an official round, and restart the official round from R1
  baton 1.

## 2026-05-14 Runtime Guardrail: Reports Must Match Sample-Level Detail

- Final `Translation-report` files and R2/R4/R6... divergence analysis reports
  must match the level of detail used by existing output samples under
  `<translate-output-root>/`, not a short rationale
  memo.
- Default final report structure should include: metadata, complete user input
  (verbatim where recoverable), prep context package summary, explicit
  input-boundary note, source text, context anchors, final translation, full
  relay trajectory table, baseline machine-translation comparison where available, full three-layer
  14-dimension GEMBA scoring by layers, `S_norm`/relative baseline rating,
  syntax/morphology
  analysis three-piece (dependency tree JSON, key lexical/morphological table,
  translation strategy table), translation highlights, prosody section
  (`N/A` when not applicable), research TODO section (`N/A` when none),
  compliance self-check, key spec/memory takeaways, and artifact list.
- Per user decision on 2026-05-15, syntax/morphology analysis must be written
  at the "teach and inspect" level, not as a terse schema artifact. Round
  checkpoint archives, every-round summary drop files, even-round divergence
  analysis reports, convergence reports, and final reports must include
  detailed sentence-by-sentence and phrase-by-phrase analysis whenever a
  candidate/final translation is being presented for user review. The expected
  quality is the revised Tanaka report style: sentence overview, approximate
  literal back-translation, phrase/particle/honorific breakdown, direct-vs-
  converted judgment, and explicit discussion points so the user can challenge
  meaning, register, and literalness even when they do not know the target
  language.
- Even when an even round converges early or does not visibly diverge, write an
  explicit "non-divergence / early convergence reason analysis" instead of
  omitting the divergence-analysis function. For true divergence, analyze
  repeated disputes, over-correction vs rollback, N-2/N-1 drift signals,
  catalyst absorption/loss, and whether user decision or research is needed.
- Short source text is not an excuse for a skeletal report. Mark irrelevant
  sections as `N/A` with a reason, but keep the report skeleton complete.

## 2026-05-14 Runtime Guardrail: Strict Convergence Means Exact Text Equality

- This applies to all future translation relays, not just the Tanaka JP run.
- The convergence index may increment only when the current baton's translation
  text is exactly identical to the immediately previous baton's translation
  text after ignoring non-substantive formatting differences.
- Ignore full-width/half-width forms, indentation, spacing, line wrapping, and
  other purely cosmetic layout differences. Do not be pedantic about these
  empty format differences when judging convergence, especially for CC/Claude
  outputs where fullwidth/halfwidth punctuation may be unstable and difficult
  to force.
- Substantive punctuation changes still break convergence when they alter
  sentence boundary, tone, or pragmatics, e.g. changing a period to an
  exclamation mark, question mark, ellipsis, or otherwise changing the actual
  punctuation function.
- Any wording, phrase, lexical choice, sentence order, register change, or
  punctuation with semantic/pragmatic force means the baton is not converged
  with the previous baton.
- Reviewer satisfaction, zero score, "no substantive difference",
  "micro-polish", and "only style polish" are never sufficient for convergence.
- At checkpoints and in handovers, record the convergence index using this
  exact-equality rule.

## 2026-05-15 Runtime Guardrail: Context Is Evidence, Not Source Text

- User-provided background, spoilers, character notes, prior reports, and deep
  research conclusions are high-priority evidence for disambiguation, register,
  terminology, and risk prevention. They are not extra source text to translate.
- Relay prompts must explicitly warn every baton: do not surface background
  facts, motives, plot mechanics, research conclusions, or inferred causal
  explanations in the translation unless the source text itself says or strongly
  implicates them at that point.
- The translation should preserve the source text's information density and
  degree of explicitness. If the source is low-density dialogue whose meaning
  is carried by context, the target text should not become explanatory dialogue.
- Necessary target-language scaffolding is allowed only to prevent ambiguity or
  ungrammaticality. Once the target reader can recover the intended meaning
  from the translated line plus context, adding more explanation is an
  Addition violation, even when the added content is true in the story.
- Each baton must distinguish "context used to choose wording" from "content
  added to the line" when explaining revisions. R2/R4/R6 divergence reports and
  final reports should flag any over-explicitness or density inflation as a
  potential Addition / style defect.

## 2026-07-05 Runtime Guardrail: Full-Line Analysis Requires Source-Locked Full Source

- Negative blocker: a line-number list, candidate-only pool, representative risk
  table, or UI screenshot is not a full source. Do not let `Line 161`/`Line 261`
  headings pass if their source anchors do not match the real first/last source
  dialogue. Do not use a contaminated round archive as N-1/handoff/member-review
  input until it is rebuilt and passes lint.
## 2026-05-14 Runtime Policy: PUA Is Not Globally Managed By translate-v2

- translate-v2 does not manage a global PUA on/off state.
- Codex's own PUA default is controlled by Codex-side config and memory.
- Other members keep their own default behavior unless the user explicitly
  changes that member.
- If a concrete PUA-related output/channel problem appears, handle it locally
  for that member/channel.

## 2026-07-10 Runtime Guardrail: 信息密度是 §3.1 常驻方法论·不靠用户临时催

- 降密度/信息密度审查是 §3.1 翻译原则的**常驻着重项**，不是每次靠用户临时
  catalyst 才做。每棒 prompt 的 §3.1 段必须含独立、显眼、着重的【★信息密度铁律】
  块（见 spec §3.1 已固化版），不得埋在【底线】【上下文证据边界】里一句带过，也不得
  只在临时审稿点里突出。
- 铁律内容（2026-07-10 用户校准）：
  - 降密度＝删译文自己多加的、源文/参考译文都没有的可有可无语气助词/赘词/包装；
    **不是砍原文的合法长句**（原文长句＝信息量长，就让它长）。
  - 保留原文本身有的语气助词/停顿（中文"嘛/呢"、英文 well），须在目标语找到对应承载，
    不得因"简洁/书面规范"删掉。
  - 方法：揣摩源文＋参考译文节奏，逐句对照译文抓"有没有能去掉的多余部分"。
  - 人物/语域分级只指密度上限严不严、不指句子长短（强势角色最严 ≠ 最短）。
- ★★上下文只作选词依据、严禁倒灌进译文（Addition 红线·重中之重·用户 2026-07-10
  着重重申）：用户给的一切解释、纠偏、背景、剧透、人设、前情报告、调研结论，用途只有
  「帮成员消歧、正确理解源文本意 ＋ 校准语域/稳定术语/避免误读」——是选词依据、不是
  待译内容（给成员看懂原文用的，不是让它们翻进去的料）。绝不许无脑填进译文：人物尚未
  知情的事实、后台真相、动机/阴谋/因果解释、研究结论、上下文推理，一律只在脑子里用来
  选对词，禁止显性写进对白（除非源文本句已明说、或强烈暗示到必须显化）。判据：读者凭
  "译文＋上下文"就能恢复原意后再加解释＝Addition（即使剧情为真）。每棒点评须自证区分
  "用背景校准了措辞"与"把背景写进了译文"，后者进 issue list。病根＝把用户"帮你理解"的
  解释/纠偏曲解成"替你加戏"。
- 反面：不得等用户催才降密度；不得把信息密度埋进其他原则一句带过；不得把用户提供的
  背景当"待译内容"塞进译文。
