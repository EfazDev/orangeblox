class ModGeneratorError(Exception): pass
class DeployHistoryError(ModGeneratorError): pass
class ImageSetsNotFoundError(ModGeneratorError): pass
class ImageSetDataNotFoundError(ModGeneratorError): pass
class FileExtractError(ModGeneratorError): pass
class FileRestoreError(ModGeneratorError): pass
class FileDownloadError(ModGeneratorError): pass
class FileCompressError(ModGeneratorError): pass