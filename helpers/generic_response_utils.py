from rest_framework.response import Response


def log_and_respond(
    data:dict = None,
    status:int = None,
    message_code:int = None,
    message:str = None,
    exception = None,
    additional_data: dict =None,
    no_response : bool = False,
    error_info : dict = None,
    log_info: bool = False,
    user = None
):

    data = {} if data is None else data
    additional_data = {} if additional_data is None else additional_data
    error_info = {} if error_info is None else do_error_map(error_info)

    data.pop("details", None)
    data.pop("status_code", None)

    if exception is not None:
        print("------")
        # logger.error(exception)

    # Log info if enabled and user passed

    elif user is not None and not log_info:
        print("++++++++")
        # logger.info({
        #     "customer_id": user,
        #     "code": message_code,
        #     "message": message,
        #     "status": status,
        #     **additional_data
        # })

    response_body = {
        "code": message_code,
        "message": message,
        "data": data,
        **additional_data,
    }

    if error_info:
        response_body["error_info"] = error_info

    return response_body if no_response else Response(response_body, status)


def do_error_map(error_info):
    error_fields=['error_message','errors','response','status']
    error_data={}
    if isinstance(error_info,list):
        error_data['errors']=error_info
    elif isinstance(error_info,dict):
        error_data=error_info
    elif isinstance(error_info,str):
        error_data['error_message']=error_info

    error_data.update({"error_message":error_data.get('error_message',""),
                                  "errors":error_data.get("errors",[]),
                                  "response":error_data.get("response"),
                                  "status":error_data.get("status"),
                                  })

    [error_data.pop(k,{}) for k in list(error_data.keys()) if k not in error_fields]
    return error_data


def format_serializer_errors(serializer_errors):
    """Format DRF serializer errors into standardized format"""
    if not serializer_errors:
        return None

    formatted_errors = []
    for field, errors in serializer_errors.items():
        for error in errors:
            formatted_errors.append(f"{field}: {error}")

    return {
        "error_message": "",
        "errors": formatted_errors,
        "response": None,
        "status": None
    }