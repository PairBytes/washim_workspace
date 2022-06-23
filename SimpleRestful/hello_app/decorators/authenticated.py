from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity



def authenticated(permission=None):
    def authorized(fn):
        @jwt_required()
        @wraps(fn)
        def _wrap(*args, **kwargs):
            current_user_id = get_jwt_identity()
            if not current_user_id:
                return RestResponse(err='Unauthorized User !!').to_json(), 401
            user = UsersModel.find_by_uuid(current_user_id)
            if user:
                if not user.active:
                    return RestResponse(err='User profile is inactive').to_json(), 401
            else:
                return RestResponse(err='User is not found').to_json(), 400
            return fn(current_user_id=user.id, *args, **kwargs)

        return _wrap

    return authorized