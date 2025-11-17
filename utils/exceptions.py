import traceback

class CustomException(Exception):
    def __init__(self, exception: Exception) -> None:
        tb = traceback.extract_tb(tb = exception.__traceback__)[-1]
        customErrorMessage = "Error encountered in line no [{lineNumber}], filename : [{fileName}], saying [{errorMessage}]"
        customErrorMessage = customErrorMessage.format(
            lineNumber = tb.lineno,
            fileName = tb.filename,
            errorMessage = str(exception)
        )
        super().__init__(customErrorMessage)