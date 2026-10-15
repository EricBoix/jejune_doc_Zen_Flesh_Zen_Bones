from pdf_to_markdown import (
    ConverterBase,
    ConverterConfig,
    SuperChapter,
    DocumentWithSubChapters,
)


class Converter(ConverterBase):
    """
    Converter for Zen Flesh, Zen Bones book.
    """

    def __init__(self, pdf_filename, structural_info, config: ConverterConfig | None = None):
        document = DocumentWithSubChapters(structural_info.book_title)
        ConverterBase.__init__(self, pdf_filename, document, structural_info, config)

    def break_document_into_chapters(self):
        return ConverterBase.break_document_into_chapters(self, SuperChapter)
