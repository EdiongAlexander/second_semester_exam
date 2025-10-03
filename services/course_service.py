from second_semester_exam.schemas.course_schema import Book

class BookService:
    def get_books_by_author(self, books: list[Book], author: str):
        for book in books:
            if book.author == author:
                return book
        return None
    
book_service = BookService()