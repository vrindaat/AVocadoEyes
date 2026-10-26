"""Native Qwen video-file inference; exclusively preinstalled local weights."""
import gc
import os
import tempfile
from pathlib import Path


def video_messages(path, prompt):
    return [{"role": "user", "content": [
        {"type": "video", "video": str(path)},
        {"type": "text", "text": prompt},
    ]}]


def count_video_frames(path, max_frames):
    """Count actual decoded frames, refusing oversized clips without truncation."""
    import av
    with av.open(str(path)) as container:
        if not container.streams.video:
            raise ValueError("The uploaded file has no video stream")
        stream = container.streams.video[0]
        duration = (float(stream.duration * stream.time_base) if stream.duration is not None
                    else container.duration / av.time_base if container.duration is not None else None)
        if duration is None or not 0 < duration <= 60:
            raise ValueError("Use a video with a known duration of at most 60 seconds")
        count = 0
        for _ in container.decode(video=0):
            count += 1
            if count > max_frames:
                raise ValueError(f"Video exceeds max_frames={max_frames}. Use a shorter clip or raise max_frames; frame sampling is disabled.")
    if count < 2:
        raise ValueError("Use a video with at least two decoded frames")
    return count


def video_processor_kwargs(frame_count, max_pixels):
    return {"return_metadata": True, "videos_kwargs": {
        "num_frames": None, "fps": None, "do_sample_frames": False,
        "size": {"shortest_edge": 4 * 32 * 32,
                 "longest_edge": frame_count * max_pixels},
        "cap_pixels_per_frame": True}}


def verify_video_frames(inputs, frame_count, temporal_patch_size):
    metadata = inputs.pop("video_metadata", None)
    if not metadata or len(metadata) != 1:
        raise ValueError("Native processor did not return frame coverage metadata")
    indices = metadata[0].frames_indices
    if indices is None or list(indices) != list(range(frame_count)):
        raise ValueError("Native processor did not preserve every decoded frame; refusing sampled video")
    expected = (frame_count + temporal_patch_size - 1) // temporal_patch_size
    if "pixel_values_videos" not in inputs or int(inputs["video_grid_thw"][0][0]) != expected:
        raise ValueError("Native processor did not produce the complete video temporal grid")


class NativeVideo:
    def __init__(self):
        self.model = self.processor = None
        self.loaded_path = None

    def complete(self, video, model_path, prompt, settings):
        path = Path(model_path).expanduser().resolve()
        if not path.is_dir() or not (path / "config.json").is_file():
            raise ValueError("Native video weights are missing. Prepare a local Qwen3-VL Transformers model directory and select its path; Ollama tags cannot be used here.")
        os.environ["HF_HUB_OFFLINE"] = "1"
        os.environ["TRANSFORMERS_OFFLINE"] = "1"
        try:
            import torch
            import av
            from transformers import AutoProcessor, AutoModelForImageTextToText
        except ImportError as exc:
            raise ValueError("Native video runtime is missing. Install requirements-video.txt with a CUDA-enabled PyTorch build before running.") from exc
        if not torch.cuda.is_available():
            raise ValueError("Native video requires a working local CUDA GPU; no CPU or cloud fallback.")
        # The processor receives a video file, not application-extracted images.
        # Its native processor decodes all frames with temporal sampling disabled.
        with tempfile.TemporaryDirectory(prefix="avocado-native-video-") as directory:
            clip = Path(directory) / "input.mp4"
            clip.write_bytes(video)
            frame_count = count_video_frames(clip, settings["max_frames"])
            if self.loaded_path != path:
                self.model = self.processor = None
                self.loaded_path = None
                gc.collect()
                torch.cuda.empty_cache()
                processor = AutoProcessor.from_pretrained(path, local_files_only=True, trust_remote_code=False)
                model = AutoModelForImageTextToText.from_pretrained(
                    path, local_files_only=True, trust_remote_code=False,
                    dtype=torch.bfloat16, attn_implementation="sdpa").to("cuda")
                model.eval()
                self.processor, self.model, self.loaded_path = processor, model, path
            inputs = self.processor.apply_chat_template(
                video_messages(clip, prompt), tokenize=True, add_generation_prompt=True,
                return_dict=True, return_tensors="pt",
                processor_kwargs=video_processor_kwargs(frame_count, settings["max_pixels"]),
            )
            verify_video_frames(inputs, frame_count, self.processor.video_processor.temporal_patch_size)
            if inputs.input_ids.shape[1] + settings["max_new_tokens"] > self.model.config.text_config.max_position_embeddings:
                raise ValueError("All-frame video exceeds the model context. Use a shorter clip or lower max_pixels; frame sampling is disabled.")
            inputs = inputs.to(self.model.device)
            try:
                with torch.inference_mode():
                    generated = self.model.generate(
                        **inputs, max_new_tokens=settings["max_new_tokens"], do_sample=False)
                trimmed = generated[:, inputs.input_ids.shape[1]:]
                return self.processor.batch_decode(trimmed, skip_special_tokens=True,
                                                   clean_up_tokenization_spaces=False)[0]
            finally:
                del inputs
