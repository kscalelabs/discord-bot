"""A module that scrapes PDFs for text and images."""

import os
from io import BytesIO

import pdfplumber
import requests
from openai import OpenAI
from PIL import Image

ai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


# def scrape_pdf2(url: str) -> str:
def scrape_pdf2() -> str:
    url = "https://arxiv.org/pdf/2405.12959"
    text = ""
    response = requests.get(url)
    image_number = 0
    with pdfplumber.open(BytesIO(response.content)) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
            for img in page.images:
                x0, y0, x1, y1 = img["x0"], img["y0"], img["x1"], img["y1"]
                image = page.to_image(resolution=300)
                image_path = f"image{image_number}.png"
                image.save(image_path, quality=95)

                pillow_image = Image.open(image_path)
                # pillow_image.show()
                cropped_image = pillow_image.crop((x0, y0, x1, y1))
                cropped_image.show()
                print("showed another image")
                image_number += 1
    pdf.close()
    return text


def main() -> None:
    scrape_pdf2()


if __name__ == "__main__":
    main()
