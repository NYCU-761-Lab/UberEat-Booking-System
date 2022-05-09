def check_username(username):
    # allows only one white space
    if username.count(" ") > 1:
        return False
    elif username.count(" ") == 1:
        # if contain " ", the format need to be XX OO
        if username[0] == " " or username[len(username)-1] == " ":
            return False
        elif not (0 < len(username) and len(username) <= 256):
            return False
        else:
            # check if only contain Eng letters
            name_list = username.split(" ")
            for name_part in name_list:
                if not name_part.isalnum():
                    return False
    elif username.count(" ") == 0:
        if not username.isalnum() or not (0 < len(username) and len(username) <= 256):
            return False

    return True


def is_float(float_str):
    try:
        float(float_str)
        return True
    except ValueError:
        return False