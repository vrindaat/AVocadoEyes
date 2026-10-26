"""Optional browser test: pip install playwright; playwright install chromium.

Uses a fake model, real synthetic video decoding and a real local browser server.
No external web resources are allowed during this test.
"""
import copy
import json
import subprocess
import tempfile
import threading
from pathlib import Path
from urllib.parse import urlsplit

import imageio_ffmpeg
from playwright.sync_api import expect, sync_playwright

from avocadoeyes.runner import Run
from avocadoeyes.server import make_server
from test_workbench import FakeAdapter, OBS


def main():
    run = Run(FakeAdapter())
    server = make_server(0, run)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        with tempfile.TemporaryDirectory() as directory, sync_playwright() as p:
            video = Path(directory) / "synthetic.mp4"
            subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-hide_banner", "-loglevel", "error", "-f", "lavfi", "-i", "testsrc=size=320x240:rate=10", "-t", "2", "-pix_fmt", "yuv420p", str(video)], check=True, capture_output=True)
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1360, "height": 1000})
            errors, external = [], []
            page.on("pageerror", lambda error: errors.append(str(error)))

            def intercept(route):
                host = urlsplit(route.request.url).hostname
                if host != "127.0.0.1":
                    external.append(route.request.url)
                    route.abort()
                else:
                    route.continue_()

            page.route("**/*", intercept)
            page.goto(f"http://127.0.0.1:{server.server_address[1]}")
            expect(page.locator("#notice")).to_contain_text("Ready.")
            page.locator("#goals").fill("Find a small group")
            page.locator("#video").set_input_files(video)
            page.locator("#upload").click()
            expect(page.locator("#notice")).to_contain_text("Confirm permission")
            page.locator("#consent").check()
            page.locator("#upload").click()
            expect(page.locator("#notice")).to_contain_text("Clip uploaded")
            page.locator("#run-all").click()
            expect(page.locator("#notice")).to_contain_text("Execution complete")
            assert page.locator(".candidate").count() == 1
            assert page.locator("canvas").count() == 2
            assert run.results["rank"]["status"] == "current"
            page.locator('#inspect-step').select_option('process')
            expect(page.locator('#inspection')).to_contain_text('Group orientation')
            expect(page.locator('#inspection')).not_to_contain_text('effective_prompt')
            expect(page.locator('#inspection')).not_to_contain_text('choices')
            page.locator('#inspection').get_by_text('Model reasoning', exact=True).click()
            expect(page.locator('#inspection')).to_contain_text('Backend explanation')
            original_vision = run.config['models'][run.config['steps'][1]['model']]
            page.get_by_role('combobox', name='process model', exact=True).fill('qwen3.5:35b')
            page.locator('#save').click()
            expect(page.locator('#notice')).to_contain_text('Saved.')
            assert run.config['models'][run.config['steps'][1]['model']] == original_vision
            assert run.results['observe']['status'] == 'current'
            assert run.results['process']['status'] == 'stale'
            assert run.results['rank']['status'] == 'stale'
            page.locator('.step').nth(3).get_by_role('button', name='Run from here', exact=True).click()
            expect(page.locator('#notice')).to_contain_text('Execution complete')
            assert run.adapter.calls[-2]['model'] == 'qwen3.5:35b'
            revision = run.results["observe"]["revision"]
            page.locator("#preferences").fill("Quiet, thoughtful interactions")
            page.locator("#save").click()
            expect(page.locator("#notice")).to_contain_text("Saved.")
            assert run.results["rank"]["status"] == "stale"
            assert run.results["observe"]["revision"] == revision
            assert page.locator(".candidate").count() == 0
            page.locator(".step").nth(4).get_by_role("button", name="Run step", exact=True).click()
            expect(page.locator("#notice")).to_contain_text("Execution complete")
            page.locator("#inspect-step").select_option("observe")
            correction = copy.deepcopy(OBS)
            correction["people"][0]["evidence"][0]["cue"] = "Human corrected cue"
            page.get_by_text("Human correction / new revision", exact=True).click()
            page.locator("#correction").fill(json.dumps(correction))
            page.locator("#correct").click()
            expect(page.locator("#notice")).to_contain_text("Human correction")
            assert run.results["observe"]["source"] == "human"
            page.locator(".step").nth(2).get_by_role("button", name="Run from here", exact=True).click()
            expect(page.locator("#notice")).to_contain_text("Execution complete")
            assert run.results["rank"]["human_assisted"]
            page.get_by_role("button", name="Locate in scene").click()
            Path("artifacts").mkdir(exist_ok=True)
            page.screenshot(path="artifacts/workbench-smoke.png", full_page=True)
            page.set_viewport_size({"width": 390, "height": 844})
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.locator("#reset").click()
            expect(page.locator("#notice")).to_contain_text("Session cleared")
            assert page.locator("canvas").count() == 0
            assert page.locator("#video").input_value() == ""
            assert not errors, errors
            assert not external, external
            browser.close()
            print("Browser smoke passed: consent, upload, decode, run, inspect, preference reuse, correction, lineage, scene overlay, mobile layout, reset; zero external page requests.")
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


if __name__ == "__main__":
    main()
