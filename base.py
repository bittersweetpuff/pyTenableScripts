import requests, sys, logging, re, time, logging, warnings, json


def TypeCheck(
    name, obj, expected_type, choices=None, default=None, case=None, pattern=None
):
    """
    Internal function for validating that inputs we are receiving are of
    the right type, have the expected values, and can handle defaults as
    necessary.

    Args:
        name (str): The name of the object (for exception reporting)
        obj (obj): The object that we will be checking
        expected_type (type):
            The expected type of object that we will check against.
        choices (list, optional):
            if the object is only expected to have a finite number of values
            then we can check to make sure that our input is one of these
            values.
        default (obj, optional):
            if we want to return a default setting if the object is None,
            we can set one here.
        case (string, optional):
            if we want to force the object values to be upper or lower case,
            then we will want to set this to either ``upper`` or ``lower``
            depending on the desired outcome.  The returned object will then
            also be in the specified case.
        pattern (string, optional):
            If we want to validate the input based on a regex pattern, then
            we should specify one here.

    Returns:
         obj: Either the object or the default object depending.
    """

    # We have a simple function to convert the case of string values so that
    # we can ensure correct output.
    def conv(obj, case):
        """
        Case conversion function
        """
        if case == "lower":
            if isinstance(obj, list):
                return [i.lower() for i in obj if isinstance(i, str)]
            elif isinstance(obj, str):
                return obj.lower()
        elif case == "upper":
            if isinstance(obj, list):
                return [i.upper() for i in obj if isinstance(i, str)]
            elif isinstance(obj, str):
                return obj.upper()
        return obj

    # Convert the case of the inputs.
    obj = conv(obj, case)
    choices = conv(choices, case)
    default = conv(default, case)

    # If the object sent to us has a None value, then we will return None.
    # If a default was set, then we will return the default value.
    if obj == None:
        return default

    # As we can support a singular expected type, or multiple types, we need
    # to check to see if the expected types was a list of types.  If so, we
    # will just pass expected_types into the etypes list.  If not, then this
    # is a singular type, and we will want to wrap it into a list before
    # passing to the etypes list.
    if isinstance(expected_type, list) and len(expected_type) > 0:
        etypes = expected_type
    else:
        etypes = [expected_type]

    # If the type is of "uuid", then we will specify a pattern and then
    # overload the type to be a type of str.
    if "uuid" in etypes:
        pattern = r"^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$"
        etypes[etypes.index("uuid")] = str

    if "scanner-uuid" in etypes:
        pattern = r"^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12,32}$"
        etypes[etypes.index("scanner-uuid")] = str

    # If we are checking for a string type, we will also want to check for
    # unicode type transparently, so add the unicode type to the expected
    # types list.  NOTE this is for Python2 only, as Python3 treats all
    # strings as type string.
    str_types = str
    if str in etypes:
        try:
            etypes.append(unicode)
            str_types = (str, unicode)
        except NameError:
            pass

    # iterate through the expected types and flag as passing if any of the
    # types match.
    type_pass = False
    for etype in etypes:
        if not type_pass:
            if isinstance(obj, etype):
                type_pass = True
            elif isinstance(obj, str_types) and etype not in [list, tuple]:
                # if the expected type is not a list or tuple and it is a
                # string type, then we will attempt to recast the object
                # to be the expected type.
                try:
                    new_obj = etype(obj)
                except:
                    # if the recasting fails, then just pass through.
                    pass
                else:
                    if etype == bool:
                        # if the expected type was boolean, then we will
                        # want to ensure that the string is one of the
                        # allowed values.  From there we will set the
                        # object to be either True or False.  in either case
                        # we will also want to make sure to set the
                        # type_pass flag to ensure we don't raise a
                        # TypeError later on.
                        if obj.lower() in ["true", "false", "yes", "no"]:
                            type_pass = True
                            obj = obj.lower() in ["true", "yes"]
                    else:
                        # In every other case, just set the object to be the
                        # recasted object and set the type_pass flag.
                        obj = new_obj
                        type_pass = True

    # If the object is none of the right types then we want to raise a
    # TypeError as it was something we weren't expecting.
    if not type_pass:
        raise TypeError("Wrong type")

    # if the object is only expected to have one of a finite set of values,
    # we should check against that and raise an exception if the the actual
    # value is outside of what we expect.

    if isinstance(obj, list):
        for item in obj:
            if isinstance(choices, list) and item not in choices:
                raise UnexpectedValueError(
                    "{} has value of {}.  Expected one of {}".format(
                        name, obj, ",".join([str(i) for i in choices])
                    )
                )
    elif isinstance(choices, list) and obj not in choices:
        raise UnexpectedValueError(
            "{} has value of {}.  Expected one of {}".format(
                name, obj, ",".join([str(i) for i in choices])
            )
        )

    if pattern and isinstance(obj, str):
        if len(re.findall(pattern, str(obj))) <= 0:
            raise UnexpectedValueError(
                "{} has value of {}.  Does not match pattern {}".format(
                    name, obj, pattern
                )
            )

    # if we made it this fire without an exception being raised, then assume
    # everything is good to go and return the object passed to us initially.
    return obj
