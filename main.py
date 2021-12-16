import string
from functools import total_ordering

@total_ordering
class Version:

    @staticmethod
    def subversion_to_common_format(s):
        """ Converting subversion to common format """
        s = s.lower()
        s = s.replace("alpha", "a")
        s = s.replace("beta", "b")
        s = s.replace("-", "")

        return s

    @staticmethod
    def split_subversion_into_digits_and_letters(subvers):
        digits = []
        letters = []

        for c in subvers:
            if c in string.digits:
                digits.append(c)
            elif c in string.ascii_lowercase:
                letters.append(c)

        return digits, letters

    def append_to_numbers_and_ratings(self, digits, letters):
        # append number
        if digits:
            number_string = "".join(digits)
            self.numbers.append(int(number_string))
        else:
            self.numbers.append(0)

        # append rating
        letters_string = "".join(letters)
        rating = self.rating_mapping[letters_string]

        self.ratings.append(rating)

    def __init__(self, version):
        self.numbers = []
        self.ratings = []

        self.rating_mapping = {
            "a": 1,
            "b": 2,
            "rc": 3,
            "": 4,
            "r": 5
        }

        subversions = version.split('.')
        for subvers in subversions:
            # converting subversion to common format
            subvers = Version.subversion_to_common_format(subvers)

            # splitting subversion into digits and letters
            digits, letters = Version.split_subversion_into_digits_and_letters(subvers)

            self.append_to_numbers_and_ratings(digits, letters)

    def __lt__(self, other):
        longer = None
        if len(self.numbers) > len(other.numbers):
            longer = self
            min_size = len(other.numbers)
            self_is_longer = True
        else:
            longer = other
            min_size = len(self.numbers)
            self_is_longer = False

        for i in range(min_size):
            if self.numbers[i] < other.numbers[i]:
                return True
            elif self.numbers[i] > other.numbers[i]:
                return False
            else:
                if self.ratings[i] < other.ratings[i]:
                    return True
                elif self.ratings[i] > other.ratings[i]:
                    return False
                else:
                    continue

        for i in range(min_size, len(longer.numbers)):
            if longer.numbers[i] > 0:
                return not self_is_longer
            elif longer.numbers[i] < 0:
                return self_is_longer
            else:
                if longer.ratings[i] > 4:
                    return not self_is_longer
                elif longer.ratings[i] < 4:
                    return self_is_longer
                else:
                    continue

        return False


    def __eq__(self, other):
        longer = None
        if len(self.numbers) > len(other.numbers):
            longer = self
            min_size = len(other.numbers)
        else:
            longer = other
            min_size = len(self.numbers)

        for i in range(min_size):
            if self.numbers[i] != other.numbers[i] or self.ratings[i] != other.ratings[i]:
                return False

        for i in range(min_size, len(longer.numbers)):
            if longer.numbers[i] != 0 or longer.ratings[i] != 4:
                return False

        return True

def main():
    to_test = [
        ("1.0.0", "2.0.0"),
        ("1.0.0", "1.42.0"),
        ("1.2.0", "1.2.42"),
        ("1.1.0-alpha", "1.2.0-alpha.1"),
        ("1.0.1b", "1.0.10-alpha.beta"),
        ("1.0.0-rc.1", "1.0.0"),
        ("1", "1.0.0r"),
        ("1.0.0a", "1")
    ]

    for version_1, version_2 in to_test:
        assert Version(version_1) < Version(version_2), "le failed"
        assert Version(version_2) > Version(version_1), "ge failed"
        assert Version(version_2) != Version(version_1), "neq failed"



if __name__ == "__main__":
    main()

    print(Version("1.0.0") == Version("1"))