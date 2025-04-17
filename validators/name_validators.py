import re
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.validators import RegexValidator


@deconstructible
class InterestValidator(RegexValidator):
    regex = r"(?i)violence|guns|lgbtq|lgbt|gender|nonbinary|pronouns|girlfriend|discrimination|stigmatization|woke|wokeness|wokeism|alcoholism|abortion|evil|sadism|sadist|sadistic|crime|blood|killing|perversion|nudity|terrorism|devil|satan|black magic|jihad|islamic state|vampirism|holy war|onlyfans|satanist|satanism|cannibal|cannibalism|only fans|onlyfans|interest|drugs|narcotics|heroine|mental illness|sodomy|drug cartel|cocaine|kill people|cannibalism|plastic surgery"
    message = f"You can't use this as a interest."
    code = "invalid interest"
    inverse_match = True


@deconstructible
class InterestNameValidator(ASCIIUsernameValidator):
    regex = r"^[ a-zA-Z ']+$"
    message = ("Interest cannot contain digits or any other symbols. Only English letters are allowed.")
    code = "invalid interest name"
    flags = re.ASCII


@deconstructible
class StopWordsValidator(RegexValidator):
    regex = r"(?i)^me\b|^myself\b|^our\b|^ours\b|^ourselves\b|^you\b|^you're\b|^your\b|^yours\b|^yourself\b|^he\b|^him\b|^his\b|^himself\b|^she\b|^her\b|^hers\b|^these\b|^about\b|^will\b|^some\b|^here\b|^but\b|^not\b|^against\b|^between\b|^into\b|^through\b|^during\b|^before\b|^after\b|^above\b|^below\b|^shouldn\b|^will\b|^just\b|^doesn\b|^too\b|^most\b|^further\b|^under\b|^over\b|^off\b|^on\b|^few\b|^each\b|^both\b|^very\b|^why\b|^where\b|^when\b|^there\b|^how\b|^same\b"
    message = ("Using stop words is not allowed.")
    code = "stop words"
    inverse_match = True