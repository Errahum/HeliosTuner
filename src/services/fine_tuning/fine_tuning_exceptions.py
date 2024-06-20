# Module: fine_tuning/fine_tuning_exceptions.py
# Description:
# Define exceptions related to fine-tuning operations.
# -----------------------------------------------------------------------------

class FineTuningError(Exception):
    """Base class for all fine-tuning related exceptions."""
    pass

class FineTuningRequestError(FineTuningError):
    """Raised when a request to the fine-tuning endpoint fails."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class InvalidFineTuningModelError(FineTuningError):
    """Raised when an invalid or deprecated model is used for fine-tuning."""
    pass

class ServiceNotFoundError(FineTuningError):
    """Raised when a requested service is not found."""
    pass
