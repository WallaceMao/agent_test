class ResumeProcessingError(Exception):
    """Base exception for resume process errors"""
    pass


class ModelNotExistsError(ResumeProcessingError):
    """Exception for model not found"""
    pass

