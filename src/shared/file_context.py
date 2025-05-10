import fitz


class FileContext:
    __path: str = ""

    def __init__(self, path: str = ""):
        self.__path = path

    def _extract_text_from_pdf(self):
        doc = fitz.open(self.__path)
        return "\n".join(page.get_text() for page in doc)

    def _extract_text_from_txt(self):
        with open(self.__path, "r", encoding="utf-8") as f:
            return f.read()

    def get_context(self) -> str:
        if self.__path.endswith(".pdf"):
            raw = self._extract_text_from_pdf()
        else:
            raw = self._extract_text_from_txt()

        return f"\n{raw}"
