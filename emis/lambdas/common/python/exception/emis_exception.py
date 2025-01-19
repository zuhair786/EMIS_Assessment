# base class for all exceptions
class EMISError(Exception):
    def __init__(self, error_content=None, message=None):
        self.content = error_content
        self._message = message
        return

    def __str__(self):
        output = []
        if self._message is not None:
            output.append(f'{self._message}')
        if self.content is not None:
            output.append(f'{self.content}')
        if output:
            return ' : '.join(output)
        return type(self).__name__
    

class JobFailedError(EMISError):
    def __init__(self, message=None):
        super().__init__(None, message)
        return

class NoDataFoundError(EMISError):
    def __init__(self, message=None):
        super().__init__(None, message)
        return
    
class NoFileFoundError(EMISError):
    def __init__(self, message=None):
        super().__init__(None, message)
        return
    
class NonJsonFormatError(EMISError):
    def __init__(self, message=None):
        super().__init__(None, message)
        return