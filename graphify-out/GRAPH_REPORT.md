# Graph Report - reshay-stats  (2026-11-07)

## Corpus Check
- 102 files · ~212,650 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 3 file(s) not represented in the graph (top: (none) 3)

## Summary
- 1206 nodes · 2953 edges · 54 communities (45 shown, 9 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 106 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `9a9c12db`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- json
- sys
- re
- scripts/mix.py
- assets.js
- ui_events.py
- hit
- from_cues.py
- unbake.py
- critique.py
- load_json
- ref_path
- resound.py
- common.py
- main
- beats.py
- from_synth.py
- maskmodel.py
- math
- listen.py
- refstyle.py
- from_hyperframes.py
- look.py
- masking.py
- env
- hear.py
- moment_test.py
- array
- analyse_sound
- collect.py
- decode_mono
- os
- Ponytail Help
- How the skill "hears" sound
- stereo_samples
- The blind "resound" test (`tests/resound.py`)
- Тексты для профилей «Решай сам»
- Handing the result to an editor
- plot_grid
- ponytail-audit/SKILL.md
- Ponytail Gain
- ponytail-review/SKILL.md
- Ponytail
- venv_python
- ponytail-debt/SKILL.md
- peak_events
- package.json
- s01/build.sh
- s02/build.sh
- CLAUDE.md
- .claude/CLAUDE.md
- find_stems
- scenariy.md
- README.md

## God Nodes (most connected - your core abstractions)
1. `main()` - 53 edges
2. `main()` - 43 edges
3. `main()` - 35 edges
4. `load_json()` - 34 edges
5. `load_index()` - 34 edges
6. `main()` - 25 edges
7. `rank()` - 25 edges
8. `unbake()` - 25 edges
9. `load_config()` - 24 edges
10. `effective_dur()` - 22 edges

## Surprising Connections (you probably didn't know these)
- `4. Choosing sounds for the main moments: look, do not guess` --references--> `water()`  [INFERRED]
  .claude/skills/real-sfx/SKILL.md → potop/art/assets.js
- `Kinds and what they become` --references--> `water()`  [INFERRED]
  .claude/skills/real-sfx/references/typed-cues.md → potop/art/assets.js
- `Libraries: what to watch for` --references--> `words()`  [INFERRED]
  .claude/skills/real-sfx/references/event-map.md → .claude/skills/real-sfx/scripts/common.py
- `How to read `REPORT.md`` --references--> `results()`  [INFERRED]
  .claude/skills/real-sfx/tests/resound.md → .claude/skills/real-sfx/scripts/listen_page.py
- `Where the sounds come from` --references--> `select()`  [INFERRED]
  .claude/skills/real-sfx/SKILL.md → .claude/skills/real-sfx/scripts/sheet.py

## Import Cycles
- None detected.

## Communities (54 total, 9 thin omitted)

### Community 0 - "json"
Cohesion: 0.05
Nodes (59): candidates(), main(), pieces(), scan(), tags_of(), usable(), effective_dur(), events_track() (+51 more)

### Community 1 - "sys"
Cohesion: 0.05
Nodes (47): build_film(), put_stem(), cmd_build(), cmd_ladder(), db(), duck_stem(), excerpt(), ff() (+39 more)

### Community 2 - "re"
Cohesion: 0.06
Nodes (39): norm_path(), run(), audio_level(), detect(), diff_series(), main(), probe(), refine() (+31 more)

### Community 3 - "scripts/mix.py"
Cohesion: 0.07
Nodes (28): arrive_offset(), channel_count(), clean_hits(), measure_loudness(), mono_drop(), show_name(), stereo_fmt(), window_levels() (+20 more)

### Community 4 - "assets.js"
Cohesion: 0.06
Nodes (45): Libraries: what to watch for, The map, What happens on screen → which sound, expand(), bgCellar(), bgCellarBoat(), boatBlanket(), crowd() (+37 more)

### Community 5 - "ui_events.py"
Cohesion: 0.06
Nodes (28): 1. Find the regions, 2. Regions and their kinds, 3. What the script cleans up itself and what to check, 4. Next, 5. What the script cannot see, 6. Screen recording metrics, Screen recordings: events by region, analyse() (+20 more)

### Community 6 - "hit"
Cohesion: 0.05
Nodes (43): Add your sounds, Install, Licences, Needs, real-sfx, Test, Use, What it will not do (+35 more)

### Community 7 - "from_cues.py"
Cohesion: 0.07
Nodes (24): centroid_window(), anchors_map(), assign_onsets(), bank_from_ids(), canon(), clean_pool(), detect_typing_runs(), estimate_time_map() (+16 more)

### Community 8 - "unbake.py"
Cohesion: 0.09
Nodes (27): _best_lag(), classify(), coarse_lag(), _corr(), _decode(), _decode_sum(), _dot(), _duration() (+19 more)

### Community 9 - "critique.py"
Cohesion: 0.07
Nodes (26): An event list without a list file, Rules, Sound already in the project: synthesis, stems, a synthesizer script, The loudness of the replaced layer and the author's chain, What the project has → what the script does, gesture_times(), grab(), clamp() (+18 more)

### Community 10 - "load_json"
Cohesion: 0.09
Nodes (24): _decode_text(), load_json(), read_stdin_text(), read_text_any(), ff(), main(), render(), apply_batch() (+16 more)

### Community 11 - "ref_path"
Cohesion: 0.07
Nodes (25): { chromium }, fs, path, { spawn, execFileSync }, {chromium}, fs, path, {chromium} (+17 more)

### Community 12 - "resound.py"
Cohesion: 0.10
Nodes (26): agreement(), band_balance(), cmd_check(), cmd_eval(), cmd_prepare(), cmd_prompt(), cmd_snapshot(), correlation() (+18 more)

### Community 13 - "common.py"
Cohesion: 0.14
Nodes (15): _catalog_key(), describe(), load_catalog(), main(), _num(), pack_record(), _read_catalog(), scan() (+7 more)

### Community 14 - "main"
Cohesion: 0.14
Nodes (15): check(), click_stem(), click_track(), ff(), fixture_library(), main(), beeps(), click_rms() (+7 more)

### Community 15 - "beats.py"
Cohesion: 0.11
Nodes (15): beat_grid(), check_grid(), decode(), detect(), detrend(), kick_peaks(), kick_phase_shift(), kick_stats() (+7 more)

### Community 16 - "from_synth.py"
Cohesion: 0.13
Nodes (16): _balanced(), extract(), find_functions(), take(), find_scripts(), from_objects(), instrument(), main() (+8 more)

### Community 17 - "maskmodel.py"
Cohesion: 0.13
Nodes (17): analyse(), ath_power(), band_power(), bark(), decode(), judged(), klass(), main() (+9 more)

### Community 18 - "math"
Cohesion: 0.14
Nodes (13): avg_power(), character_from_power(), _fft(), sound_features(), steadiness(), best_shift(), chroma(), _decode() (+5 more)

### Community 19 - "listen.py"
Cohesion: 0.21
Nodes (13): words(), compare(), describe(), have_runtime(), install(), main(), onsets_cmd(), reexec_in_venv() (+5 more)

### Community 20 - "refstyle.py"
Cohesion: 0.14
Nodes (12): aggregate(), _band(), bed_share(), compare(), export(), find_style(), gestures(), group_gestures() (+4 more)

### Community 21 - "from_hyperframes.py"
Cohesion: 0.15
Nodes (10): Collector, find_calls(), hint_of(), load(), resolve(), main(), num(), split_args() (+2 more)

### Community 22 - "look.py"
Cohesion: 0.25
Nodes (13): at(), esc(), events_sheet(), ff(), find_font(), frames_row(), label_filter(), main() (+5 more)

### Community 23 - "masking.py"
Cohesion: 0.16
Nodes (9): voice_share(), band_env(), lowend_collisions(), main(), masked_cues(), speech_active(), speech_activity(), sub_env() (+1 more)

### Community 24 - "env"
Cohesion: 0.11
Nodes (18): runs-on, steps, YT_API_KEY, YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN, jobs, collect (+10 more)

### Community 25 - "hear.py"
Cohesion: 0.25
Nodes (11): ask_model(), bench(), bench_captions(), ffmpeg(), have_model(), install(), main(), run_jobs() (+3 more)

### Community 26 - "moment_test.py"
Cohesion: 0.19
Nodes (10): build_moment(), candidates_for(), cmd_build(), current_cues(), _ir(), kpower(), loud150(), lufs_of() (+2 more)

### Community 27 - "array"
Cohesion: 0.21
Nodes (7): active_level_diff(), cue_levels(), full_env(), band_db(), main(), pauses_of(), segments()

### Community 28 - "analyse_sound"
Cohesion: 0.18
Nodes (6): analyse_sound(), arrival_landmarks(), decode_sound(), native_peak_db(), onset_time(), stereo_peak()

### Community 29 - "collect.py"
Cohesion: 0.21
Nodes (5): api(), load(), recent_comments(), rep(), retention()

### Community 30 - "decode_mono"
Cohesion: 0.22
Nodes (5): decode_mono(), baked_layer(), envelope(), synth_peak_times(), verify_stems()

### Community 31 - "os"
Cohesion: 0.18
Nodes (5): find_project_anchors(), kind_definitions(), matching_renders(), pchip_map(), probe_duration()

### Community 32 - "Ponytail Help"
Cohesion: 0.22
Nodes (8): Band (Claude Code), Configure Default Mode, Deactivate, Levels, More, Ponytail Help, Skills, Update

### Community 33 - "How the skill "hears" sound"
Cohesion: 0.22
Nodes (8): How the skill "hears" sound, How to read a spectrogram (level 1), Level 2: what gets installed and from where, Level 3: external "listeners", Levels, Separating "music / effects / speech" in references (researched, not built in), What else was found online (researched 2026-10-14, not adopted), What is left to the human ear

### Community 34 - "stereo_samples"
Cohesion: 0.22
Nodes (4): _fold(), fold_report(), louder_channel(), stereo_samples()

### Community 35 - "The blind "resound" test (`tests/resound.py`)"
Cohesion: 0.29
Nodes (6): How to read `REPORT.md`, Round 1 (skill 0.12.0, seed 635056751), as an example of reading, Steps, The blind "resound" test (`tests/resound.py`), Traps (all caught in round 1), What is needed

### Community 36 - "Тексты для профилей «Решай сам»"
Cohesion: 0.29
Nodes (6): Instagram (шапка), TikTok (до 80 символов), YouTube — описание канала, Имя, Тексты для профилей «Решай сам», Хештеги к серии 1

### Community 37 - "Handing the result to an editor"
Cohesion: 0.33
Nodes (5): After Effects, Handing the result to an editor, MP4 only, Premiere Pro, The source was made in HyperFrames

### Community 39 - "ponytail-audit/SKILL.md"
Cohesion: 0.40
Nodes (4): 1. Map first, 2. Look for, 3. Check before you report, 4. Output

### Community 40 - "Ponytail Gain"
Cohesion: 0.40
Nodes (4): Boundaries, Honesty boundary, Ponytail Gain, Scoreboard

### Community 41 - "ponytail-review/SKILL.md"
Cohesion: 0.40
Nodes (4): 1. Understand first, 2. Look for, 3. Check before you report, 4. Output

### Community 42 - "Ponytail"
Cohesion: 0.40
Nodes (4): Before you write, Levels, Ponytail, The smallest complete change

### Community 43 - "venv_python"
Cohesion: 0.40
Nodes (3): venv_python(), run_masking(), _need_numpy()

### Community 44 - "ponytail-debt/SKILL.md"
Cohesion: 0.50
Nodes (3): Boundaries, Output, Scan

### Community 46 - "package.json"
Cohesion: 0.50
Nodes (3): name, private, version

## Knowledge Gaps
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `water()` connect `assets.js` to `hit`?**
  _High betweenness centrality (0.077) - this node is a cross-community bridge._
- **Should `json` be split into smaller, more focused modules?**
  _Cohesion score 0.052564102564102565 - nodes in this community are weakly interconnected._
- **Why does `The map` connect `assets.js` to `load_json`, `hit`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
- **Should `sys` be split into smaller, more focused modules?**
  _Cohesion score 0.05016722408026756 - nodes in this community are weakly interconnected._
- **Why does `select()` connect `load_json` to `critique.py`, `assets.js`, `hit`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Should `re` be split into smaller, more focused modules?**
  _Cohesion score 0.05594679186228482 - nodes in this community are weakly interconnected._
- **Should `scripts/mix.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06708595387840671 - nodes in this community are weakly interconnected._