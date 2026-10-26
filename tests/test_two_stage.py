import copy
import json
import unittest
from types import SimpleNamespace

from avocadoeyes.native_video import NativeVideo, video_messages, verify_video_frames
from avocadoeyes.two_stage import TwoStage

class VideoFake:
    def __init__(self):
        self.calls = []
        self.output = '{"people": [], "unknowns": ["No people visible"]}'

    def complete(self, video, model, prompt, settings):
        self.calls.append((video, model, prompt, settings))
        return self.output


class TextFake:
    def __init__(self):
        self.calls = []

    def complete(self, model, prompt, inputs, settings, frames=None):
        self.calls.append(copy.deepcopy((model, prompt, inputs, settings, frames)))
        return {"raw": json.dumps({"message": {"content": "There are no visible people to analyze.", "thinking": "Consider evidence limits."}})}


class TwoStageTests(unittest.TestCase):
    def setUp(self):
        self.video, self.text = VideoFake(), TextFake()
        self.run = TwoStage(self.text, self.video)
        self.run.upload(b'video-file-bytes', 'test.mp4')

    def test_exact_two_calls_and_json_text_handoff(self):
        self.assertTrue(self.run.execute(mode='all'))
        self.assertEqual(self.video.calls[0][0], b'video-file-bytes')
        self.assertEqual(self.text.calls[0][2], json.loads(self.video.output))
        self.assertIsNone(self.text.calls[0][4])
        self.assertIsNone(self.text.calls[0][3]['format'])
        self.assertEqual(len(self.video.calls), 1)
        self.assertEqual(len(self.text.calls), 1)
        self.assertIn('no visible people', self.run.results['reason']['output'])

    def test_reason_prompt_edit_reuses_json_and_video_edit_blocks_reason(self):
        self.assertTrue(self.run.execute(mode='all'))
        config = copy.deepcopy(self.run.config)
        config['reason']['prompt'] = 'New instruction'
        self.run.configure(config)
        self.assertEqual(self.run.results['video']['status'], 'current')
        self.assertEqual(self.run.results['reason']['status'], 'stale')
        self.assertTrue(self.run.execute('reason'))
        self.assertEqual(len(self.video.calls), 1)
        self.assertEqual(self.text.calls[-1][1], 'New instruction')
        config['video']['prompt'] = 'New video instruction'
        self.run.configure(config)
        self.assertFalse(self.run.execute('reason'))
        self.assertEqual(len(self.text.calls), 2)

    def test_custom_schema_and_invalid_output_visible_not_forwarded(self):
        config = copy.deepcopy(self.run.config)
        config['video']['schema'] = {'type': 'object', 'properties': {'count': {'type': 'integer'}}, 'required': ['count']}
        self.run.configure(config)
        self.assertFalse(self.run.execute(mode='all'))
        self.assertEqual(self.run.results['video']['output'], self.video.output)
        self.assertFalse(self.text.calls)
        self.video.output = '{"count": 2}'
        self.assertTrue(self.run.execute(mode='all'))
        self.assertEqual(self.text.calls[-1][2], {'count': 2})
        for bad in ('not json', '{"count": NaN}'):
            self.video.output = bad
            self.assertFalse(self.run.execute(mode='all'))
            self.assertEqual(self.run.results['reason']['status'], 'stale')
            self.assertEqual(len(self.text.calls), 1)

    def test_schema_edit_invalidates_and_external_schema_rejected(self):
        self.assertTrue(self.run.execute(mode='all'))
        config = copy.deepcopy(self.run.config)
        config['video']['schema'] = {'type': 'array'}
        self.run.configure(config)
        self.assertEqual(self.run.results['video']['status'], 'stale')
        config['video']['schema'] = {'$ref': 'https://example.com/schema'}
        with self.assertRaisesRegex(ValueError, 'remote schemas'):
            self.run.configure(config)

    def test_upload_and_reset_discard_outputs(self):
        self.assertTrue(self.run.execute(mode='all'))
        self.run.upload(b'new video', 'new.mp4')
        self.assertEqual(self.run.results, {})
        fresh = self.run.fresh()
        self.assertFalse(fresh.snapshot()['has_video'])
        self.assertEqual(fresh.results, {})
        self.assertIs(fresh.video_adapter, self.video)

    def test_native_interface_and_missing_weights_fail_without_fallback(self):
        message = video_messages('/tmp/input.mp4', 'Look for gestures')[0]
        self.assertEqual(message['content'][0], {'type': 'video', 'video': '/tmp/input.mp4'})
        with self.assertRaisesRegex(ValueError, 'weights are missing'):
            NativeVideo().complete(b'video', '/definitely/missing/model', 'prompt', {})

    def test_all_frame_coverage_guard_including_odd_frame_padding(self):
        for count in (20, 21):
            inputs = {'video_metadata': [SimpleNamespace(frames_indices=list(range(count)))],
                      'pixel_values_videos': object(), 'video_grid_thw': [[(count + 1) // 2, 4, 4]]}
            verify_video_frames(inputs, count, 2)
            self.assertNotIn('video_metadata', inputs)
        for indices in (None, [0, 2, 4], [2, 1, 0], [0, 1, 1]):
            inputs = {'video_metadata': [SimpleNamespace(frames_indices=indices)]}
            with self.assertRaisesRegex(ValueError, 'every decoded frame'):
                verify_video_frames(inputs, 3, 2)
        with self.assertRaisesRegex(ValueError, 'coverage metadata'):
            verify_video_frames({}, 3, 2)
        with self.assertRaisesRegex(ValueError, 'temporal grid'):
            verify_video_frames({'video_metadata': [SimpleNamespace(frames_indices=[0, 1, 2])],
                                 'pixel_values_videos': object(), 'video_grid_thw': [[1, 4, 4]]}, 3, 2)


if __name__ == '__main__':
    unittest.main()
