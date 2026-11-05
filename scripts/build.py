#!/usr/bin/env python3
"""Build versioned assets from an MP4 without changing its frame sequence."""
import hashlib, pathlib, subprocess, sys, tempfile
root = pathlib.Path(__file__).resolve().parents[1]
source = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv)>1 else next(root.glob('*.mp4'))
assets = root / 'assets'
assets.mkdir(exist_ok=True)
with tempfile.TemporaryDirectory() as tmp:
    video = pathlib.Path(tmp)/'factory.mp4'
    poster = pathlib.Path(tmp)/'poster.jpg'
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(source),'-map','0:v:0','-an','-vf','scale=1280:720:force_original_aspect_ratio=decrease:force_divisible_by=2','-c:v','libx264','-preset','slow','-crf','21','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],check=True)
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(video),'-frames:v','1','-q:v','2',str(poster)],check=True)
    def publish(path, prefix):
        data=path.read_bytes()
        name=f'{prefix}.{hashlib.sha256(data).hexdigest()[:16]}{path.suffix}'
        (assets/name).write_bytes(data)
        return 'assets/'+name
    video_path=publish(video,'factory')
    poster_path=publish(poster,'poster')
html='''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Father Frost helps Santa</title>
  <style>
    html, body { width: 100%; height: 100%; margin: 0; overflow: hidden; background: transparent; }
    body { display: grid; place-items: center; }
    video { display: block; width: min(100vw, 177.777778vh); height: auto; aspect-ratio: 16 / 9; max-height: 100vh; object-fit: contain; border: 0; pointer-events: none; }
  </style>
</head>
<body>
  <video autoplay muted loop playsinline preload="auto" disablepictureinpicture disableremoteplayback
    width="1280" height="720" poster="POSTER" aria-label="Christmas toy factory">
    <source src="VIDEO" type="video/mp4">
  </video>
  <script>
    const video = document.querySelector('video');
    video.defaultMuted = true;
    video.muted = true;
    const play = () => { video.muted = true; video.play().catch(() => {}); };
    video.addEventListener('volumechange', () => { if (!video.muted) video.muted = true; });
    document.addEventListener('visibilitychange', () => { if (!document.hidden) play(); });
    window.addEventListener('pageshow', play);
    play();
  </script>
</body>
</html>
'''.replace('POSTER',poster_path).replace('VIDEO',video_path)
(root/'index.html').write_text(html)
print(video_path,poster_path,sep='\n')
