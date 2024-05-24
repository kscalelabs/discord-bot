"""A module that scrapes PDFs for text and images."""

import os
from io import BytesIO

import pdfplumber
import requests
from openai import OpenAI

ai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


# def scrape_pdf2(url: str) -> str:
def scrape_pdf_text(url: str) -> str:
    text = ""
    response = requests.get(url)
    number = 0
    with pdfplumber.open(BytesIO(response.content)) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
            number += 1
            break
    pdf.close()
    return text


def scrape_pdf_image(url: str, x: int) -> str | None:
    text = ""
    response = requests.get(url)

    with pdfplumber.open(BytesIO(response.content)) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
            image = page.to_image(resolution=300)
            image_path = f"image{x}.png"
            #print(image_path)
            image.save(image_path, quality=95)
            # pillow_image = Image.open(image_path)
            # pillow_image.show()
            return image_path

            """for img in page.images:
                x0, y0, x1, y1 = img["x0"], img["y0"], img["x1"], img["y1"]
                image = page.to_image(resolution=300)
                image_path = f"image{number}.png"
                image.save(image_path, quality=95)

                pillow_image = Image.open(image_path)
                # pillow_image.show()
                cropped_image = pillow_image.crop((x0, y0, x1, y1))
                cropped_image.show()
                print("showed another image")
                number += 1"""

    return None


def main() -> None:
    scrape_pdf_image("", 0)
    scrape_pdf_text("")


if __name__ == "__main__":
    main()
