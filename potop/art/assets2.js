// ПОТОП s02 — дополнительные SVG-ассеты (расширяют POTOP из assets.js). Кадр 1080×1920.
(function (g) {
  const A = g.POTOP, P = A.P;
  // затопленный подвал: потолок с трубами, стены, лестница слева, лампа, вода на уровне wy
  function bgCellar(o = {}) {
    const wy = o.wy ?? 1350, t = o.t ?? 0, lamp = o.lamp ?? 1, calm = !!o.calm;
    let stairs = '';
    for (let i = 0; i < 7; i++) stairs += `<rect x="0" y="${560 + i * 110}" width="${330 - i * 36}" height="110" fill="${i % 2 ? '#1c2127' : '#20262c'}"/><rect x="0" y="${560 + i * 110}" width="${330 - i * 36}" height="10" fill="#2c333a"/>`;
    let bricks = '';
    for (let y = 300; y < 1500; y += 70) bricks += `M0 ${y} H1080 `;
    for (let y = 300, r = 0; y < 1500; y += 70, r++) for (let x = (r % 2) * 60; x < 1080; x += 120) bricks += `M${x} ${y} v70 `;
    let wl = '';
    if (calm) wl = `<rect x="0" y="${wy}" width="1080" height="${1920 - wy}" fill="#0b1c24"/><path d="M0 ${wy} H1080" stroke="#4d8696" stroke-width="3"/>
      <ellipse cx="540" cy="${wy + 140}" rx="300" ry="40" fill="${P.lampSoft}" opacity=".12"/><path d="M420 ${wy + 20} v300 M540 ${wy + 20} v420 M660 ${wy + 20} v260" stroke="${P.lampSoft}" stroke-width="3" opacity=".14"/>`;
    else wl = A.water(wy, 7, t);
    return `<g class="bg-cellar">
      <rect width="1080" height="1920" fill="#101418"/>
      <path d="${bricks}" stroke="#181d22" stroke-width="3" fill="none"/>
      <rect width="1080" height="240" fill="#0a0d10"/>
      <path d="M0 90 H1080 M0 160 H1080" stroke="#2a3238" stroke-width="30"/><path d="M0 160 H1080" stroke="#1d2328" stroke-width="10"/>
      <path d="M260 0 v100 M760 0 v90" stroke="#20262b" stroke-width="10"/>
      <rect x="470" y="240" width="140" height="22" fill="#202429"/><path d="M540 180 v70" stroke="#202429" stroke-width="5"/>
      <defs><radialGradient id="cl"><stop offset="0" stop-color="${P.lampSoft}" stop-opacity="${.5 * lamp}"/><stop offset="1" stop-color="${P.lampSoft}" stop-opacity="0"/></radialGradient></defs>
      <circle cx="540" cy="300" r="760" fill="url(#cl)"/><circle cx="540" cy="268" r="26" fill="${P.lampSoft}" opacity="${lamp}"/>
      ${stairs}
      <rect x="0" y="540" width="330" height="14" fill="#0a0d10"/>
      ${wl}
    </g>`;
  }
  // десять силуэтов; ключ-кадр: стоят по воде (низ силуэта на wy+offset)
  function crowd(wy = 1380, o = {}) {
    const xs = [60, 190, 300, 420, 530, 640, 750, 860, 960, 1040], ds = [0, 6, 2, 8, 4, 10, 3, 7, 1, 5];
    const sc = i => [.95, .85, 1.0, .9, .95, .88, 1.0, .92, .86, .98][i];
    return xs.map((x, i) => {
      const k = sc(i) * .78, jit = o.push ? Math.sin((o.t || 0) * 5 + i * 1.7) * 14 : 0;
      return `<g transform="translate(${x + jit} ${wy + 20 - 392 * k}) scale(${k})">${A.neighbor(i)}</g>`;
    }).join('');
  }
  // лодка с одеялом: head 0..1 — как высоко Аня показалась, lump — шевеление
  function boatBlanket(o = {}) {
    const lump = o.lump ?? 0, head = o.head ?? 0;
    return `<g class="boat2">
      <path d="M0 90 Q300 130 600 90 L540 200 Q300 236 60 200Z" fill="#4a3426"/>
      <path d="M0 90 Q300 130 600 90 L588 112 Q300 152 12 112Z" fill="#6a4a34"/>
      <path d="M230 120 v80 M410 120 v80" stroke="#3a281d" stroke-width="12"/>
      ${head > 0 ? `<g transform="translate(300 ${60 - head * 150}) scale(.9)"><g transform="translate(-100 -40)">
        <clipPath id="hc"><rect x="0" y="0" width="200" height="${48 + head * 140}"/></clipPath><g clip-path="url(#hc)">${A.anya({ opacity: 1 })}</g></g></g>` : ''}
      <path d="M130 100 Q200 ${30 - lump * 24} 300 ${22 - lump * 40} Q400 ${30 - lump * 24} 470 100 Q300 134 130 100Z" fill="#5b6b55"/>
      <path d="M200 90 Q250 ${60 - lump * 20} 300 ${56 - lump * 30} M300 56 Q350 ${60 - lump * 20} 400 90" stroke="#46543f" stroke-width="5" fill="none"/>
    </g>`;
  }
  // кольцо волны от свистка
  function ring(cx, cy, r, op = 1) {
    return `<g fill="none" stroke="${P.cyan}" opacity="${op}"><ellipse cx="${cx}" cy="${cy}" rx="${r}" ry="${r * .28}" stroke-width="5"/><ellipse cx="${cx}" cy="${cy}" rx="${r * .72}" ry="${r * .2}" stroke-width="3" opacity=".6"/></g>`;
  }
  // подвал с видом на лодку: лодка в воде между людьми и бетонной аркой
  function bgCellarBoat(o = {}) {
    const wy = o.wy ?? 1180;
    return `<g>${bgCellar({ wy, t: o.t, calm: o.calm, lamp: o.lamp })}
      <g transform="translate(${o.bx ?? 240} ${wy - 150 + (o.bob ?? 0)})">${boatBlanket(o)}</g></g>`;
  }
  Object.assign(A, { bgCellar, crowd, boatBlanket, ring, bgCellarBoat });
})(window);
