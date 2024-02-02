import io
import logging
import math
import random
from typing import Union

import docx
import fitz
import nltk
import numpy as np
import pandas as pd
from nltk import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from paddleocr import PaddleOCR
from PIL import Image

# HACK
# os.environ["KMP_DUPLICATE_LIB_OK"] = "True"

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

ocr = PaddleOCR(
    use_angle_cls=True,
    det_model_dir="models/det_onnx/model.onnx",
    rec_model_dir="models/rec_onnx/model.onnx",
    cls_model_dir="models/cls_onnx/model.onnx",
    use_onnx=True,
    lang="en",
)


def filter_noun_phrases(noun_chunks, stopwords):
    """Filters the noun phrases by removing stopwords.

    Args:
        noun_chunks: A list of noun phrases.
        stopwords: A list of stopwords.

    Returns:
        A list of filtered noun phrases.
    """

    filtered_noun_phrases = []
    for noun_phrase in noun_chunks:
        if noun_phrase.text not in stopwords:
            filtered_noun_phrases.append(noun_phrase.text)

    return filtered_noun_phrases


def sanitize_text(text: str, lemmatize: bool = True, *args, **kwargs) -> str:
    """Removes all non-alphanumeric characters from a string.

    This function uses the `RegexpTokenizer` from the Natural Language Toolkit
    (NLTK) to split the input string into words using a regular expression
    pattern that matches only alphanumeric characters. It then joins the
    resulting list of words back into a single string separated by spaces.

    Args:
        text (str): The input string to be sanitized.

    Returns:
        str: The sanitized string, containing only alphanumeric characters
            separated by spaces.
    """

    tokenizer = RegexpTokenizer(r"\w+")
    text = text.lower()
    words = tokenizer.tokenize(text)

    stop_words = set(stopwords.words("english"))
    filtered_tokens = [token for token in words if token not in stop_words]
    if lemmatize:
        lemmatizer = WordNetLemmatizer()
        lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]

        result = " ".join(lemmatized_tokens)
    else:
        result = " ".join(filtered_tokens)

    return result


def sample_pages(documents: list) -> list:
    """Randomly samples a subset of pages from a list of documents.

    Args:
        documents (list): A list of document pages.

    Returns:
        list: A list containing the sampled pages.
    """

    num_documents = len(documents)

    if num_documents > 100:
        sample_size = int(math.sqrt(num_documents))
    else:
        sample_size = min(10, num_documents)

    sampled_documents = random.sample(documents, sample_size)

    return sampled_documents


def get_image_text(image: Union[bytes, np.ndarray], request_id: str, filename: str = "file") -> dict:
    """Extract text from an image using OCR and return the resulting text as a string.

    Args:
        image (list or str): A list of image paths or a single image path as a string.
        filename (str, optional): File name of the input. Defaults to "file".


    Returns:
        str: The text extracted from the image(s) as a string.
    """

    logger = logging.getLogger(request_id)

    logger.info("Running OCR on " + filename)

    if isinstance(image, bytes):
        try:
            pil_object = Image.open(io.BytesIO(image)).convert("RGB")
        except Exception as e:
            logger.error(e)
            logger.info("Image File type not supported: %s", filename)
            pil_object = Image.new("RGB", (500, 500))

        image = np.array(pil_object)

    text = ""
    result = ocr.ocr(image, cls=True)

    for line in result[0]:
        text += line[1][0] + " "

    ocr_result = sanitize_text(text)

    ocr_data = {"text": [ocr_result], "pages": 1}
    return ocr_data


def get_pdf_text(
    iobytes: bytes, request_id: str, filename: str = "file", segregate: bool = False, text_threshold: int = 500
) -> dict:
    """Extracts the text from a PDF document. If the text is less that a
    certain threshold then run the ocr.

    Args:
        iobytes (bytes): A byte stream containing the PDF document.
        request_id (str): The ID of the request.
        filename (str, optional): _description_. Defaults to "file".


    Returns:
        dict: The extracted text data from the PDF document.
    """

    logger = logging.getLogger(request_id)

    logger.info("Running fitz extraction on " + filename)

    ocr_data = {"text": [], "pages": 0}

    with fitz.open(stream=io.BytesIO(iobytes)) as doc:
        ocr_data["pages"] = doc.page_count

        if doc.is_encrypted:
            ocr_data["text"].append("encrypted")
            return ocr_data

        if segregate:
            for i, page in enumerate(doc):
                pdf_text = page.get_text("text")
                if len(pdf_text) <= text_threshold:
                    pix = page.get_pixmap()
                    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
                    ocr = get_image_text(
                        np.array(img),
                        filename=f"{filename}, page number [{i}]",
                        request_id=request_id,
                    )
                    pdf_text = ocr["text"][0]

                ocr_data["text"].append(sanitize_text(pdf_text))
        else:
            ocr_pages = []
            for page in doc:
                pdf_text = page.get_text("text")

                if len(pdf_text) <= text_threshold:
                    ocr_pages.append(page)
                    continue

                ocr_data["text"].append(sanitize_text(pdf_text))

            ocr_pages = sample_pages(ocr_pages)

            for i, page in enumerate(ocr_pages):
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
                ocr = get_image_text(
                    np.array(img),
                    filename=f"{filename}, page number [{i}]",
                    request_id=request_id,
                )

                ocr_data["text"].append(ocr["text"][0])

    return ocr_data


def get_excel_text(iobytes: bytes, request_id: str, filename: str = "file") -> dict:
    """After receiving the excel file, we will read it with the help of pandas
    library and concatenate the text.

    Args:
        iobytes (bytes): A byte stream containing the PDF document.
        request_id (str): The ID of the request.
        filename (str, optional): _description_. Defaults to "file".

    Returns:
        dict: The extracted text data from the Excel document.
    """

    logger = logging.getLogger(request_id)

    logger.info("Extracting Text from " + filename)

    excel_data = io.BytesIO(iobytes)
    df = pd.read_excel(excel_data)

    # Concatenate all the text in the Excel file
    ocr = " ".join(df.stack().astype(str))

    result = {"text": [sanitize_text(ocr)], "pages": 1}
    return result


def get_docx_text(iobytes: bytes, request_id: str, filename: str = "file") -> dict:
    """After receiving the DOC file as a byte stream, extract the text using
    python-docx library.

    Args:
        iobytes (bytes): A byte stream containing the DOC document.
        request_id (str): The ID of the request.
        filename (str, optional): The name of the file. Defaults to "file".

    Returns:
        dict: The extracted text data from the DOC document.
    """

    logger = logging.getLogger(request_id)

    logger.info("Extracting Text from " + filename)

    doc_stream = io.BytesIO(iobytes)
    doc = docx.Document(doc_stream)
    ocr = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    result = {"text": [sanitize_text(ocr)], "pages": 1}
    return result
