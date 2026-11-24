from pdf_to_markdown import (
    ConverterBase,
    SuperChapter,
    DocumentWithSubChapters,
)


class Converter(ConverterBase):
    """
    Converter for Zen Flesh, Zen Bones book.
    """

    # Lines of paragraphs longer than this are broken (markdownlint MD013),
    # without starting new paragraphs.
    DEFAULT_MAXIMUM_LINE_LENGTH = 800

    def __init__(self, pdf_filename, structural_info, maximum_line_length=None):
        document = DocumentWithSubChapters(structural_info.book_title)
        if maximum_line_length is None:
            maximum_line_length = self.DEFAULT_MAXIMUM_LINE_LENGTH
        ConverterBase.__init__(
            self, pdf_filename, document, structural_info, maximum_line_length
        )

    def break_document_into_chapters(self):
        return ConverterBase.break_document_into_chapters(self, SuperChapter)
