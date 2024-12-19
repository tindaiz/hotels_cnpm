# import streamlit as st
# import firebase_admin
# from firebase_admin import firestore
# from firebase_admin import credentials
# from firebase_admin import auth
# import json
# import requests

# # Khởi tạo Firebase chỉ một lần
# cred = credentials.Certificate("E:\\hk7\\5.CMPM\\chay thu\\hotel-43f3e-f759d5da9de7.json")
# if not firebase_admin._apps:
#     firebase_admin.initialize_app(cred)

# def main():  
#     st.title(":key: :blue[Login / Sign up]")

#     if 'username' not in st.session_state:
#         st.session_state.username = ''
#     if 'useremail' not in st.session_state:
#         st.session_state.useremail = ''
        
#     def sign_up_with_email_and_password(email, password, username=None, return_secure_token=True):
#         try:
#             rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signUp"
#             payload = {
#                 "email": email,
#                 "password": password,
#                 "returnSecureToken": return_secure_token
#             }
#             if username:
#                 payload["displayName"] = username 
#             payload = json.dumps(payload)
#             r = requests.post(rest_api_url, params={"key": "AIzaSyCmkJEWJXUyEiVLjGKX-VomOa7wc7wTg_o"}, data=payload)
#             try:                                            

#                 return r.json()['email']
#             except:
#                 st.warning(r.json())
#         except Exception as e:
#             st.warning(f'Signup failed: {e}')

#     def sign_in_with_email_and_password(email=None, password=None, return_secure_token=True):
#         rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"

#         try:
#             payload = {
#                 "returnSecureToken": return_secure_token
#             }
#             if email:
#                 payload["email"] = email
#             if password:
#                 payload["password"] = password
#             payload = json.dumps(payload)
#             print('payload sigin',payload)
#             r = requests.post(rest_api_url, params={"key": "AIzaSyCmkJEWJXUyEiVLjGKX-VomOa7wc7wTg_o"}, data=payload)
#             try:
#                 data = r.json()
#                 user_info = {
#                     'email': data['email'],
#                     'username': data.get('displayName')  # Retrieve username if available
#                 }
#                 return user_info
#             except:
#                 st.warning(data)
#         except Exception as e:
#             st.warning(f'Signin failed: {e}')

#     def reset_password(email):
#         try:
#             rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode"
#             payload = {
#                 "email": email,
#                 "requestType": "PASSWORD_RESET"
#             }
#             payload = json.dumps(payload)
#             r = requests.post(rest_api_url, params={"key": "AIzaSyCmkJEWJXUyEiVLjGKX-VomOa7wc7wTg_o"}, data=payload)
#             if r.status_code == 200:
#                 return True, "Reset email Sent"
#             else:
#                 # Handle error response
#                 error_message = r.json().get('error', {}).get('message')
#                 return False, error_message
#         except Exception as e:
#             return False, str(e)

#     def f(): 
#         try:
#             userinfo = sign_in_with_email_and_password(st.session_state.email_input, st.session_state.password_input)
#             st.session_state.username = userinfo['username']
#             st.session_state.useremail = userinfo['email']
            
#             global Usernm
#             Usernm = (userinfo['username'])
            
#             st.session_state.signedout = True
#             st.session_state.signout = True    
  
#         except: 
#             st.warning('Login Failed')

#     def t():
#         st.session_state.signout = False
#         st.session_state.signedout = False   
#         st.session_state.username = ''

#     def forget():
#         email = st.text_input('Email')
#         if st.button('Send Reset Link'):
#             print(email)
#             success, message = reset_password(email)
#             if success:
#                 st.success("Password reset email sent successfully.")
#             else:
#                 st.warning(f"Password reset failed: {message}") 

#     if "signedout" not in st.session_state:
#         st.session_state["signedout"] = False
#     if 'signout' not in st.session_state:
#         st.session_state['signout'] = False    

#     if not st.session_state["signedout"]:
#         choice = st.selectbox('Login/Signup', ['Login', 'Sign up'])
#         email = st.text_input('Email Address')
#         password = st.text_input('Password', type='password')
#         st.session_state.email_input = email
#         st.session_state.password_input = password

#         if choice == 'Sign up':
#             username = st.text_input("Enter your unique username")
#             if st.button('Create my account'):
#                 user = sign_up_with_email_and_password(email=email, password=password, username=username)
#                 st.success('Account created successfully!')
#                 st.markdown('Please Login using your email and password')
#                 st.balloons()
#         else:
#             st.button('Login', on_click=f)
#             forget()

#     if st.session_state.signout:
#         st.text('Name: ' + st.session_state.username)
#         st.text('Email: ' + st.session_state.useremail)
#         st.button('Sign out', on_click=t)

import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth
import requests
import json

# Khởi tạo Firebase (chỉ một lần)
firebase_json_path = "hotel-43f3e-f759d5da9de7.json"  # Đường dẫn tới file JSON của Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_json_path)
    firebase_admin.initialize_app(cred)


def main():
    st.title(":key: Đăng nhập hoặc Đăng ký")

    # Quản lý trạng thái
    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''
    if 'signed_in' not in st.session_state:
        st.session_state.signed_in = False

    # Hàm đăng ký
    def sign_up(email, password, username=None):
        try:
            url = "https://identitytoolkit.googleapis.com/v1/accounts:signUp"
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": True
            }
            if username:
                payload["displayName"] = username
            r = requests.post(url, params={"key": "AIzaSyCmkJEWJXUyEiVLjGKX-VomOa7wc7wTg_o"}, json=payload)
            response = r.json()
            if 'error' in response:
                st.warning(f"Lỗi đăng ký: {response['error']['message']}")
            else:
                st.success("Tài khoản đã được tạo! Hãy đăng nhập.")
        except Exception as e:
            st.error(f"Lỗi đăng ký: {e}")

    # Hàm đăng nhập
    def sign_in(email, password):
        try:
            url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": True
            }
            r = requests.post(url, params={"key": "AIzaSyCmkJEWJXUyEiVLjGKX-VomOa7wc7wTg_o"}, json=payload)
            response = r.json()
            if 'error' in response:
                st.warning(f"Lỗi đăng nhập: {response['error']['message']}")
            else:
                st.session_state.signed_in = True
                st.session_state.username = response.get('displayName', '')
                st.session_state.useremail = response['email']
                st.success(f"Chào mừng, {st.session_state.username or 'Người dùng'}!")
        except Exception as e:
            st.error(f"Lỗi đăng nhập: {e}")

    # Giao diện
    if not st.session_state.signed_in:
        choice = st.radio("Chọn hành động", ["Đăng nhập", "Đăng ký"])
        email = st.text_input("Email")
        password = st.text_input("Mật khẩu", type="password")
        
        if choice == "Đăng ký":
            username = st.text_input("Tên người dùng (tuỳ chọn)")
            if st.button("Đăng ký"):
                sign_up(email, password, username)
        else:
            if st.button("Đăng nhập"):
                sign_in(email, password)
    else:
        st.success(f"Đã đăng nhập với email: {st.session_state.useremail}")
        if st.button("Đăng xuất"):
            st.session_state.signed_in = False
            st.session_state.username = ''
            st.session_state.useremail = ''
            st.info("Đã đăng xuất thành công!")
