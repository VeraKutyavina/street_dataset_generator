from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from maps.serializer import ScreenshotCreateSerializer
from playwright.sync_api import sync_playwright


def index(request):
    context = {}
    return render(request, 'maps/index.html', context)


def test(request):
    print('wehdbjwhebd')
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(record_video_dir="videos/")
        page = context.new_page()
        page.goto('http://127.0.0.1:8000/maps/')
        page.wait_for_timeout(5000)

        for i in range(50):
            print("рас ", i)
            page.locator('canvas').click(position={'x': 614, 'y': 478}, timeout=15000)
            page.wait_for_timeout(1000)
        page.locator('wedhbjhwebdjhbwejdhbjhwbe').click()
        print(page.title())
        browser.close()
        context.close()
    return render(request, 'maps/index.html', {})


class SaveScreenshot(CreateAPIView):
    serializer_class = ScreenshotCreateSerializer
    permission_classes = [AllowAny]
