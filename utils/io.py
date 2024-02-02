import csv
import io
import logging
import zipfile

import backoff
import magic
import numpy as np
import pandas as pd
import requests

from utils.constants import FileEntry, FileType, PredictionTypes
from utils.encryption import calculate_sha256
from utils.ocr import get_docx_text, get_excel_text, get_image_text, get_pdf_text


class FileProcessor:
    def __init__(self, documents: list, request_id: str, segregate: bool = False):
        self.documents = documents
        self.request_id = request_id
        self.segregate = segregate
        self.request_info = {}
        self.extracted_documents = []

    def process_files(self):
        """Process files and does the ocr in the zip archive.

        Returns:
            str: Returns ocr data in csv format.
        """

        logger = logging.getLogger(self.request_id)

        csv_data = []

        for document in self.documents:
            filename = document.filename
            file = document.file_object
            mime_type = magic.from_buffer(file, mime=True)
            logger.info("Processing %s", filename)

            for key in self.file_type_mapping:
                if mime_type in key:
                    process_func = self.file_type_mapping[key]
                    result = process_func(self, contents=file, filename=filename)
                    csv_data.extend(result)
                    break
            else:
                logger.info(
                    "The file type is not supported by the platform, please check the file %s",
                    mime_type,
                )

                contents_hash = calculate_sha256(file)
                csv_data.extend([[contents_hash, filename, " ", 0]])
                self.request_info.update(
                    {contents_hash: {"filename": filename, "pages": 0, "remarks": PredictionTypes.INVALID_FILE.value}}
                )

        headers = ["parent_hash", "filename", "text", "page_number"]
        result_csv = self._create_csv_string(headers, csv_data)

        return result_csv

    def _do_post_processing(self, ocr_data: dict, contents: bytes, filename: str) -> list:
        """Performs post-processing on OCR data and returns a list of results.

        Args:
            ocr_data (dict): A dictionary containing OCR data, including the extracted text and number of pages.
            contents (bytes): The contents of the file.
            filename (str): The name of the file.

        Returns:
            list: A list of post-processed results. Each result is represented as a sublist with the following elements:
                - contents_hash: The SHA256 hash of the file contents.
                - filename: The name of the file.
                - ocr: The post-processed OCR text.
                - page_index: The index of the page in the OCR data.
        """
        file_result = []
        ocr_result, number_of_pages = (
            ocr_data["text"],
            ocr_data["pages"],
        )

        contents_hash = calculate_sha256(contents)

        self.request_info.update({contents_hash: {"filename": filename, "pages": number_of_pages}})
        for i, ocr in enumerate(ocr_result):
            if not (ocr and len(ocr)):
                ocr = " "
            file_result.append([contents_hash, filename, ocr, i])

        extracted_document = FileEntry(filename, contents)
        self.extracted_documents.append(extracted_document)
        return file_result

    def _process_zip(self, contents: bytes, filename: str) -> list:
        """Process a zip file and extract information from its contents.

        Args:
            contents (bytes): The binary contents of the zip file.
            filename (str): The name of the zip file.

        Returns:
            list: A list of extracted information from the zip file.
        """
        logger = logging.getLogger(self.request_id)
        zip_result = []
        logger.info("Opening zip file")
        zip_file = zipfile.ZipFile(io.BytesIO(contents))
        file_list = zip_file.infolist()

        file_name_list = [file.filename for file in file_list]

        logger.info("Files in zip %s", str(file_name_list))
        for file_info in file_list:
            if file_info.is_dir() or file_info.filename.startswith("__MACOSX"):
                continue

            filename = file_info.filename
            logger.info("Processing %s", filename)

            with zip_file.open(filename) as file:
                individual_file = file.read()
                mime_type = magic.from_buffer(individual_file, mime=True)

                for key in self.file_type_mapping:
                    if mime_type in key:
                        process_func = self.file_type_mapping[key]
                        result = process_func(self, contents=individual_file, filename=filename)
                        zip_result.extend(result)
                        break
                else:
                    logger.info(
                        "The file type is not supported by the platform, please check the file %s",
                        mime_type,
                    )

                    contents_hash = calculate_sha256(individual_file)
                    zip_result.extend([[contents_hash, filename, " ", 0]])
                    self.request_info.update(
                        {
                            contents_hash: {
                                "filename": filename,
                                "pages": 0,
                                "remarks": PredictionTypes.INVALID_FILE.value,
                            }
                        }
                    )

        return zip_result

    def _process_pdf(self, contents: bytes, filename: str) -> list:
        """Process a PDF file and extract text from its contents using OCR.

        Args:
            contents (bytes): The binary contents of the PDF file.
            filename (str): The name of the PDF file.

        Returns:
            list: A list of extracted information from the PDF file.
        """
        pdf_data = get_pdf_text(
            iobytes=contents, request_id=self.request_id, filename=filename, segregate=self.segregate
        )
        pdf_result = self._do_post_processing(ocr_data=pdf_data, contents=contents, filename=filename)
        return pdf_result

    def _process_image(self, contents: bytes, filename: str) -> list:
        """Process a image file and extract text from its contents using OCR.

        Args:
            contents (bytes): The binary contents of the PDF file.
            filename (str): The name of the PDF file.

        Returns:
            list: A list of extracted information from the image file.
        """
        image_data = get_image_text(image=contents, request_id=self.request_id, filename=filename)
        image_result = self._do_post_processing(ocr_data=image_data, contents=contents, filename=filename)
        return image_result

    def _process_excel(self, contents: bytes, filename: str) -> list:
        """Process a excel file and extract text from it.

        Args:
            contents (bytes): The binary contents of the PDF file.
            filename (str): The name of the PDF file.

        Returns:
            list: A list of extracted information from the excel file.
        """
        excel_data = get_excel_text(iobytes=contents, request_id=self.request_id, filename=filename)
        excel_result = self._do_post_processing(ocr_data=excel_data, contents=contents, filename=filename)
        return excel_result

    def _process_word_doc(self, contents: bytes, filename: str) -> list:
        """Process a docx file and extract text from it.

        Args:
            contents (bytes): The binary contents of the PDF file.
            filename (str): The name of the PDF file.

        Returns:
            list: A list of extracted information from the PDF file.
        """
        docx_data = get_docx_text(iobytes=contents, request_id=self.request_id, filename=filename)
        docx_result = self._do_post_processing(ocr_data=docx_data, contents=contents, filename=filename)
        return docx_result

    def _create_csv_string(self, headers: list, csv_data: list) -> str:
        """Create a CSV string from a list of data.

        Args:
            data (list): A list of rows, where each row is a list of values.

        Returns:
            str: The CSV string representation of the data.
        """

        csv_string = io.StringIO()
        csv_writer = csv.writer(csv_string, quoting=csv.QUOTE_ALL)
        csv_writer.writerow(headers)

        for row in csv_data:
            csv_writer.writerow(row)

        csv_string.seek(0)
        csv_formatted_data = csv_string.getvalue()
        csv_string.close()
        return csv_formatted_data

    file_type_mapping = {
        FileType.PDF.value: _process_pdf,
        FileType.EXCEL_FILE.value: _process_excel,
        FileType.WORD_DOCUMENT.value: _process_word_doc,
        FileType.IMAGE.value: _process_image,
        FileType.ZIP.value: _process_zip,
    }


