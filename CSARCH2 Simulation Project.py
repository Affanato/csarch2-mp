from decimal import Decimal, getcontext, ROUND_DOWN

getcontext().prec = 50


def check_binary_digits(number):
    num_str = str(number)
    for char in num_str:
        if char == '-':  # Skip the negative sign
            continue
        if char == '.':  # Skip the decimal point
            continue
        if char != '1' and char != '0':  # Check if the character is not '1' or '0'
            print("Entered number is not in binary. Restart the program.")
            exit(0)


def binary_to_decimal(binary_number):
    # Convert the string input directly to a Decimal
    binary_number = Decimal(binary_number)
    negative = binary_number < 0

    if negative:
        binary_number *= -1

    fractional_part = binary_number % 1
    whole_part = binary_number - fractional_part

    # Convert whole part from binary to decimal
    dec_whole, i = Decimal(0), 0
    while whole_part > 0:
        r = whole_part % 10
        exp = r * (2 ** i)
        dec_whole = dec_whole + exp
        whole_part = whole_part // 10
        i += 1

    # Convert fractional part from binary to decimal
    dec_fractional, j = Decimal(0), 1
    while fractional_part > 0:
        fractional_part *= 10
        bit = int(fractional_part)
        exp = bit * (Decimal(2) ** - j)
        dec_fractional = dec_fractional + exp
        fractional_part -= bit
        j += 1

        # Limit the length of the binary fraction to avoid infinite loop
        if j > 50:
            break

    dec = dec_whole + dec_fractional

    if negative:
        dec *= -1
    return dec


def decimal_to_binary(decimal_number):
    if decimal_number == 0:
        return '0'

    is_negative = decimal_number < 0
    if is_negative:
        decimal_number = -decimal_number

    integer_part = int(decimal_number)
    fractional_part = decimal_number - integer_part

    binary_integer_part = bin(integer_part)[2:]

    binary_fractional_part = []
    while fractional_part and len(binary_fractional_part) < 52:  # Limit to 52 bits for precision
        fractional_part *= 2
        bit = int(fractional_part)
        binary_fractional_part.append(str(bit))
        fractional_part -= bit

    binary_fractional_part = ''.join(binary_fractional_part)
    binary_representation = binary_integer_part + '.' + binary_fractional_part if binary_fractional_part else binary_integer_part

    if is_negative:
        binary_representation = '-' + binary_representation

    return binary_representation


def single_digit_format(number, base):
    num_str = str(number)

    is_negative = num_str[0] == '-'
    if is_negative:
        num_str = num_str[1:]

    decimal_pos = num_str.find('.')

    if decimal_pos == -1:
        decimal_pos = len(num_str)
        num_str += '.'  # Append a decimal point if there isn't one

    # Count digits before and after the decimal point
    num_digits_before_decimal = decimal_pos
    num_str = num_str.replace('.', '')

    # Adjust the string to ensure the first digit before the decimal is not 0
    new_number = num_str.lstrip('0')
    if len(new_number) > 1:
        new_number = new_number[0] + '.' + new_number[1:]
    else:
        new_number = new_number + '.0'

    if is_negative:
        new_number = '-' + new_number

    # Return the new base after normalization
    new_base = int(base) + (decimal_pos - 1) - (len(num_str) - len(num_str.lstrip('0')))
    return new_number, new_base


def match_decimal_digits(num1, num2):
    # Convert inputs to Decimal for accurate decimal digit counting
    d1 = Decimal(str(num1))
    d2 = Decimal(str(num2))

    # Get the number of decimal digits in each number
    num1_decimals = abs(d1.as_tuple().exponent)
    num2_decimals = abs(d2.as_tuple().exponent)

    # Determine the maximum number of decimal digits
    max_decimals = max(num1_decimals, num2_decimals)

    # Extend num1 and num2 to match the maximum number of decimal digits
    new_num1 = d1.quantize(Decimal('1e-{0}'.format(max_decimals)))
    new_num2 = d2.quantize(Decimal('1e-{0}'.format(max_decimals)))

    return str(new_num1), str(new_num2), num1_decimals, num2_decimals


def normalize_exponents(num1, base1, num2, base2, max_decimals):
    d1 = Decimal(str(num1))
    d2 = Decimal(str(num2))

    # Determine the higher exponent
    higher_exponent = max(base1, base2)

    # Compute the offsets to align exponents
    offset1 = higher_exponent - base1
    offset2 = higher_exponent - base2

    # Normalize the numbers to have the same exponent
    new_num1 = d1 * (Decimal(10) ** -offset1)
    new_num2 = d2 * (Decimal(10) ** -offset2)

    # Ensure the precision for fractional parts
    precision = max(max_decimals, abs(offset1), abs(offset2))
    new_num1 = new_num1.quantize(Decimal('1e-{0}'.format(precision)))
    new_num2 = new_num2.quantize(Decimal('1e-{0}'.format(precision)))

    # Format numbers to avoid scientific notation for display
    new_num1_str = format(new_num1, f'.{precision}f')
    new_num2_str = format(new_num2, f'.{precision}f')

    return new_num1_str, higher_exponent, new_num2_str, higher_exponent


def limit_decimal_placement(number, limit):
    getcontext().prec = limit + 3

    quantize_str = '1.' + '0' * (limit + 3)
    quantize_format = Decimal(quantize_str)
    limited_number = number.quantize(quantize_format, rounding=ROUND_DOWN)

    return limited_number


