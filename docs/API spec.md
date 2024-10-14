Crop-Type API spec

- Authentication
    - login
        request
            email and password
        response
            token and userinfo
        description
            when user login with email and password, API will response with token and some userinfo
    - register
        request
            email, password and re_password
        response
            token and userinfo
        description
            when user register with email and password, API will response with token and some userinfo
    - forgot_password
        request
            email
        response
            return "success"
        description
            when user send forgot password request with email, will send reset_password link to email
    - reset_password
        request
            token, password
        response
            token, userinfo
        description
            when user send token and password, will set password for user
        
- Admin
    - get_all_users
        request
            type
        response
            will send all typed users info
        detail
            when user send type, API will response typed users list
    - set_activate_user
        request
            email
        response
            return "success"
        description
            when user send email, will set user's is_active -> true
    - set_deavtivate_user
        request
            email
        response
            return "success"
        description
            when user send email, will set user's is_active -> false
- User
    - get_userinfo
        request
        response
            return userinfo
        description
            return userinfo related to token user
    - update_userinfo
        request
            userinfo
        response
            return "success"
        description
            will update userinfo related to token user
- FarmCrop
    - get_crops_from_buffer
        request
            location, range
        response
            farmcrop polygons, crop, crop color
        descroption
            when user send location and range, will check farmcrop polygons inside circle, then will send polygondata and cropname, and color 
    - get_crops_from_polygon
        request
            polygon data
        response
            farmcrop polygons, crop, crop color
        descroption
            when user send buffer data, will check farmcrop polygons inside buffer, then will send polygondata and cropname, and color