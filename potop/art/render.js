// Рендер кадров animate.html → сегменты MP4 (параллельно), затем склейка с голосом.
// node render.js <words.json> <outdir> [fps] [workers]
const { chromium } = require('playwright'); const fs = require('fs'); const { spawn, execFileSync } = require('child_process'); const path = require('path');
const [, , words, out, fpsA, wA] = process.argv; const fps = +fpsA || 30, W = +wA || 4;
fs.mkdirSync(out, { recursive: true });
(async () => {
  const b = await chromium.launch(); const raw = JSON.parse(fs.readFileSync(words));
  const p0 = await b.newPage(); await p0.goto('file://' + path.resolve(__dirname, process.env.ANIM || 'animate.html')); const dur = await p0.evaluate(w => { setup(w); return DURATION; }, raw); await p0.close();
  const N = Math.round(dur * fps), per = Math.ceil(N / W); const t0 = Date.now();
  await Promise.all([...Array(W)].map(async (_, k) => {
    const p = await b.newPage({ viewport: { width: 1080, height: 1920 } }); p.on('pageerror', e => console.log('ERR', e.message));
    await p.goto('file://' + path.resolve(__dirname, process.env.ANIM || 'animate.html')); await p.evaluate(w => setup(w), raw);
    const ff = spawn('ffmpeg', ['-loglevel', 'error', '-y', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', `${out}/seg${k}.mp4`]);
    for (let i = k * per; i < Math.min(N, (k + 1) * per); i++) {
      await p.evaluate(t => render(t), i / fps);
      const buf = await p.screenshot({ type: 'jpeg', quality: 93 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      if (k === 0 && i % 150 === 0) console.log(`kadr ${i}/${per} ${((Date.now() - t0) / 1000).toFixed(0)}s`);
    }
    ff.stdin.end(); await new Promise(r => ff.on('close', r));
  }));
  await b.close();
  fs.writeFileSync(`${out}/list.txt`, [...Array(W)].map((_, k) => `file 'seg${k}.mp4'`).join('\n'));
  execFileSync('ffmpeg', ['-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', `${out}/list.txt`, '-c', 'copy', `${out}/video_only.mp4`]);
  console.log('done', N, 'frames', ((Date.now() - t0) / 1000).toFixed(0) + 's');
})();
