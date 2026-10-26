"""Real local native-video → JSON → Ollama text smoke using synthetic footage."""
import json
import subprocess
import tempfile
import time
from pathlib import Path
import imageio_ffmpeg
from avocadoeyes.two_stage import TwoStage
from avocadoeyes.native_video import count_video_frames, video_messages, video_processor_kwargs, verify_video_frames


def main():
    import torch
    import transformers
    import av
    print(json.dumps({'torch': torch.__version__, 'transformers': transformers.__version__,
                      'av': av.__version__, 'cuda': torch.cuda.is_available(),
                      'gpu': torch.cuda.get_device_name(0) if torch.cuda.is_available() else None}), flush=True)
    run = TwoStage()
    config = run.config
    config['video']['prompt'] = 'Describe the visible video content briefly. Are any people visible? Do not invent people.'
    config['video']['schema'] = {'type': 'object', 'properties': {'description': {'type': 'string'}, 'people_visible': {'type': 'boolean'}}, 'required': ['description', 'people_visible'], 'additionalProperties': False}
    config['video']['settings']['max_new_tokens'] = 256
    config['reason']['prompt'] = 'In one sentence, explain whether these observations provide any evidence about people. Do not invent details.'
    config['reason']['settings']['num_predict'] = 2048
    run.configure(config)
    processor = transformers.AutoProcessor.from_pretrained(config['video']['model'], local_files_only=True, trust_remote_code=False)
    with tempfile.TemporaryDirectory() as directory:
        clip = Path(directory) / 'synthetic.mp4'
        for count in (20, 21):
            subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-hide_banner', '-loglevel', 'error', '-f', 'lavfi', '-i', 'testsrc=size=320x240:rate=10', '-frames:v', str(count), '-pix_fmt', 'yuv420p', str(clip)], check=True, capture_output=True)
            actual = count_video_frames(clip, config['video']['settings']['max_frames'])
            assert actual == count
            try:
                count_video_frames(clip, count - 1)
            except ValueError as exc:
                assert 'frame sampling is disabled' in str(exc)
            else:
                raise AssertionError('Oversized video was not rejected')
            inputs = processor.apply_chat_template(video_messages(clip, 'Describe this video'), tokenize=True,
                add_generation_prompt=True, return_dict=True, return_tensors='pt',
                processor_kwargs=video_processor_kwargs(count, config['video']['settings']['max_pixels']))
            indices = [int(index) for index in inputs['video_metadata'][0].frames_indices]
            grid = inputs['video_grid_thw'].tolist()
            verify_video_frames(inputs, count, processor.video_processor.temporal_patch_size)
            print(json.dumps({'all_frame_processor_check': 'passed', 'decoded_frames': count,
                              'frame_indices': indices, 'temporal_grid': grid}), flush=True)
        run.upload(clip.read_bytes(), 'synthetic.mp4')
    for stage in ('video', 'reason'):
        start = time.monotonic()
        passed = run.execute(stage)
        result = run.results[stage]
        print(json.dumps({'stage': stage, 'passed': passed, 'seconds': round(time.monotonic() - start, 3),
                          'status': result['status'], 'output': result.get('json', result.get('output')),
                          'error': result.get('error')}), flush=True)
        if not passed:
            raise SystemExit(1)
    assert run.results['video']['json']['people_visible'] is False
    print('PASS native local video and text inference; synthetic scene only, not real-room quality.', flush=True)


if __name__ == '__main__':
    main()