# class MetaReportGenerator:
#     def __init__(
#         self,
#         files_info: dict,
#         csv_string: str,
#         mapping: dict,
#         segregate: bool = False,
#         probability_threshold: float = 0.95,
#         distance_threshold: float = 0,
#     ) -> None:
#         self.csv_string = csv_string
#         self.files_info = files_info
#         self.mapping = mapping
#         self.segregate = segregate
#         self.probability_threshold = probability_threshold
#         self.distance_threshold = distance_threshold
#         self.sagemaker_result = {}

#     def process(self):
#         """Process the CSV data and generate prediction results.

#         Returns:
#             dict: A dictionary containing the prediction results.
#         """

#         self._preprocess_prediction_data()
#         prediction_info = self._generate_prediction_info()
#         self._add_prediction_info(prediction_info)

#         if self.segregate:
#             self._add_segregation_results()

#         return self.files_info

#     def _preprocess_prediction_data(self):
#         df = pd.read_csv(io.StringIO(self.csv_string))

#         parent_hashes = df["parent_hash"]
#         predicted_classes = df["predicted"]
#         prediction_scores = df["prediction_scores"].str[1:-1].str.split().apply(lambda x: np.asarray(x, dtype=float))
#         probability_scores = df["probability_scores"].str[1:-1].str.split().apply(lambda x: np.asarray(x, dtype=float))
#         page_numbers = df["page_number"]

