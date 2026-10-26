"""Browser flow with fixture models; no inference-quality claim."""
import json
import tempfile
import threading
from pathlib import Path
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright, expect
from avocadoeyes.server import make_server
from avocadoeyes.two_stage import TwoStage
from test_two_stage import VideoFake, TextFake


def main():
    video, text = VideoFake(), TextFake()
    run = TwoStage(text, video)
    server = make_server(0, run)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        with tempfile.TemporaryDirectory() as directory, sync_playwright() as p:
            clip = Path(directory) / 'fixture.mp4'
            clip.write_bytes(b'fixture-only-video')
            browser = p.chromium.launch()
            page = browser.new_page(viewport={'width': 1360, 'height': 1000})
            errors, external = [], []
            page.on('pageerror', lambda error: errors.append(str(error)))
            def route(request):
                if urlsplit(request.request.url).hostname != '127.0.0.1':
                    external.append(request.request.url)
                    request.abort()
                else:
                    request.continue_()
            page.route('**/*', route)
            page.goto(f'http://127.0.0.1:{server.server_address[1]}')
            expect(page.locator('#reason-model')).to_have_value('qwen3.5:9b')
            page.locator('#file').set_input_files(clip)
            expect(page.locator('#notice')).to_contain_text('Confirm permission')
            page.locator('#consent').check()
            page.locator('#file').set_input_files(clip)
            expect(page.locator('#notice')).to_contain_text('Video uploaded')
            page.locator('#both').click()
            expect(page.locator('#notice')).to_have_text('Output ready.')
            expect(page.locator('#video-output')).to_contain_text('No people visible')
            expect(page.locator('#reason-output')).to_contain_text('no visible people')
            page.locator('#reason-prompt').fill('Explain uncertainty only.')
            page.locator('#run-reason').click()
            expect(page.locator('#run-reason')).to_be_enabled()
            expect(page.locator('#notice')).to_have_text('Output ready.')
            assert len(video.calls) == 1 and len(text.calls) == 2
            page.locator('#video-schema').fill(json.dumps({'type': 'array'}))
            page.locator('#run-reason').click()
            expect(page.locator('#run-reason')).to_be_enabled()
            expect(page.locator('#notice')).to_contain_text('Run the video model successfully')
            assert len(text.calls) == 2
            page.locator('#run-video').click()
            expect(page.locator('#video-status')).to_have_text('error')
            expect(page.locator('#video-output')).to_contain_text('No people visible')
            page.locator('#video-schema').fill('{')
            page.locator('#save').click()
            expect(page.locator('#notice')).to_have_class('error')
            page.set_viewport_size({'width': 390, 'height': 844})
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
            Path('artifacts').mkdir(exist_ok=True)
            page.screenshot(path='artifacts/two-stage-smoke.png', full_page=True)
            page.locator('#clear').click()
            expect(page.locator('#notice')).to_have_text('Session cleared.')
            expect(page.locator('#video-output')).to_have_text('No output yet.')
            assert not errors, errors
            assert not external, external
            browser.close()
            print('PASS: two-stage browser flow, schema/error display, reuse, reset, mobile layout; no external requests.')
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


if __name__ == '__main__':
    main()
