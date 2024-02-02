from collections import namedtuple
from enum import Enum


class FileType(Enum):
    """Enumeration for different types of file formats.

    Args:
        Enum (Enum): The base class for creating enumerations.
    """

    PDF = ("application/pdf",)
    WORD_DOCUMENT = ("application/vnd.openxmlformats-officedocument.wordprocessingml.document",)
    EXCEL_FILE = (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/vnd.ms-excel",
        "text/csv",
        "application/octet-stream",
    )
    IMAGE = (
        "image/x-ms-bmp",
        "image/gif",
        "image/ief",
        "image/jpeg",
        "image/png",
        "image/svg+xml",
        "image/tiff",
        "image/vnd.microsoft.icon",
        "image/x-cmu-raster",
        "image/x-portable-anymap",
        "image/x-portable-bitmap",
        "image/x-portable-graymap",
        "image/x-portable-pixmap",
        "image/x-rgb",
        "image/x-xbitmap",
        "image/x-xpixmap",
        "image/x-xwindowdump",
    )
    ZIP = ("application/zip",)


class PredictionTypes(Enum):
    OTHERS = "Others"
    INVALID_FILE = "Invalid_File_Type"
    MULTI_TYPE = "Multiple_Documents_Detected"


FileEntry = namedtuple("FileEntry", ["filename", "file_object"])