#         self.sagemaker_result = {
#             "parent_hashes": parent_hashes,
#             "predicted_classes": predicted_classes,
#             "prediction_scores": prediction_scores,
#             "probability_scores": probability_scores,
#             "page_numbers": page_numbers,
#         }

#     def _generate_prediction_info(self) -> dict:
#         prediction_info = {}

#         for parent_hash, predicted, prediction_score, probability_score in zip(
#             self.sagemaker_result["parent_hashes"],
#             self.sagemaker_result["predicted_classes"],
#             self.sagemaker_result["prediction_scores"],
#             self.sagemaker_result["probability_scores"],
#         ):
#             if np.all(probability_score < self.probability_threshold) and np.all(
#                 prediction_score < self.distance_threshold
#             ):
#                 predicted = PredictionTypes.OTHERS.value

#             prediction_info.setdefault(parent_hash, {}).setdefault(predicted, {}).setdefault("pages", 0)
#             prediction_info.setdefault(parent_hash, {}).setdefault(predicted, {}).setdefault("confidence", 0)
#             prediction_info[parent_hash][predicted]["pages"] += 1
#             prediction_info[parent_hash][predicted]["confidence"] += np.max(probability_score) * 100

#         for hash_key, hash_value in prediction_info.items():
#             for key, value in hash_value.items():
#                 value["confidence"] /= value["pages"]

#         return prediction_info

#     def _add_prediction_info(self, prediction_info: dict) -> None:
#         for hash_key, hash_value in self.files_info.items():
#             if prediction_info.get(hash_key) is None:
#                 continue

#             if self.files_info[hash_key].get("remarks") == PredictionTypes.INVALID_FILE.value:
#                 continue

#             if len(prediction_info[hash_key]) == 1:
#                 predicted_class = next(iter(prediction_info[hash_key]))
#                 confidence = prediction_info[hash_key][predicted_class]["confidence"]
#                 self.files_info[hash_key]["prediction"] = {
#                     "class": predicted_class,
#                     "confidence": confidence,
#                     "text": str(predicted_class).replace("_", " "),
#                 }
#             else:
#                 self.files_info[hash_key]["prediction"] = {
#                     "class": PredictionTypes.MULTI_TYPE.value,
#                     "text": PredictionTypes.MULTI_TYPE.value.replace("_", " "),
#                 }
#             self.files_info[hash_key]["prediction_info"] = prediction_info[hash_key]

#     def _add_segregation_results(self) -> None:
#         for parent_hash, predicted, prediction_score, probability_score, page_number in zip(
#             self.sagemaker_result["parent_hashes"],
#             self.sagemaker_result["predicted_classes"],
#             self.sagemaker_result["prediction_scores"],
#             self.sagemaker_result["probability_scores"],
#             self.sagemaker_result["page_numbers"],
#         ):
#             if self.files_info[parent_hash].get("remarks", None) == PredictionTypes.INVALID_FILE.value:
#                 continue

#             if np.all(probability_score < self.probability_threshold) and np.all(
#                 prediction_score < self.distance_threshold
#             ):
#                 predicted = PredictionTypes.OTHERS.value

#             self.files_info[parent_hash].setdefault("pages_info", [])
#             self.files_info[parent_hash]["pages_info"].append(
#                 {"page_number": page_number, "class": predicted, "text": str(predicted).replace("_", " ")}
#             )


# def is_retryable_error(e):
#     try:
#         return 400 <= e.response.status_code < 500
#     except Exception:
#         return True


# class CallbackExecutor:
#     def __init__(self, callback_url, request_id):
#         self.callback_url = callback_url
#         self.request_id = request_id

#     @backoff.on_exception(
#         backoff.expo,
#         requests.exceptions.RequestException,
#         max_tries=3,
#         raise_on_giveup=False,
#         giveup=is_retryable_error,
#     )
#     def execute(self, data=None, files=None, computed_hmac=None):
#         response = requests.post(
#             self.callback_url,
#             files=files,
#             json=data,
#             headers={"x-request-id": self.request_id, "x-hash-signature": computed_hmac},
#         )
#         logger = logging.getLogger(self.request_id)
#         logger.info("Callback POST response code: %s", response.status_code)

#         response.raise_for_status()

#         logger.info(
#             "POST request to callback URL successful. HTTP status code: %s",
#             response.status_code,
#         )
