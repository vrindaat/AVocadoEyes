"""Bounded decoding. No video/frame files survive this function."""
import base64
import re
import subprocess
import tempfile
from pathlib import Path

import imageio_ffmpeg


def sample(video, settings):
    count = int(settings.get("count", 8))
    seconds = float(settings.get("seconds", 12))
    if not 1 <= count <= 16 or not 0.1 <= seconds <= 60:
        raise ValueError("Use 1–16 frames and 0.1–60 seconds")
    if not video or len(video) > 64 * 1024 * 1024:
        raise ValueError("Upload a nonempty clip up to 64 MiB")
    with tempfile.TemporaryDirectory(prefix="avocado-decode-") as directory:
        source = Path(directory) / "clip"
        source.write_bytes(video)
        # showinfo records actual source PTS, rather than invented sample timestamps.
        command = [imageio_ffmpeg.get_ffmpeg_exe(), "-hide_banner", "-nostdin",
                   "-protocol_whitelist", "file,pipe", "-format_whitelist", "mov,matroska,webm,avi,mpegts,mpeg,ogg",
                   "-i", str(source), "-an", "-sn",
                   "-t", str(seconds), "-vf",
                   f"setpts=PTS-STARTPTS,select=isnan(prev_selected_t)+gte(t-prev_selected_t\\,{seconds/count}),scale=960:-2,showinfo",
                   "-vsync", "vfr", "-frames:v", str(count), "-q:v", "4", str(Path(directory) / "%03d.jpg")]
        result = subprocess.run(command, capture_output=True, timeout=45)
        if result.returncode:
            raise ValueError("Video decode failed; choose a supported video clip")
        timestamps = re.findall(r"\bn:\s*\d+\s+pts:.*?pts_time:([\d.eE+\-]+)", result.stderr.decode(errors="replace"))
        paths = sorted(Path(directory).glob("*.jpg"))
        if not paths or len(timestamps) < len(paths):
            raise ValueError("No timestamped frames decoded")
        return {"frames": [{"id": f"f{i:03d}", "timestamp_s": float(timestamps[i]),
                            "image": "data:image/jpeg;base64," + base64.b64encode(path.read_bytes()).decode()}
                           for i, path in enumerate(paths)],
                "window_s": seconds, "note": "Sparse samples; unsampled behavior remains unknown."}
