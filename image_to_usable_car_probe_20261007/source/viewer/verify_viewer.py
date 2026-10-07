#!/usr/bin/env python3
"""Verify actual saved GLBs in the browser; never creates or substitutes assets."""
import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import urljoin, urlsplit
from urllib.request import urlopen

from playwright.sync_api import sync_playwright


def digest_url(url):
    with urlopen(url) as response:
        return hashlib.sha256(response.read()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', default='http://127.0.0.1:8777/source/viewer/')
    parser.add_argument('--output', type=Path, default=Path(__file__).parent / 'verification')
    parser.add_argument('--chromium', default='/usr/bin/chromium')
    parser.add_argument('--authored', action='store_true', help='Require and exercise the authored DoorPivot export')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    origin = urlsplit(args.url).netloc
    errors, foreign_requests = [], []
    result = {'status': 'started', 'phase': 'authored' if args.authored else 'raw', 'url': args.url}

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=args.chromium, headless=True, args=[
            '--no-sandbox', '--disable-dev-shm-usage', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'
        ])
        page = browser.new_page(viewport={'width': 1440, 'height': 960}, device_scale_factor=1)
        page.on('pageerror', lambda error: errors.append(str(error)))

        def local_only(route):
            address = urlsplit(route.request.url)
            if address.scheme in ('http', 'https') and address.netloc != origin:
                foreign_requests.append(route.request.url)
                route.abort()
            else:
                route.continue_()

        page.route('**/*', local_only)
        try:
            page.goto(args.url, wait_until='networkidle')
            page.wait_for_function('window.authoringAPI?.ready || window.authoringAPI?.getState().errors.length', timeout=90000)
            initial = page.evaluate('authoringAPI.getState()')
            assert initial['ready'] and not initial['errors'], initial
            assert initial['mode'] == 'raw'
            assert page.locator('#doorSlider').is_disabled()
            raw_url = urljoin(args.url, initial['urls']['raw'])
            result['raw_sha256'] = digest_url(raw_url)
            result['initial_state'] = initial
            result['raw_materials'] = page.evaluate('authoringAPI.getMaterials()')
            assert result['raw_materials'], 'No mesh materials found'
            for view in ['hero', 'side', 'front']:
                page.evaluate('(view) => authoringAPI.setView(view)', view)
                page.screenshot(path=str(args.output / f'raw_{view}.png'))
            page.evaluate("authoringAPI.setView('hero')")

            if args.authored:
                page.evaluate("authoringAPI.setMode('authored')")
                state = page.evaluate('authoringAPI.getState()')
                assert state['motionMode'], state['motionReason']
                assert not page.locator('#doorSlider').is_disabled()
                result['authored_state'] = state
                result['authored_materials'] = page.evaluate('authoringAPI.getMaterials()')
                authored_url = urljoin(args.url, state['urls']['authored'])
                result['authored_sha256'] = digest_url(authored_url)
                poses = {}
                for degrees, label in [(0, 'closed'), (30, 'intermediate'), (60, 'open')]:
                    page.evaluate('(degrees) => authoringAPI.setAngle(degrees)', degrees)
                    sampled = page.evaluate('authoringAPI.getState()')
                    assert abs(sampled['measuredPivotAngleDegrees'] - degrees) < 0.01, sampled
                    poses[label] = page.evaluate('authoringAPI.getTransforms()')
                    page.screenshot(path=str(args.output / f'authored_{label}.png'))
                closed = {node['uuid']: node for node in poses['closed']}
                opened = {node['uuid']: node for node in poses['open']}
                moving, fixed = [], []
                for identity, node in closed.items():
                    delta = max(abs(a - b) for a, b in zip(node['matrixWorld'], opened[identity]['matrixWorld']))
                    (moving if delta > 1e-7 else fixed).append(node['name'])
                assert moving and fixed, {'moving': moving, 'fixed': fixed}
                page.evaluate('authoringAPI.setAngle(0)')
                reset = {node['uuid']: node for node in page.evaluate('authoringAPI.getTransforms()')}
                reset_delta = max(abs(a - b) for identity, node in closed.items() for a, b in zip(node['matrixWorld'], reset[identity]['matrixWorld']))
                assert reset_delta < 1e-7
                page.click('#openButton')
                assert page.evaluate('authoringAPI.getState().angleDegrees') == 60
                page.click('#closedButton')
                assert page.evaluate('authoringAPI.getState().angleDegrees') == 0
                page.evaluate("authoringAPI.setView('side')")
                for degrees, label in [(0, 'closed'), (30, 'intermediate'), (60, 'open')]:
                    page.evaluate('(degrees) => authoringAPI.setAngle(degrees)', degrees)
                    page.screenshot(path=str(args.output / f'authored_{label}_side.png'))
                page.evaluate("authoringAPI.setView('hero')")
                page.evaluate('authoringAPI.setAngle(0)')
                page.screenshot(path=str(args.output / 'authored_comparison_closed.png'))
                compare_camera = page.evaluate('authoringAPI.getState().cameraPosition')
                page.evaluate("authoringAPI.setMode('raw')")
                page.screenshot(path=str(args.output / 'raw_comparison.png'))
                assert page.evaluate('authoringAPI.getState().cameraPosition') == compare_camera
                page.evaluate("authoringAPI.setMode('authored')")
                page.locator('#doorSlider').evaluate("element => { element.value = '22.5'; element.dispatchEvent(new Event('input', { bubbles: true })); }")
                assert abs(page.evaluate('authoringAPI.getState().angleDegrees') - 22.5) < 1e-6
                page.click('#playButton')
                page.wait_for_function('authoringAPI.getState().playing && authoringAPI.getState().angleDegrees > 22.5')
                page.click('#playButton')
                paused = page.evaluate('authoringAPI.getState().angleDegrees')
                page.wait_for_timeout(150)
                assert page.evaluate('authoringAPI.getState().angleDegrees') == paused
                camera_before = page.evaluate('authoringAPI.getState().cameraPosition')
                page.evaluate("authoringAPI.setMode('raw')")
                assert page.locator('#doorSlider').is_disabled()
                assert page.evaluate('authoringAPI.getState().cameraPosition') == camera_before
                page.evaluate("authoringAPI.setMode('authored')")
                assert not page.locator('#doorSlider').is_disabled()
                assert page.evaluate('authoringAPI.getState().cameraPosition') == camera_before
                assert digest_url(authored_url) == result['authored_sha256']
                result.update({'poses': poses, 'moving_nodes': moving, 'fixed_nodes': fixed, 'reset_max_matrix_delta': reset_delta, 'comparison_camera': compare_camera})

            assert digest_url(raw_url) == result['raw_sha256']
            assert not errors, errors
            assert not foreign_requests, foreign_requests
            result.update({'status': 'passed', 'browser': browser.version, 'final_state': page.evaluate('authoringAPI.getState()')})
        except Exception as error:
            result.update({'status': 'failed', 'failure': str(error)})
            raise
        finally:
            result.update({'javascript_errors': errors, 'external_requests': foreign_requests})
            (args.output / 'viewer_verification.json').write_text(json.dumps(result, indent=2) + '\n')
            print(json.dumps({key: value for key, value in result.items() if key not in ('poses', 'raw_materials', 'authored_materials')}, indent=2))
            browser.close()


if __name__ == '__main__':
    main()
