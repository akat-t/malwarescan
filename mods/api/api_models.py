from __future__ import absolute_import
import pprint
import typing
from datetime import datetime
import six
from libs import util

# Base model
T = typing.TypeVar("T")


class Model:
    # swaggerTypes: The key is attribute name and the
    # value is attribute type.
    swagger_types = {}

    # attributeMap: The key is attribute name and the
    # value is json key in definition.
    attribute_map = {}

    @classmethod
    def from_dict(cls: typing.Type[T], dikt) -> T:
        """Returns the dict as a model"""
        return util.deserialize_model(dikt, cls)

    def to_dict(self):
        """Returns the model properties as a dict

        :rtype: dict
        """
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(
                    map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, value)
                )
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict())
                        if hasattr(item[1], "to_dict")
                        else item,
                        value.items(),
                    )
                )
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model

        :rtype: str
        """
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other


# Evaluation Status model
class EvaluationStatus(Model):
    """
    allowed enum values
    """

    INPROGRESS = "InProgress"
    COMPLETE = "Complete"
    ERROR = "Error"

    def __init__(self):  # noqa: E501
        """EvaluationStatus - a model defined in Swagger

        """
        self.swagger_types = {}

        self.attribute_map = {}

    @classmethod
    def from_dict(cls, dikt) -> "EvaluationStatus":
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The EvaluationStatus of this EvaluationStatus.  # noqa: E501
        :rtype: EvaluationStatus
        """
        return util.deserialize_model(dikt, cls)


# Evaluation File model
class EvaluationFile(Model):
    def __init__(
        self,
        file_name: str = None,
        sha256: str = None,
        status_date: datetime = None,
        malicious: bool = None,
        message: str = None,
    ):  # noqa: E501,E252
        """EvaluationFile - a model defined in Swagger

        :param file_name: The file_name of this EvaluationFile.  # noqa: E501
        :type file_name: str
        :param sha256: The sha256 of this EvaluationFile.  # noqa: E501
        :type sha256: str
        :param status_date: The status_date of this EvaluationFile.  # noqa: E501
        :type status_date: datetime
        :param malicious: The malicious of this EvaluationFile.  # noqa: E501
        :type malicious: bool
        :param message: The message of this EvaluationFile.  # noqa: E501
        :type message: str
        """
        self.swagger_types = {
            "file_name": str,
            "sha256": str,
            "status_date": datetime,
            "malicious": bool,
            "message": str,
        }

        self.attribute_map = {
            "file_name": "fileName",
            "sha256": "sha256",
            "status_date": "statusDate",
            "malicious": "malicious",
            "message": "message",
        }

        self._file_name = file_name
        self._sha256 = sha256
        self._status_date = status_date
        self._malicious = malicious
        self._message = message

    @classmethod
    def from_dict(cls, dikt) -> "EvaluationFile":
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The EvaluationFile of this EvaluationFile.  # noqa: E501
        :rtype: EvaluationFile
        """
        return util.deserialize_model(dikt, cls)

    @property
    def file_name(self) -> str:
        """Gets the file_name of this EvaluationFile.

        File name  # noqa: E501

        :return: The file_name of this EvaluationFile.
        :rtype: str
        """
        return self._file_name

    @file_name.setter
    def file_name(self, file_name: str):
        """Sets the file_name of this EvaluationFile.

        File name  # noqa: E501

        :param file_name: The file_name of this EvaluationFile.
        :type file_name: str
        """

        self._file_name = file_name

    @property
    def sha256(self) -> str:
        """Gets the sha256 of this EvaluationFile.

        SHA-256 hash of the file to evaluate  # noqa: E501

        :return: The sha256 of this EvaluationFile.
        :rtype: str
        """
        return self._sha256

    @sha256.setter
    def sha256(self, sha256: str):
        """Sets the sha256 of this EvaluationFile.

        SHA-256 hash of the file to evaluate  # noqa: E501

        :param sha256: The sha256 of this EvaluationFile.
        :type sha256: str
        """

        self._sha256 = sha256

    @property
    def status_date(self) -> datetime:
        """Gets the status_date of this EvaluationFile.

        Date/time of the status  # noqa: E501

        :return: The status_date of this EvaluationFile.
        :rtype: datetime
        """
        return self._status_date

    @status_date.setter
    def status_date(self, status_date: datetime):
        """Sets the status_date of this EvaluationFile.

        Date/time of the status  # noqa: E501

        :param status_date: The status_date of this EvaluationFile.
        :type status_date: datetime
        """
        if status_date is None:
            raise ValueError(
                "Invalid value for `status_date`, must not be `None`"
            )  # noqa: E501

        self._status_date = status_date

    @property
    def malicious(self) -> bool:
        """Gets the malicious of this EvaluationFile.

        Flag indicating whether the evaluation identified this file malicious or not  # noqa: E501

        :return: The malicious of this EvaluationFile.
        :rtype: bool
        """
        return self._malicious

    @malicious.setter
    def malicious(self, malicious: bool):
        """Sets the malicious of this EvaluationFile.

        Flag indicating whether the evaluation identified this file malicious or not  # noqa: E501

        :param malicious: The malicious of this EvaluationFile.
        :type malicious: bool
        """

        self._malicious = malicious

    @property
    def message(self) -> str:
        """Gets the message of this EvaluationFile.

        Message  # noqa: E501

        :return: The message of this EvaluationFile.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message: str):
        """Sets the message of this EvaluationFile.

        Message  # noqa: E501

        :param message: The message of this EvaluationFile.
        :type message: str
        """

        self._message = message