def limit_decimal_places(value, digit_limit):

    getcontext().prec = digit_limit + 3

    if not isinstance(value, Decimal):
        value = Decimal(value)

    quantize_str = '1.' + '0' * digit_limit
    quantize_format = Decimal(quantize_str)

    limited_value = value.quantize(quantize_format, rounding=ROUND_DOWN)

    return limited_value


def NTTE(number, limit):
    num_str = str(number)

    count_digits = 0
    last_digit = 0
    valid_digits = ""
    remaining_digits = ""

    for char in num_str:
        if char.isdigit():
            if count_digits < limit:
                valid_digits += char
                count_digits += 1
                if char == '1':
                    last_digit = 1
                else:
                    last_digit = 0
            else:
                remaining_digits += char
        elif char in "-.":
            continue
        else:
            remaining_digits += char

    remaining_digits = "0." + remaining_digits
    remainder = binary_to_decimal(remaining_digits)

    loop_limit = limit - 2
    count = 0

    if remainder > 0.5:
        to_add = "0."
        while count < loop_limit:
            to_add += '0'
            count += 1
        to_add += '1'
        valid_digits = binary_to_decimal(number)
        to_add = binary_to_decimal(to_add)
        valid_digits += to_add

        valid_digits = decimal_to_binary(valid_digits)
        return valid_digits

    elif remainder == 0.5 and last_digit == 1:
        to_add = "0."
        while count < loop_limit:
            to_add += '0'
            count += 1
        to_add += '1'
        valid_digits = binary_to_decimal(number)
        to_add = binary_to_decimal(to_add)
        valid_digits += to_add

        valid_digits = decimal_to_binary(valid_digits)
        return valid_digits
    else:
        return number


""""------------------------------------------MAIN------------------------------------------"""
# Get inputs
print("IEEE-754 binary-32 floating point operation\n")
input_one = input("Enter First Binary Number: ")
check_binary_digits(input_one)
base_one = input("Enter Exponent Base 2: ")

input_two = input("\nEnter Second Binary Number: ")
check_binary_digits(input_two)
base_two = input("Enter Exponent Base 2: ")

# Get rounding method
rounding_method = input("\nChoose a rounding method:\n[1] G/R/S \n[2] Nearest Ties to Even:\n")

if rounding_method != "1" and rounding_method != "2":
    print("Please select only 1 or 2. Restart the program.")
    exit(0)

digit_limit = int(input("\nNumber of digits supported: "))

# Start of computation
adjusted_input_one, adjusted_base_one = single_digit_format(input_one, base_one)
adjusted_input_two, adjusted_base_two = single_digit_format(input_two, base_two)
adjusted_input_one, adjusted_input_two, num1_decimals, num2_decimals = match_decimal_digits(adjusted_input_one, adjusted_input_two)

"""
# Adjusted to only have 1 decimal placement 
print(f"Adjusted First Input: {adjusted_input_one} x 2 ^ {adjusted_base_one}")
print(f"Adjusted Second Input: {adjusted_input_two} x 2 ^ {adjusted_base_two}")
"""

max_decimal = max(num1_decimals, num2_decimals)
normalized_input_one, normalized_base_one, normalized_input_two, normalized_base_two = normalize_exponents(adjusted_input_one, adjusted_base_one, adjusted_input_two, adjusted_base_two, max_decimal)

# Adjusted to have the same exponent
print("\nNormalized Exponents")
print(f"Normalized First Input: {normalized_input_one} x 2 ^ {normalized_base_one}")
print(f"Normalized Second Input: {normalized_input_two} x 2 ^ {normalized_base_two}")

# Performs addition based on rounding method
if rounding_method == '1':
    GRS_value_one = limit_decimal_places(normalized_input_one, digit_limit + 2)
    GRS_value_two = limit_decimal_places(normalized_input_two, digit_limit + 2)

    value_input_one = binary_to_decimal(GRS_value_one)
    value_input_two = binary_to_decimal(GRS_value_two)
    value_sum = value_input_one + value_input_two
    value_sum = decimal_to_binary(value_sum)
    final_value, final_base = single_digit_format(value_sum, normalized_base_one)

    print("\nPerform Addition with respect to G/R/S")
    print("     " + str(GRS_value_one) + " x 2 ^ " + str(normalized_base_one))
    print("+    " + str(GRS_value_two) + " x 2 ^ " + str(normalized_base_two))
    print("Sum: " + str(final_value) + " x 2 ^ " + str(final_base))

    final_rounded = NTTE(final_value, digit_limit)
    final_value, final_base = single_digit_format(final_value, final_base)

    final_rounded = float(final_rounded)
    final_rounded = f"{final_rounded:.{digit_limit - 1}f}"

    print("\nRounded Final Answer:")
    print(str(final_rounded) + " x 2 ^ " + str(final_base))
else:
    value_input_one = binary_to_decimal(normalized_input_one)
    value_input_two = binary_to_decimal(normalized_input_two)
    value_sum = value_input_one + value_input_two
    value_sum = decimal_to_binary(value_sum)

    print("\nPerform Addition")
    print(f"     {normalized_input_one} x 2 ^ " + str(normalized_base_one))
    print(f"+    {normalized_input_two} x 2 ^ " + str(normalized_base_two))
    print(f"Sum: {value_sum} x 2 ^ {normalized_base_one}")

    final_value, final_base = single_digit_format(value_sum, normalized_base_one)
    final_rounded = NTTE(final_value, digit_limit)
    final_rounded, final_base = single_digit_format(final_rounded, final_base)
    final_rounded = float(final_rounded)
    final_rounded = f"{final_rounded:.{digit_limit - 1}f}"

    print("\nRounded Final Answer")
    print(str(final_rounded) + " x 2 ^ " + str(final_base))