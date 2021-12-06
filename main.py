import string
from functools import total_ordering

@total_ordering
class Version:
    def __init__(self, version):
        self.numbers = []
        self.ratings = []

        subversions = version.split('.')
        for subvers in subversions:
            subvers = subvers.lower()
            subvers = subvers.replace("alpha", "a")
            subvers = subvers.replace("beta", "b")
            subvers = subvers.replace("-", "")

            digits = []
            letters = []

            for c in subvers:
                if c in string.digits:
                    digits.append(c)
                elif c in string.ascii_lowercase:
                    letters.append(c)

            # append number
            if len(digits) != 0:
                number_string = "".join(digits)
                self.numbers.append(int(number_string))
            else:
                self.numbers.append(0)

            # append rating
            letters_string = "".join(letters)
            rating = None
            if 'a' in letters_string:
                rating = 1
            elif 'b' in letters_string:
                rating = 2
            elif 'rc' in letters_string:
                rating = 3
            elif len(letters_string) == 0:
                rating = 4
            elif 'r' in letters_string:
                rating = 5
            assert rating is not None, "Version is incorrect"
            self.ratings.append(rating)

    def __lt__(self, other):
        min_size = min(len(self.numbers), len(other.numbers))

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

        if len(self.numbers) < len(other.numbers):
            return True

        return False


    def __eq__(self, other):
        if len(self.numbers) != len(other.numbers):
            return False

        for i in range(len(self.numbers)):
            if (self.numbers[i] != other.numbers[i]) or (self.ratings[i] != other.ratings[i]):
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
    ]

    for version_1, version_2 in to_test:
        assert Version(version_1) < Version(version_2), "le failed"
        assert Version(version_2) > Version(version_1), "ge failed"
        assert Version(version_2) != Version(version_1), "neq failed"


if __name__ == "__main__":
     main()

