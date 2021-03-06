from src.models.response import Response

class ResponseController:

    ### Database updates.
    
    @staticmethod
    def create(author_id: int, thread_id: int, content: str):
        result = Response.create(author_id, thread_id, content)
        return result
