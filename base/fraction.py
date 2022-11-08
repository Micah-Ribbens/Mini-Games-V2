class Fraction:
    """Has a numerator and a denominator along with utility functions that go along with fractions"""
    numerator = None
    denominator = None

    def __init__(self, numerator, denominator):
        """ summary: initializes the fraction
            params:
                numerator: int; the top part of the fraction
                denominator: int; the bottom part of the fraction
            returns: None
        """

        self.numerator = numerator
        self.denominator = denominator

    def get_reciprocal(self):
        """ summary: In math reciprocal is denominator/numerator
            params: None
            returns: Fraction; a new Fraction where the denominator and numerator switch places
        """

        return Fraction(self.denominator, self.numerator)

    def get_number(self):
        """ summary: turns the fraction into a number
            params: None
            returns: float; the
        """

        return self.numerator / self.denominator

    def get_fraction_to_power(self, power):
        """ summary: uses the function pow() to get the fraction to the specified power
            params:
                power: int; the power to which the fraction is raised
            returns: Fraction; a new fraction where the numerator and denominator are raised to the power specified
        """

        return Fraction(pow(self.numerator, power), pow(self.denominator, power))

    # Gets the other part of the fraction to make it one
    # For instance for 3/4 it would do 4 - 3/4 which would be 1/4 and 1/4 + 3/4 = 1
    def get_fraction_to_become_one(self):
        """ summary: gets the fraction that makes the current fraction + the new fraction equal to one
            for instance if the current fraction is 3/4 then 1 - 3/4 the new fraction would be 1/4
            params: None
            returns: Fraction; a new Fraction where the current fraction + the new fraction equals one
        """

        return Fraction(self.denominator - self.numerator, self.denominator)

    def __str__(self):
        """ summary: formats the Fraction in this form "numerator/denominator"
            params: None
            returns: String; "numerator/denominator"- looks like this when printed 1/4 (if numerator was 1 and denominator was 4)
        """
        return f"{self.numerator}/{self.denominator}"