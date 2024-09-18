class WrongVariableDataError(Exception):
    pass

class DuplicateVariableError(Exception):
    pass

class DuplicateLabelError(Exception):
    pass

class GarbageBeforeEndOfLineError(Exception):
    pass

class NoMoreTokensError(Exception):
    pass

class NotLabelError(Exception):
    pass

class NotVariableOrLabelError(Exception):
    pass

class UndefinedVariableError(Exception):
    pass

class UnexpectedEndOfFileError(Exception):
    pass

class UnexpectedEndOfLineError(Exception):
    pass

class UnexpectedParserStateError(Exception):
    pass

class UnknownOperationError(Exception):
    pass

class UndefinedLabelError(Exception):
    pass