# Evaluation model
class Evaluation(Model):
    def __init__(
        self,
        id: str = None,
        correlation_id: str = None,
        date: datetime = None,
        elapsed_time: str = None,
        status_date: datetime = None,
        malicious: bool = None,
        files: typing.List[EvaluationFile] = None,
    ):
        """Evaluation - a model defined in Swagger

        :param id: The id of this Evaluation.  # noqa: E501
        :type id: str
        :param correlation_id: The correlation_id of this Evaluation.  # noqa: E501
        :type correlation_id: str
        :param date: The date of this Evaluation.  # noqa: E501
        :type date: datetime
        :param elapsed_time: The elapsed_time of this Evaluation.  # noqa: E501
        :type elapsed_time: str
        :param status_date: The status_date of this Evaluation.  # noqa: E501
        :type status_date: datetime
        :param malicious: The malicious of this Evaluation.  # noqa: E501
        :type malicious: bool
        :param files: The files of this Evaluation.  # noqa: E501
        :type files: typing.List[EvaluationFile]
        """
        self.swagger_types = {
            "id": str,
            "correlation_id": str,
            "date": datetime,
            "elapsed_time": str,
            "status_date": datetime,
            "malicious": bool,
            "files": typing.List[EvaluationFile],
        }

        self.attribute_map = {
            "id": "id",
            "correlation_id": "correlationID",
            "date": "date",
            "elapsed_time": "elapsedTime",
            "status_date": "statusDate",
            "malicious": "malicious",
            "files": "files",
        }

        self._id = id
        self._correlation_id = correlation_id
        self._date = date
        self._elapsed_time = elapsed_time
        self._status_date = status_date
        self._malicious = malicious
        self._files = files

    @classmethod
    def from_dict(cls, dikt) -> "Evaluation":
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Evaluation of this Evaluation.  # noqa: E501
        :rtype: Evaluation
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> str:
        """Gets the id of this Evaluation.

        ID of the evaluation  # noqa: E501

        :return: The id of this Evaluation.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id: str):
        """Sets the id of this Evaluation.

        ID of the evaluation  # noqa: E501

        :param id: The id of this Evaluation.
        :type id: str
        """

        self._id = id

    @property
    def correlation_id(self) -> str:
        """Gets the correlation_id of this Evaluation.

        Correlation ID  # noqa: E501

        :return: The correlation_id of this Evaluation.
        :rtype: str
        """
        return self._correlation_id

    @correlation_id.setter
    def correlation_id(self, correlation_id: str):
        """Sets the correlation_id of this Evaluation.

        Correlation ID  # noqa: E501

        :param correlation_id: The correlation_id of this Evaluation.
        :type correlation_id: str
        """

        self._correlation_id = correlation_id

    @property
    def date(self) -> datetime:
        """Gets the date of this Evaluation.

        Date/time the request for evaluation was made  # noqa: E501

        :return: The date of this Evaluation.
        :rtype: datetime
        """
        return self._date

    @date.setter
    def date(self, date: datetime):
        """Sets the date of this Evaluation.

        Date/time the request for evaluation was made  # noqa: E501

        :param date: The date of this Evaluation.
        :type date: datetime
        """
        if date is None:
            raise ValueError(
                "Invalid value for `date`, must not be `None`"
            )  # noqa: E501

        self._date = date

    @property
    def elapsed_time(self) -> str:
        """Gets the elapsed_time of this Evaluation.

        Elapsed time since the request for evaluation was made  # noqa: E501

        :return: The elapsed_time of this Evaluation.
        :rtype: str
        """
        return self._elapsed_time

    @elapsed_time.setter
    def elapsed_time(self, elapsed_time: str):
        """Sets the elapsed_time of this Evaluation.

        Elapsed time since the request for evaluation was made  # noqa: E501

        :param elapsed_time: The elapsed_time of this Evaluation.
        :type elapsed_time: str
        """
        if elapsed_time is None:
            raise ValueError(
                "Invalid value for `elapsed_time`, must not be `None`"
            )  # noqa: E501

        self._elapsed_time = elapsed_time

    @property
    def status_date(self) -> datetime:
        """Gets the status_date of this Evaluation.

        Date/time of the status  # noqa: E501

        :return: The status_date of this Evaluation.
        :rtype: datetime
        """
        return self._status_date

    @status_date.setter
    def status_date(self, status_date: datetime):
        """Sets the status_date of this Evaluation.

        Date/time of the status  # noqa: E501

        :param status_date: The status_date of this Evaluation.
        :type status_date: datetime
        """
        if status_date is None:
            raise ValueError(
                "Invalid value for `status_date`, must not be `None`"
            )  # noqa: E501

        self._status_date = status_date

    @property
    def malicious(self) -> bool:
        """Gets the malicious of this Evaluation.

        Flag indicating whether the evaluation identified a file as malicious or not.  # noqa: E501

        :return: The malicious of this Evaluation.
        :rtype: bool
        """
        return self._malicious

    @malicious.setter
    def malicious(self, malicious: bool):
        """Sets the malicious of this Evaluation.

        Flag indicating whether the evaluation identified a file as malicious or not.  # noqa: E501

        :param malicious: The malicious of this Evaluation.
        :type malicious: bool
        """

        self._malicious = malicious

    @property
    def files(self) -> typing.List[EvaluationFile]:
        """Gets the files of this Evaluation.

        Files  # noqa: E501

        :return: The files of this Evaluation.
        :rtype: typing.List[EvaluationFile]
        """
        return self._files

    @files.setter
    def files(self, files: typing.List[EvaluationFile]):
        """Sets the files of this Evaluation.

        Files  # noqa: E501

        :param files: The files of this Evaluation.
        :type files: typing.List[EvaluationFile]
        """

        self._files = files
