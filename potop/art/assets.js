// ПОТОП — общие SVG-ассеты сериала (плоский 2D, тёмная тревожная палитра).
// Каждая функция возвращает строку SVG-разметки. Фоны — в системе 1080×1920.
(function (g) {
  const P = {
    night: '#0a1018', night2: '#121b26', sky: '#1a2633',
    water: '#12303b', waterDeep: '#071820', waterLine: '#2f6474',
    wall: '#232d37', wall2: '#1d252e', wallEnd: '#2b3540', floor: '#1a1d21',
    door: '#3a2f28', door2: '#2e2520', paper: '#e6e1d3',
    lamp: '#e8c76a', lampSoft: '#f3dc96',
    red: '#d0473b', cyan: '#7fd1d9', brass: '#c9a24a',
    skin: '#d4bca6', skinSh: '#b9a08b', skinPale: '#d9d2c8',
    ink: '#101317', hair: '#1e1b20',
  };

  // детерминированный «рандом», чтобы кадры не дрожали
  function rng(seed) { let s = seed >>> 0; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296); }

  // ---------- ПЕРСОНАЖИ (viewBox 0 0 200 400, ступни на y≈390) ----------
  function ilya(o = {}) {
    const blink = o.blink ? 1 : 5, back = !!o.back;
    const front = back ? '' : `
      <path d="M80 150 L100 196 L120 150" fill="none" stroke="#2f3c43" stroke-width="5"/>
      <rect x="72" y="226" width="56" height="30" rx="11" fill="#34434a"/>
      <path d="M93 152 C 90 190, 106 205, 110 232" fill="none" stroke="${P.brass}" stroke-width="2"/>
      <rect x="104" y="224" width="16" height="9" rx="3" fill="${P.brass}"/><circle cx="117" cy="228" r="2.5" fill="#6d5520"/>`;
    const head = back ? `
      <rect x="86" y="120" width="28" height="34" rx="8" fill="${P.skinSh}"/>
      <circle cx="62" cy="100" r="9" fill="${P.skinSh}"/><circle cx="138" cy="100" r="9" fill="${P.skinSh}"/>
      <ellipse cx="100" cy="92" rx="42" ry="47" fill="${P.hair}"/>
      <path d="M70 118 Q100 134 130 118 Q124 130 100 134 Q76 130 70 118Z" fill="#14121a"/>
      <path d="M60 94 Q62 34 100 32 Q138 34 140 94" fill="none" stroke="#1b1f24" stroke-width="9" stroke-linecap="round"/>
      <rect x="52" y="86" width="20" height="30" rx="9" fill="#1b1f24"/><rect x="128" y="86" width="20" height="30" rx="9" fill="#1b1f24"/>
      <circle cx="62" cy="101" r="3" fill="${P.cyan}"/>` : `
      <rect x="88" y="128" width="24" height="22" fill="${P.skinSh}"/>
      <path d="M66 150 Q100 176 134 150" fill="none" stroke="#15181c" stroke-width="8" stroke-linecap="round"/>
      <circle cx="68" cy="148" r="13" fill="#1b1f24"/><circle cx="132" cy="148" r="13" fill="#1b1f24"/>
      <circle cx="132" cy="148" r="3" fill="${P.cyan}"/>
      <ellipse cx="100" cy="92" rx="40" ry="46" fill="${P.skin}"/>
      <path d="M124 60 Q144 92 124 128 Q138 92 124 60Z" fill="${P.skinSh}" opacity=".7"/>
      <path d="M59 92 C56 50 76 40 100 40 C124 40 144 50 141 92 C137 76 124 68 100 68 C76 68 63 76 59 92Z" fill="${P.hair}"/>
      <path d="M76 88 L94 82 M124 88 L106 82" stroke="${P.hair}" stroke-width="3.5" stroke-linecap="round"/>
      <ellipse cx="86" cy="98" rx="4.2" ry="${blink}" fill="${P.ink}"/><ellipse cx="114" cy="98" rx="4.2" ry="${blink}" fill="${P.ink}"/>
      <circle cx="87.5" cy="96" r="1.3" fill="#fff"/><circle cx="115.5" cy="96" r="1.3" fill="#fff"/>
      <path d="M79 107 Q86 111 93 107 M107 107 Q114 111 121 107" fill="none" stroke="#9c8373" stroke-width="2"/>
      <path d="M93 122 Q100 119 107 122" fill="none" stroke="#7a5f55" stroke-width="2.5" stroke-linecap="round"/>
      <path d="M134 86 q4 8 0 11 q-4 -3 0 -11Z" fill="#9fd0dd"/>`;
    return `<g class="ilya">
      <ellipse cx="100" cy="392" rx="58" ry="8" fill="#000" opacity=".35"/>
      <rect x="70" y="262" width="27" height="118" rx="9" fill="#27303d"/>
      <rect x="103" y="262" width="27" height="118" rx="9" fill="#232b37"/>
      <rect x="62" y="372" width="38" height="16" rx="7" fill="#7d858e"/><rect x="62" y="383" width="38" height="5" rx="2" fill="#a7adb3"/>
      <rect x="101" y="372" width="38" height="16" rx="7" fill="#737a83"/><rect x="101" y="383" width="38" height="5" rx="2" fill="#a7adb3"/>
      <g id="ilya-armL"><rect x="36" y="156" width="25" height="112" rx="12" fill="#34434a" transform="rotate(6 48 160)"/><circle cx="41" cy="270" r="11" fill="${P.skin}"/></g>
      <g id="ilya-armR"><rect x="139" y="156" width="25" height="112" rx="12" fill="#34434a" transform="rotate(-6 152 160)"/><circle cx="159" cy="270" r="11" fill="${P.skin}"/></g>
      <rect x="54" y="146" width="92" height="136" rx="28" fill="${back ? '#38474e' : '#3d4d55'}"/>${front}
      <ellipse cx="100" cy="144" rx="44" ry="18" fill="#34434a"/>${head}
    </g>`;
  }

  function vera(o = {}) {
    const beam = o.beam !== false;
    return `<g class="vera">
      ${beam ? `<defs><linearGradient id="vbeam" x1="0" x2="1"><stop offset="0" stop-color="${P.lampSoft}" stop-opacity=".55"/><stop offset="1" stop-color="${P.lampSoft}" stop-opacity="0"/></linearGradient></defs>
      <polygon points="170,238 420,170 420,330" fill="url(#vbeam)"/>` : ''}
      <ellipse cx="100" cy="392" rx="54" ry="8" fill="#000" opacity=".35"/>
      <rect x="76" y="280" width="20" height="100" rx="8" fill="#2a2730"/><rect x="104" y="280" width="20" height="100" rx="8" fill="#26232b"/>
      <path d="M70 352 h30 v34 h-34 q-2 -10 4 -12Z" fill="#3a2a22"/><path d="M100 352 h30 v22 q6 2 4 12 h-34Z" fill="#33251e"/>
      <g id="vera-armL"><rect x="42" y="158" width="23" height="108" rx="11" fill="#977429" transform="rotate(7 53 162)"/><circle cx="46" cy="268" r="10" fill="${P.skin}"/></g>
      <path d="M62 150 Q100 136 138 150 L150 302 Q100 312 50 302Z" fill="#a8842f"/>
      <path d="M100 150 L100 304" stroke="#8c6d25" stroke-width="3"/>
      <circle cx="108" cy="186" r="3.5" fill="#5a4517"/><circle cx="108" cy="222" r="3.5" fill="#5a4517"/><circle cx="108" cy="258" r="3.5" fill="#5a4517"/>
      <path d="M58 290 L66 168 M142 290 L136 168" stroke="#8c6d25" stroke-width="4"/>
      <g id="vera-armR"><rect x="136" y="158" width="23" height="84" rx="11" fill="#977429" transform="rotate(-40 148 162)"/>
        <circle cx="170" cy="232" r="10" fill="${P.skin}"/><rect x="160" y="226" width="26" height="13" rx="3" fill="#4a4f55" transform="rotate(-15 170 232)"/><circle cx="185" cy="227" r="5" fill="${P.lampSoft}"/></g>
      <ellipse cx="100" cy="150" rx="40" ry="14" fill="#8c6d25"/>
      <rect x="90" y="128" width="20" height="20" fill="${P.skinSh}"/>
      <path d="M58 98 Q56 44 100 42 Q144 44 142 98 L142 122 Q132 100 130 76 Q100 70 70 76 Q68 100 58 122Z" fill="#6b2f24"/>
      <ellipse cx="100" cy="94" rx="36" ry="42" fill="${P.skin}"/>
      <path d="M64 86 Q66 50 100 50 Q136 50 136 86 Q120 66 100 70 Q84 66 64 86Z" fill="#6b2f24"/>
      <path d="M134 112 q12 30 2 66 q-6 14 -10 0 q10 -34 2 -60Z" fill="#5a271e"/>
      <circle cx="134" cy="182" r="4" fill="${P.red}"/>
      <path d="M78 84 L92 86 M122 84 L108 86" stroke="#4a2018" stroke-width="3" stroke-linecap="round"/>
      <ellipse cx="86" cy="97" rx="4" ry="5" fill="${P.ink}"/><ellipse cx="114" cy="97" rx="4" ry="5" fill="${P.ink}"/>
      <circle cx="87.5" cy="95" r="1.3" fill="#fff"/><circle cx="115.5" cy="95" r="1.3" fill="#fff"/>
      <circle cx="80" cy="110" r="6" fill="#d08a7a" opacity=".35"/><circle cx="120" cy="110" r="6" fill="#d08a7a" opacity=".35"/>
      <path d="M94 118 Q100 121 106 118" fill="none" stroke="#7a4a40" stroke-width="2.5" stroke-linecap="round"/>
    </g>`;
  }

  function anya(o = {}) {
    return `<g class="anya" opacity="${o.opacity ?? 1}">
      <ellipse cx="100" cy="392" rx="50" ry="7" fill="#000" opacity=".3"/>
      <rect x="80" y="286" width="17" height="96" rx="7" fill="#c9c3b8"/><rect x="103" y="286" width="17" height="96" rx="7" fill="#c2bcb1"/>
      <rect x="74" y="374" width="26" height="12" rx="5" fill="#4b525b"/><rect x="100" y="374" width="26" height="12" rx="5" fill="#4b525b"/>
      <path d="M66 266 L134 266 L142 304 L58 304Z" fill="#4f5966"/>
      <g id="anya-armL"><rect x="44" y="156" width="22" height="104" rx="11" fill="#cfd4da" transform="rotate(5 55 160)"/><circle cx="50" cy="262" r="9.5" fill="${P.skinPale}"/></g>
      <rect x="58" y="146" width="84" height="128" rx="26" fill="#d7dbe0"/>
      <path d="M64 196 h72 M64 214 h72 M64 232 h72" stroke="#c3c8cf" stroke-width="3"/>
      <g id="anya-armR"><rect x="134" y="156" width="22" height="92" rx="11" fill="#cfd4da" transform="rotate(-24 145 160)"/>
        <circle cx="166" cy="242" r="9.5" fill="${P.skinPale}"/><rect x="156" y="216" width="34" height="26" rx="2" fill="${P.paper}" transform="rotate(10 172 228)"/>
        <path d="M162 224 h20 M161 230 h18 M160 236 h14" stroke="#555" stroke-width="1.6" transform="rotate(10 172 228)"/></g>
      <rect x="90" y="128" width="20" height="20" fill="#c6bdb2"/>
      <ellipse cx="100" cy="94" rx="37" ry="43" fill="${P.skinPale}"/>
      <path d="M60 110 Q54 50 100 46 Q146 50 140 110 L140 126 Q134 90 128 74 Q100 82 72 74 Q66 90 60 126Z" fill="#b9a88a"/>
      <path d="M66 104 v22 M74 110 v20 M126 110 v20 M134 104 v22" stroke="#a69476" stroke-width="3" stroke-linecap="round"/>
      <path d="M79 99 Q86 103 93 99 M107 99 Q114 103 121 99" fill="none" stroke="${P.ink}" stroke-width="2.6" stroke-linecap="round"/>
      <path d="M95 119 h10" stroke="#8a7a72" stroke-width="2.4" stroke-linecap="round"/>
      <path d="M128 70 q3 6 0 9 q-3 -3 0 -9Z" fill="#9fd0dd"/>
    </g>`;
  }

  // кот (viewBox 0 0 200 200, сидит, основание y≈190)
  function cat(o = {}) {
    const eyes = o.eyes ?? 1, lk = o.look ?? 0, ey = o.blink ? 1.5 : 9;
    return `<g class="cat">
      <path d="M150 182 Q196 170 184 128 Q178 112 168 120 Q178 140 150 160Z" fill="#0f1114"/>
      <path d="M58 190 Q50 110 80 92 L120 92 Q150 110 142 190Z" fill="#111317" stroke="#3a5866" stroke-width="3"/>
      <ellipse cx="100" cy="78" rx="42" ry="36" fill="#14161b" stroke="#3a5866" stroke-width="3"/>
      <path d="M62 62 L66 22 L92 50Z M138 62 L134 22 L108 50Z" fill="#14161b" stroke="#3a5866" stroke-width="3" stroke-linejoin="round"/>
      <path d="M70 52 L70 34 L84 50Z M130 52 L130 34 L116 50Z" fill="#2a2228"/>
      <path d="M70 108 l-3 10 M90 112 l-2 12 M118 110 l2 11" stroke="#22262c" stroke-width="3" stroke-linecap="round"/>
      <g opacity="${eyes}"><ellipse cx="84" cy="78" rx="10" ry="${ey}" fill="#e2c64b"/><ellipse cx="116" cy="78" rx="10" ry="${ey}" fill="#e2c64b"/>
      ${o.blink ? "" : `<ellipse cx="${84 + lk}" cy="78" rx="2.4" ry="8" fill="#0a0a0a"/><ellipse cx="${116 + lk}" cy="78" rx="2.4" ry="8" fill="#0a0a0a"/>`}</g>
      <path d="M95 92 l5 4 l5 -4Z" fill="#5c4048"/>
      <path d="M60 196 q8 -14 16 0 M124 196 q8 -14 16 0" fill="#111317"/>
    </g>`;
  }

  // сосед-силуэт (viewBox 0 0 200 400)
  function neighbor(v = 0) {
    const s = [1, 0.9, 1.06, 0.95][v % 4], w = [1, 1.15, 0.9, 1.05][v % 4];
    return `<g class="neighbor" transform="translate(100 392) scale(${w} ${s}) translate(-100 -392)">
      <path d="M58 392 L62 170 Q100 140 138 170 L142 392Z" fill="#0b1016" stroke="#2c4552" stroke-width="3"/>
      <ellipse cx="100" cy="112" rx="34" ry="40" fill="#0b1016" stroke="#2c4552" stroke-width="3"/>
      ${v % 4 === 1 ? '<path d="M64 108 Q100 40 136 108 Q100 84 64 108Z" fill="#0b1016"/>' : ''}
      <circle cx="88" cy="112" r="3.2" fill="#a9dbe3"/><circle cx="112" cy="112" r="3.2" fill="#a9dbe3"/>
    </g>`;
  }

  // ---------- РЕКВИЗИТ ----------
  function clock(t = '21:14') {
    return `<g><rect x="0" y="0" width="260" height="110" rx="14" fill="#14181c" stroke="#3a4148" stroke-width="6"/>
      <text x="130" y="80" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="72" fill="${P.red}">${t}</text></g>`;
  }
  function phone() {
    return `<g><rect x="0" y="0" width="150" height="290" rx="22" fill="#0e1114" stroke="#333a41" stroke-width="5"/>
      <rect x="10" y="22" width="130" height="246" rx="10" fill="#18232c"/>
      <text x="75" y="56" text-anchor="middle" font-family="Inter" font-weight="700" font-size="14" fill="#9fb2bf">ПОСЛЕДНИЙ</text><text x="75" y="74" text-anchor="middle" font-family="Inter" font-weight="700" font-size="14" fill="#9fb2bf">ПОЕЗД</text>
      <text x="75" y="125" text-anchor="middle" font-family="Inter" font-weight="800" font-size="44" fill="${P.lamp}">23:40</text>
      <rect x="22" y="150" width="106" height="8" rx="4" fill="#2c3a45"/><rect x="22" y="150" width="70" height="8" rx="4" fill="${P.red}"/>
      <text x="75" y="196" text-anchor="middle" font-family="Inter" font-size="14" fill="#7d8e9a">Вокзал · путь 3</text>
      <text x="75" y="240" text-anchor="middle" font-family="Inter" font-size="13" fill="${P.red}">сеть: нет</text></g>`;
  }
  function note(txt = ['НЕ СПУСКАЙТЕСЬ', 'В ПОДВАЛ']) {
    return `<g><path d="M0 4 L180 0 L184 120 L4 126Z" fill="${P.paper}"/><path d="M80 0 h24 v14 h-24Z" fill="#b9b39f" opacity=".8"/>
      ${txt.map((t, i) => `<text x="92" y="${58 + i * 34}" text-anchor="middle" font-family="DejaVu Serif" font-style="italic" font-weight="700" font-size="22" textLength="${Math.min(150, t.length * 11)}" lengthAdjust="spacingAndGlyphs" fill="#23252b" transform="rotate(-2 92 60)">${t}</text>`).join('')}</g>`;
  }
    function poster() {
    return `<g><rect x="0" y="0" width="220" height="300" fill="${P.paper}"/>
      <text x="110" y="46" text-anchor="middle" font-family="Inter" font-weight="900" font-size="38" fill="${P.red}">ПРОПАЛА</text>
      <rect x="40" y="62" width="140" height="150" fill="#9aa1a8"/>
      <clipPath id="phclip"><rect x="40" y="62" width="140" height="150"/></clipPath><g clip-path="url(#phclip)"><g transform="translate(30 70) scale(.8)" filter="url(#gray)">${anya().replace('class="anya"', 'class="anya-photo"')}</g></g>
      <text x="110" y="238" text-anchor="middle" font-family="Inter" font-weight="700" font-size="20" fill="#2b2d33">Аня, к. 42</text>
      <text x="110" y="266" text-anchor="middle" font-family="Inter" font-size="14" fill="#555">видели утром…</text></g>`;
  }
  function whistle() {
    return `<g><rect x="0" y="20" width="90" height="40" rx="20" fill="${P.brass}"/><rect x="70" y="10" width="44" height="26" rx="6" fill="#b08b38"/>
      <circle cx="34" cy="40" r="10" fill="#6d5520"/><path d="M0 40 Q-40 20 -50 -20" fill="none" stroke="#7a4a2a" stroke-width="3"/></g>`;
  }
  function pills() {
    return `<g><rect x="0" y="0" width="120" height="70" rx="8" fill="#b7c0c8"/>
      ${[0, 1, 2, 3, 4, 5].map(i => `<ellipse cx="${20 + (i % 3) * 40}" cy="${20 + Math.floor(i / 3) * 30}" rx="12" ry="9" fill="${i < 2 ? '#8b939a' : '#eef1f3'}"/>`).join('')}</g>`;
  }

  // ---------- ФОНЫ (1080×1920) ----------
  function rain(seed = 1, n = 140, op = .35) {
    const r = rng(seed); let s = '';
    for (let i = 0; i < n; i++) { const x = r() * 1180 - 50, y = r() * 1920, l = 40 + r() * 70; s += `M${x.toFixed(0)} ${y.toFixed(0)} l${(-l * .18).toFixed(0)} ${l.toFixed(0)} `; }
    return `<path class="rain" d="${s}" stroke="#7f9db0" stroke-width="2.2" opacity="${op}" stroke-linecap="round"/>`;
  }
  function car(color = '#3b4450', hazard = true) {
    return `<g><path d="M0 70 Q4 40 40 36 L80 6 Q96 0 150 0 Q196 2 214 34 Q250 38 256 70 L256 96 L0 96Z" fill="${color}"/>
      <path d="M90 14 L148 12 Q178 14 192 36 L72 36Z" fill="#1d2a33"/><path d="M134 13 v23" stroke="${color}" stroke-width="6"/>
      ${hazard ? `<rect x="244" y="54" width="12" height="10" rx="3" fill="#e0913a" class="hazard"/><rect x="0" y="54" width="10" height="10" rx="3" fill="#e0913a" class="hazard"/>` : ''}</g>`;
  }
  function water(y0, seed = 3, t = 0) {
    const r = rng(seed); let lines = '';
    for (let i = 0; i < 26; i++) { const y = y0 + 20 + i * ((1920 - y0) / 26), x = r() * 900, w = 60 + r() * 180; lines += `M${x.toFixed(0)} ${y.toFixed(0)} q${w / 2} -8 ${w} 0 `; }
    return `<defs><linearGradient id="wg${seed}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${P.water}"/><stop offset="1" stop-color="${P.waterDeep}"/></linearGradient></defs>
      <rect x="0" y="${y0}" width="1080" height="${1920 - y0}" fill="url(#wg${seed})"/>
      <path class="waves" transform="translate(${Math.sin(t * .9) * 30} 0)" d="${lines}" fill="none" stroke="${P.waterLine}" stroke-width="3" opacity=".55"/>`;
  }

  function bgFlood(o = {}) {
    const dx = (o.t || 0) * 6;
    const r = rng(7); let bld = '', win = '';
    const xs = [[0, 250, 520], [250, 230, 640], [480, 300, 480], [780, 300, 600]];
    xs.forEach(([x, w, h]) => { bld += `<rect x="${x}" y="${1180 - h}" width="${w}" height="${h}" fill="#111922"/>`;
      for (let yy = 1180 - h + 40; yy < 1140; yy += 70) for (let xx = x + 24; xx < x + w - 40; xx += 56)
        win += `<rect x="${xx}" y="${yy}" width="26" height="36" fill="${r() < .06 ? P.lamp : '#1d2832'}" opacity="${r() < .06 ? .8 : 1}"/>`; });
    return `<g class="bg-flood">
      <defs><linearGradient id="sky1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#070b11"/><stop offset="1" stop-color="#1c2a37"/></linearGradient></defs>
      <rect width="1080" height="1920" fill="url(#sky1)"/>${bld}${win}
      ${water(1130, 3, o.t)}
      <g transform="translate(${150 + dx * .6} ${1185 + Math.sin((o.t || 0) * 1.3) * 5}) rotate(-4) scale(.8)">${car('#2f3842', true)}</g>
      <g transform="translate(${dx} ${Math.sin((o.t || 0) * 1.1) * 8})"><g transform="translate(470 1250) rotate(3) scale(1.6)">${car('#4a3b3b', (o.t * 2 | 0) % 2 === 0)}</g>
      <g class="cat-on-car" transform="translate(628 1142) scale(.62)">${cat(o.cat || {})}</g></g>
      
      ${o.noRain ? '' : rain(11, 160)}
      <path fill-rule="evenodd" d="M0 0 H1080 V1920 H0Z M90 170 H990 V1480 H90Z" fill="#17120f"/>
      <rect x="528" y="170" width="24" height="1310" fill="#17120f"/><rect x="90" y="800" width="900" height="22" fill="#17120f"/>
      <rect x="60" y="1480" width="960" height="40" fill="#241b16"/>
      <rect x="0" y="1520" width="1080" height="400" fill="#10161c"/>
    </g>`;
  }

  function bgCorridor(o = {}) {
    const dx = o.vx || 0, VX0 = 400 + dx, VX1 = 680 + dx, VY0 = 660, VY1 = 1060, exit = o.end === 'exit';
    const lt = x => VY0 * x / VX0, lb = x => 1920 - (1920 - VY1) * x / VX0;
    const rt = x => VY0 * (1080 - x) / (1080 - VX1), rb = x => 1920 - (1920 - VY1) * (1080 - x) / (1080 - VX1);
    const wall = (side, u1, u2, label, gold) => {
      const X = u => side === 'L' ? u * VX0 : 1080 - u * (1080 - VX1), top = side === 'L' ? lt : rt, bot = side === 'L' ? lb : rb;
      const x1 = X(u1), x2 = X(u2), Y = (x, f) => { const a = top(x) + (bot(x) - top(x)) * .22; return a + (bot(x) - a) * f; };
      const quad = (f1, f2, fa, fb) => `${fa},${Y(fa === x1 ? x1 : x2, f1)} ${fb},${Y(fb === x1 ? x1 : x2, f1)} ${fb},${Y(fb === x1 ? x1 : x2, f2)} ${fa},${Y(fa === x1 ? x1 : x2, f2)}`;
      const mid = (x1 + x2) / 2, nx1 = x1 + (x2 - x1) * .22, nx2 = x1 + (x2 - x1) * .78;
      const Q = (xa, xb, f1, f2) => `${xa},${Y(xa, f1)} ${xb},${Y(xb, f1)} ${xb},${Y(xb, f2)} ${xa},${Y(xa, f2)}`;
      return `<polygon points="${Q(x1, x2, 0, 1)}" fill="${P.door}"/>
        <polygon points="${Q(x1 + (x2 - x1) * .08, x2 - (x2 - x1) * .08, .05, .93)}" fill="none" stroke="${P.door2}" stroke-width="4"/>
        ${o.strips ? `<polygon points="${Q(x1, x2, 1, 1.012)}" fill="#f3dc96" opacity=".75"/>` : ''}
        ${o.notes === false ? '' : `<polygon class="note" points="${Q(nx1, nx2, .3, .5)}" fill="${P.paper}"/><polygon points="${Q(nx1 + (nx2 - nx1) * .12, nx2 - (nx2 - nx1) * .12, .35, .37)}" fill="#8b8f96"/><polygon points="${Q(nx1 + (nx2 - nx1) * .12, nx2 - (nx2 - nx1) * .3, .41, .43)}" fill="#8b8f96"/>`}
        <text x="${mid}" y="${Y(mid, .12)}" font-family="Inter" font-weight="800" font-size="${Math.max(10, (x2 - x1) * .17)}" fill="${gold ? '#f0cf86' : '#c9b79a'}" text-anchor="middle">${label}</text>`;
    };
    let tiles = '';
    for (let i = 1; i < 9; i++) { const t = i / 9, y = VY1 + (1920 - VY1) * t * t, k = (y - VY1) / (1920 - VY1); tiles += `M${VX0 * (1 - k)} ${y} L${1080 - (1080 - VX1) * (1 - k)} ${y} `; }
    for (let i = -4; i <= 4; i++) tiles += `M${(VX0 + VX1) / 2 + i * 35} ${VY1} L${(VX0 + VX1) / 2 + i * 260} 1920 `;
    const endWall = exit
      ? `<rect x="${VX0}" y="${VY0}" width="${VX1 - VX0}" height="${VY1 - VY0}" fill="#1c2630"/><rect x="${VX0 + 70}" y="${VY0 + 90}" width="${VX1 - VX0 - 140}" height="${VY1 - VY0 - 90}" fill="#26323c" stroke="#10161c" stroke-width="6"/>
         <rect x="${(VX0 + VX1) / 2 - 55}" y="${VY0 + 28}" width="110" height="44" rx="6" fill="#0c3a24"/><text x="${(VX0 + VX1) / 2}" y="${VY0 + 62}" text-anchor="middle" font-family="Inter" font-weight="900" font-size="26" fill="#3cff8f">ВЫХОД</text>
         <rect x="${VX0 + 70}" y="${VY0 + 90}" width="${VX1 - VX0 - 140}" height="${VY1 - VY0 - 90}" fill="#3cff8f" opacity=".07"/>`
      : `<rect x="${VX0}" y="${VY0}" width="${VX1 - VX0}" height="${VY1 - VY0}" fill="${P.wallEnd}"/>
         <rect x="${VX0 + 70}" y="${VY0 + 70}" width="140" height="170" fill="#0c1a24"/><path d="M${VX0 + 140} ${VY0 + 70} v170 M${VX0 + 70} ${VY0 + 150} h140" stroke="${P.wallEnd}" stroke-width="8"/>
         <g transform="translate(${VX0 + 75} ${VY0 + 270}) scale(.5)">${clock()}</g>`;
    return `<g class="bg-corridor">
      <rect width="1080" height="1920" fill="${P.floor}"/>
      <polygon points="0,0 1080,0 ${VX1},${VY0} ${VX0},${VY0}" fill="#161c23"/>
      <polygon points="0,0 ${VX0},${VY0} ${VX0},${VY1} 0,1920" fill="${P.wall}"/>
      <polygon points="1080,0 ${VX1},${VY0} ${VX1},${VY1} 1080,1920" fill="${P.wall2}"/>
      <polygon points="0,1920 ${VX0},${VY1} ${VX1},${VY1} 1080,1920" fill="${P.floor}"/>
      <path d="${tiles}" stroke="#262a30" stroke-width="3" fill="none"/>
      ${endWall}
      ${wall('L', .06, .38, 41)}${wall('L', .5, .72, 43)}${wall('L', .8, .92, 45)}
      ${wall('R', .08, .4, 42, true)}${wall('R', .52, .74, 44)}${wall('R', .82, .94, 46)}
      <path class="crack" d="M120 420 l40 60 l-20 40 l50 70 l-10 50 l40 60" fill="none" stroke="#0a0d11" stroke-width="6" stroke-linejoin="bevel" opacity="${o.crack ?? 1}" stroke-dasharray="700" stroke-dashoffset="${700 * (1 - (o.crack ?? 1))}"/>
      <defs><radialGradient id="lampg"><stop offset="0" stop-color="${P.lamp}" stop-opacity=".45"/><stop offset="1" stop-color="${P.lamp}" stop-opacity="0"/></radialGradient></defs>
      <g class="lamp" opacity="${o.lamp ?? 1}"><circle cx="${(VX0 + VX1) / 2}" cy="470" r="420" fill="url(#lampg)"/><rect x="${(VX0 + VX1) / 2 - 70}" y="420" width="140" height="22" rx="8" fill="${P.lampSoft}"/></g>
    </g>`;
  }

  // дверь крупным планом: номер, записка/объявление целиком в кадре
  function bgDoorClose(o = {}) {
    const n = o.n || 41, sway = Math.sin((o.t || 0) * 2.1) * 1.2;
    let item = '';
    if (o.mode === 'poster') item = `<g transform="translate(540 930) rotate(${-2 + sway}) scale(2.55) translate(-110 -150)">${poster()}</g>`;
    else if (o.mode !== 'bare') item = `<g transform="translate(540 920) rotate(${(o.rot ?? -3) + sway}) scale(${o.s || 3.5}) translate(-92 -63)">${note(o.txt)}</g>`;
    return `<g class="bg-door">
      <rect width="1080" height="1920" fill="#1e2832"/>
      ${Array.from({ length: 6 }, (_, i) => `<rect x="${i * 190 - 20}" y="0" width="4" height="1920" fill="#1a222b"/>`).join('')}
      <defs><radialGradient id="dlg" cx=".5" cy=".4" r=".7"><stop offset="0" stop-color="${P.lamp}" stop-opacity=".30"/><stop offset="1" stop-color="${P.lamp}" stop-opacity="0"/></radialGradient></defs>
      <rect x="130" y="90" width="820" height="1470" fill="#17110e"/><rect x="160" y="120" width="760" height="1440" fill="${P.door}"/>
      <rect x="215" y="190" width="650" height="520" fill="none" stroke="${P.door2}" stroke-width="10"/><rect x="215" y="780" width="650" height="700" fill="none" stroke="${P.door2}" stroke-width="10"/>
      <rect x="400" y="132" width="280" height="110" rx="14" fill="#b08b38"/><rect x="408" y="140" width="264" height="94" rx="10" fill="none" stroke="#6d5520" stroke-width="4"/>
      <text x="540" y="218" text-anchor="middle" font-family="Inter" font-weight="900" font-size="88" fill="${n == 42 ? '#fff1c0' : '#3a2c0f'}">${n}</text>
      <circle cx="540" cy="320" r="24" fill="#0b0d10" stroke="#8a7a5a" stroke-width="6"/>
      <rect x="790" y="800" width="34" height="140" rx="12" fill="#8a7a5a"/><circle cx="807" cy="948" r="22" fill="#8a7a5a"/>
      <rect x="130" y="1550" width="820" height="40" fill="#0e0b09"/>
      <rect width="1080" height="1920" fill="url(#dlg)"/>${item}</g>`;
  }

  // комната Ильи (стрим-уголок), окно с потопом
  function bgRoom(o = {}) {
    const t = o.t || 0, r = rng(5); let bulbs = '', city = '';
    for (let i = 0; i < 16; i++) { const x = 40 + i * 66, y = 120 + Math.sin(i * .9) * 26 + (x - 540) * (x - 540) / 9000; bulbs += `<circle cx="${x}" cy="${y.toFixed(0)}" r="9" fill="#ffd9a0" opacity="${(.55 + .35 * Math.sin(t * 3 + i)).toFixed(2)}"/><circle cx="${x}" cy="${y.toFixed(0)}" r="26" fill="#ffd9a0" opacity=".12"/>`; }
    for (let i = 0; i < 7; i++) { const h = 120 + r() * 200; city += `<rect x="${100 + i * 52}" y="${700 - h}" width="46" height="${h}" fill="#0e1722"/>` + (r() < .8 ? `<rect x="${112 + i * 52}" y="${720 - h + r() * 90}" width="10" height="14" fill="${P.lamp}"/>` : ''); }
    const rainW = Array.from({ length: 26 }, () => `M${(100 + r() * 380).toFixed(0)} ${(300 + r() * 580).toFixed(0)} l-8 36`).join(' ');
    return `<g class="bg-room">
      <rect width="1080" height="1920" fill="#17202a"/><rect y="1260" width="1080" height="660" fill="#10161d"/>
      <path d="M0 0 H1080 M0 40 H1080" stroke="#1d2833" stroke-width="3"/>
      <path d="M20 90 Q540 260 1060 90" fill="none" stroke="#2b3744" stroke-width="3"/>${bulbs}
      <rect x="80" y="300" width="420" height="600" fill="#0b121a" stroke="#2b3744" stroke-width="14"/>
      <defs><linearGradient id="rwg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#101a26"/><stop offset="1" stop-color="#1c3646"/></linearGradient></defs>
      <rect x="94" y="314" width="392" height="572" fill="url(#rwg)"/>${city}<rect x="94" y="700" width="392" height="186" fill="${P.water}"/><path d="M110 740 q40 -8 80 0 M260 790 q50 -8 100 0 M130 840 q60 -8 120 0" stroke="${P.waterLine}" stroke-width="3" fill="none" opacity=".7"/>
      <path d="${rainW}" stroke="#7f9db0" stroke-width="2" opacity=".35"/><rect x="283" y="314" width="14" height="572" fill="#2b3744"/><rect x="94" y="560" width="392" height="12" fill="#2b3744"/>
      <circle cx="800" cy="520" r="150" fill="#f3dc96" opacity=".12" filter="url(#rb)"/><circle cx="800" cy="520" r="110" fill="none" stroke="#f3f0ea" stroke-width="22" opacity=".9"/><circle cx="800" cy="520" r="110" fill="none" stroke="#f3dc96" stroke-width="40" opacity=".25"/>
      <rect x="570" y="660" width="460" height="300" rx="14" fill="#0c1016" stroke="#2c3642" stroke-width="12"/><rect x="584" y="674" width="432" height="272" fill="#14202c"/>
      <circle cx="610" cy="702" r="9" fill="${P.red}" opacity="${(t * 2 | 0) % 2 ? 1 : .35}"/><text x="630" y="710" font-family="Inter" font-weight="800" font-size="22" fill="${P.red}">LIVE</text>
      ${Array.from({ length: 6 }, (_, i) => `<rect x="610" y="${740 + i * 32}" width="${120 + ((i * 53) % 160)}" height="14" rx="7" fill="#2b4256"/>`).join('')}<rect x="840" y="740" width="150" height="180" rx="8" fill="#1d3345"/>
      <rect x="780" y="960" width="40" height="60" fill="#1a2028"/><rect x="720" y="1010" width="160" height="14" rx="6" fill="#1a2028"/>
      <rect x="40" y="1220" width="1000" height="40" rx="8" fill="#2a2018"/><rect x="80" y="1260" width="26" height="420" fill="#1a1510"/><rect x="974" y="1260" width="26" height="420" fill="#1a1510"/>
      <rect x="560" y="1180" width="360" height="30" rx="8" fill="#1f2630"/><rect x="170" y="1160" width="64" height="62" rx="10" fill="#3a2f28"/><path d="M234 1176 q30 0 0 30" stroke="#3a2f28" stroke-width="8" fill="none"/>
      <rect x="0" y="1280" width="1080" height="640" fill="#000" opacity=".25"/>
      <defs><filter id="rb"><feGaussianBlur stdDeviation="30"/></filter></defs></g>`;
  }

  function bgBasement(o = {}) {
    let stairs = '';
    for (let i = 0; i < 8; i++) stairs += `<rect x="${0}" y="${780 + i * 90}" width="${300 - i * 22}" height="90" fill="${i % 2 ? '#22272d' : '#262b31'}"/><rect x="0" y="${780 + i * 90}" width="${300 - i * 22}" height="10" fill="#30363d"/>`;
    let rivets = '';
    for (let y = 740; y < 1480; y += 80) rivets += `<circle cx="370" cy="${y}" r="7" fill="#596066"/><circle cx="710" cy="${y}" r="7" fill="#596066"/>`;
    let keys = '';
    for (let i = 0; i < 12; i++) keys += `<rect x="${806 + (i % 3) * 30}" y="${1000 + Math.floor(i / 3) * 30}" width="22" height="22" rx="4" fill="#3a434b"/>`;
    return `<g class="bg-basement">
      <rect width="1080" height="1920" fill="#16191d"/>
      <rect x="0" y="0" width="1080" height="160" fill="#101316"/>
      <path d="M0 120 H1080 M0 170 H1080" stroke="#2c3338" stroke-width="26"/><path d="M0 170 H1080" stroke="#20262b" stroke-width="10"/>
      <rect x="300" y="620" width="480" height="900" fill="#0f1215"/>
      <rect x="340" y="680" width="400" height="840" fill="#3d4448"/><rect x="340" y="680" width="400" height="18" fill="#4f575c"/>
      ${rivets}
      <rect x="790" y="960" width="120" height="170" rx="10" fill="#1d2328"/>${keys}<circle cx="850" cy="980" r="6" fill="${P.red}" class="led"/>
      <rect x="640" y="1080" width="60" height="22" rx="8" fill="#6a7277"/>
      ${o.digits === false ? '' : `<g class="digits" transform="rotate(-3 540 420)"><text x="540" y="470" text-anchor="middle" font-family="DejaVu Serif" font-size="190" letter-spacing="40" fill="none" stroke="#b7c0c6" stroke-width="6" opacity=".8">4 1 9 7</text>
        <path d="M250 520 L830 500" stroke="#b7c0c6" stroke-width="4" opacity=".5"/><path d="M880 330 v80 M900 330 v80 M920 330 v80 M940 330 v80 M870 390 L960 350" stroke="#8b949a" stroke-width="5" opacity=".6"/></g>`}
      ${stairs}
      ${water(1520, 5, o.t)}
      <defs><radialGradient id="flash"><stop offset="0" stop-color="${P.lampSoft}" stop-opacity=".22"/><stop offset="1" stop-color="${P.lampSoft}" stop-opacity="0"/></radialGradient></defs>
      <circle class="flashlight" cx="560" cy="1060" r="520" fill="url(#flash)"/>
    </g>`;
  }

  function bgBoat() {
    return `<g class="bg-boat">
      <rect width="1080" height="1920" fill="#06090c"/>
      <defs><radialGradient id="flash2" cx=".5" cy=".62" r=".55"><stop offset="0" stop-color="${P.lampSoft}" stop-opacity=".28"/><stop offset="1" stop-color="${P.lampSoft}" stop-opacity="0"/></radialGradient></defs>
      <rect width="1080" height="1920" fill="url(#flash2)"/>
      <path d="M0 1080 Q540 1040 1080 1080 V1920 H0Z" fill="#0b1e26"/>
      <path class="waves" d="M60 1180 q90 -14 180 0 M360 1240 q120 -16 240 0 M700 1170 q90 -12 180 0 M120 1420 q150 -18 300 0 M600 1460 q140 -16 280 0 M260 1650 q160 -20 320 0" stroke="${P.waterLine}" stroke-width="4" fill="none" opacity=".6"/>
      <g class="boat" transform="translate(300 1180)">
        <path d="M0 40 Q240 70 480 40 L430 130 Q240 160 50 130Z" fill="#4a3426"/>
        <path d="M0 40 Q240 70 480 40 L470 58 Q240 88 10 58Z" fill="#6a4a34"/>
        <path d="M150 62 v70 M330 62 v70" stroke="#3a281d" stroke-width="10"/>
        <path d="M480 44 q60 -40 120 -10" fill="none" stroke="#8a7a5a" stroke-width="5"/>
        <path d="M50 150 Q240 180 430 150" stroke="#000" stroke-width="20" opacity=".35"/>
      </g>
      <path fill-rule="evenodd" d="M0 0 H1080 V1920 H0Z M180 300 H900 V1920 H180Z" fill="#3d4448"/>
      <path d="M180 300 H900 V1920 M180 300 V1920" fill="none" stroke="#1d2226" stroke-width="16"/>
    </g>`;
  }

  function bgCity(o = {}) {
    const r = rng(21); let sky = '', win = '';
    let x = 0;
    while (x < 1080) { const w = 70 + r() * 120, h = 260 + r() * 520; sky += `<rect x="${x.toFixed(0)}" y="${(1100 - h).toFixed(0)}" width="${w.toFixed(0)}" height="${h.toFixed(0)}" fill="#0e1520"/>`;
      for (let yy = 1100 - h + 24; yy < 1080; yy += 34) for (let xx = x + 12; xx < x + w - 16; xx += 24) if (r() < .55) { const on = xx < (o.lightX ?? 2000) - r() * 80; const c = r() < .7 ? P.lamp : P.lampSoft, op = .6 + r() * .4; win += `<rect class="cw" x="${xx.toFixed(0)}" y="${yy.toFixed(0)}" width="12" height="16" fill="${on ? c : '#1a2330'}" opacity="${on ? op : 1}"/>`; }
      x += w + 6; }
    return `<g class="bg-city">
      <defs><linearGradient id="sky2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#05080d"/><stop offset=".7" stop-color="#16202e"/><stop offset="1" stop-color="#2a2a30"/></linearGradient></defs>
      <rect width="1080" height="1920" fill="url(#sky2)"/>
      <path d="M0 260 q200 -60 420 -10 q240 50 660 -20 V0 H0Z" fill="#0b1119" opacity=".9"/>
      ${sky}${win}
      ${water(1100, 9, o.t)}
      <g opacity=".25" transform="translate(0 2200) scale(1 -1)">${win}</g>
      <g class="our-house" transform="rotate(-7 640 1700)">
        <rect x="420" y="760" width="440" height="1200" fill="#06090d"/>
        ${Array.from({ length: 14 }, (_, i) => Array.from({ length: 5 }, (_, j) => `<rect x="${450 + j * 80}" y="${800 + i * 80}" width="40" height="50" fill="#0f141a"/>`).join('')).join('')}
        <rect x="420" y="740" width="440" height="24" fill="#0a0e13"/>
      </g>
      ${water(1640, 10, o.t)}
      ${o.noRain ? '' : rain(31, 120, .25)}
    </g>`;
  }

  g.POTOP = { P, rng, ilya, vera, anya, cat, neighbor, clock, phone, note, poster, whistle, pills, rain, car, water, bgFlood, bgCorridor, bgDoorClose, bgRoom, bgBasement, bgBoat, bgCity };
})(typeof window !== 'undefined' ? window : globalThis);
