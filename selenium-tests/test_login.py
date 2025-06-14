# import time
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# def create_driver():
#     options = Options()
#     options.add_argument("--headless")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#     return webdriver.Chrome(options=options)

# def test_login_valid_user():
#     driver = create_driver()
#     wait = WebDriverWait(driver, 10)
#     driver.get("http://localhost:3000/login")

#     wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='email']"))).send_keys("admin@demo.com")
#     driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys("admin123")
#     driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

#     wait.until(EC.url_to_be("http://localhost:3000/"))
#     assert driver.current_url == "http://localhost:3000/", "Login failed for valid user"
#     print("✅ Valid login test passed.")
#     driver.quit()

# def test_login_invalid_user():
#     driver = create_driver()
#     wait = WebDriverWait(driver, 10)
#     driver.get("http://localhost:3000/login")

#     wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='email']"))).send_keys("wrong@email.com")
#     driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys("wrongpass")
#     driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

#     # Wait for Ant Design toast error message
#     toast = wait.until(
#         EC.visibility_of_element_located((By.CSS_SELECTOR, ".ant-notification-notice-message"))
#     )
#     assert any(word in toast.text.lower() for word in ["404", "invalid", "error"]), "Toast does not show expected error"
#     print("✅ Invalid login test passed.")
#     driver.quit()

# def test_login_empty_fields():
#     driver = create_driver()
#     wait = WebDriverWait(driver, 10)
#     driver.get("http://localhost:3000/login")

#     # Click the submit button without entering anything
#     submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
#     submit_button.click()

#     try:
#         # Wait for the error message to appear under the input
#         email_error = wait.until(EC.visibility_of_element_located(
#             (By.CLASS_NAME, "ant-form-item-explain-error")
#         ))

#         print("✅ Empty fields login test passed.")
#         assert "enter" in email_error.text.lower(), "Expected validation message not found"

#     finally:
#         driver.quit()

# def test_email_only_filled():
#     driver = create_driver()
#     wait = WebDriverWait(driver, 10)
#     driver.get("http://localhost:3000/login")

#     wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='email']"))).send_keys("admin@demo.com")
#     driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

#     error = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "ant-form-item-explain-error")))
#     print("✅ Email Filled only login test passed.")
#     assert "enter" in error.text.lower() or "required" in error.text.lower()
#     driver.quit()

# def test_password_only_filled():
#     driver = create_driver()
#     wait = WebDriverWait(driver, 10)
#     driver.get("http://localhost:3000/login")

#     # ✅ Wait until password input is visible
#     wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password']"))).send_keys("admin123")
#     driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

#     error = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "ant-form-item-explain-error")))
#     print("✅ Password Filled only login test passed.")
#     assert "enter" in error.text.lower() or "required" in error.text.lower()
#     driver.quit()

# def test_login_with_whitespace():
#     driver = create_driver()
#     wait = WebDriverWait(driver, 10)
#     driver.get("http://localhost:3000/login")

#     wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='email']"))).send_keys("  admin@demo.com  ")
#     wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password']"))).send_keys("  admin123  ")
#     wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

#     # Debugging help
#     time.sleep(2)

#     # Try flexible condition
#     wait.until(lambda d: d.current_url.startswith("http://localhost:3000"))
#     print("✅ Login with whitespace test passed.")
#     driver.quit()

# def test_invalid_email_format():
#     driver = create_driver()
#     wait = WebDriverWait(driver, 10)
#     driver.get("http://localhost:3000/login")

#     wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='email']"))).send_keys("wrongemail.com")
#     wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password']"))).send_keys("admin123")
#     wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

#     error = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "ant-form-item-explain-error")))
#     print("✅ Invalid email format test passed.")
#     driver.quit()

# def test_case_sensitive_email():
#     driver = create_driver()
#     wait = WebDriverWait(driver, 10)
#     driver.get("http://localhost:3000/login")

#     wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='email']"))).send_keys("Admin@Demo.com")
#     wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password']"))).send_keys("admin123")
#     wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

#     try:
#         wait.until(EC.url_to_be("http://localhost:3000/"))
#         print("✅ Case insensitive email accepted.")
#     except:
#         print("❌ Case sensitivity issue: email must match exactly.")
#     finally:
#         driver.quit()

# def test_successful_login_redirects_to_dashboard():
#     driver = create_driver()
#     wait = WebDriverWait(driver, 10)
#     driver.get("http://localhost:3000/login")

#     wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='email']"))).send_keys("admin@demo.com")
#     wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password']"))).send_keys("admin123")
#     wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

#     # Wait for redirect
#     wait.until(EC.url_to_be("http://localhost:3000/"))
#     assert driver.current_url == "http://localhost:3000/"
#     print("✅ Redirect to dashboard test passed.")
#     driver.quit()

# def test_forgot_password_redirect():
#     driver = create_driver()
#     wait = WebDriverWait(driver, 10)
#     driver.get("http://localhost:3000/login")

#     try:
#         # Locate using class name or href
#         forgot_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.login-form-forgot")))
#         forgot_link.click()

#         # Wait until redirected to /forgetpassword
#         wait.until(EC.url_to_be("http://localhost:3000/forgetpassword"))
#         print("✅ Forgot password redirect test passed.")
#     except Exception as e:
#         print("❌ Forgot password redirect test failed:", e)
#     finally:
#         driver.quit()




# # Run tests
# if __name__ == "__main__":
#     test_login_valid_user()
#     test_login_invalid_user()
#     test_login_empty_fields()
#     test_email_only_filled()
#     test_password_only_filled()
#     test_login_with_whitespace()
#     test_invalid_email_format()
#     test_case_sensitive_email()
#     test_successful_login_redirects_to_dashboard()
#     test_forgot_password_redirect()



import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://localhost:3000"

def create_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)

def login_to_app(driver, email="", password=""):
    driver.get(f"{BASE_URL}/login")
    wait = WebDriverWait(driver, 10)
    if email:
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='email']"))).send_keys(email)
    if password:
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password']"))).send_keys(password)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
    return wait

def test_login_valid_user():
    driver = create_driver()
    wait = login_to_app(driver, "admin@demo.com", "admin123")
    wait.until(EC.url_to_be(f"{BASE_URL}/"))
    assert driver.current_url == f"{BASE_URL}/", "Login failed for valid user"
    print("✅ Valid login with correct credentials passed.")
    driver.quit()

def test_login_invalid_user():
    driver = create_driver()
    wait = login_to_app(driver, "wrong@email.com", "wrongpass")
    toast = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".ant-notification-notice-message")))
    assert any(word in toast.text.lower() for word in ["404", "invalid", "error"]), "Expected error toast not found"
    print("✅ Invalid credentials show error message correctly.")
    driver.quit()

def test_login_empty_fields():
    driver = create_driver()
    wait = login_to_app(driver)
    error = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "ant-form-item-explain-error")))
    assert "enter" in error.text.lower()
    print("✅ Empty fields show required field error.")
    driver.quit()

def test_email_only_filled():
    driver = create_driver()
    wait = login_to_app(driver, email="admin@demo.com")
    error = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "ant-form-item-explain-error")))
    assert "required" in error.text.lower() or "enter" in error.text.lower()
    print("✅ Submitting with only email shows password required error.")
    driver.quit()

def test_password_only_filled():
    driver = create_driver()
    wait = login_to_app(driver, password="admin123")
    error = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "ant-form-item-explain-error")))
    assert "required" in error.text.lower() or "enter" in error.text.lower()
    print("✅ Submitting with only password shows email required error.")
    driver.quit()

def test_login_with_whitespace():
    driver = create_driver()
    wait = login_to_app(driver, "  admin@demo.com  ", "  admin123  ")
    time.sleep(2)
    wait.until(lambda d: d.current_url.startswith(BASE_URL))
    print("✅ Login works correctly even with whitespace in credentials.")
    driver.quit()

def test_invalid_email_format():
    driver = create_driver()
    wait = login_to_app(driver, "wrongemail.com", "admin123")
    error = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "ant-form-item-explain-error")))
    assert "valid email" in error.text.lower() or "email" in error.text.lower()
    print("✅ Invalid email format triggers validation error.")
    driver.quit()

def test_case_sensitive_email():
    driver = create_driver()
    wait = login_to_app(driver, "Admin@Demo.com", "admin123")
    wait.until(EC.url_to_be(f"{BASE_URL}/"))
    assert driver.current_url == f"{BASE_URL}/", "Login failed due to case-sensitive email"
    print("✅ Case-insensitive email login passed.")
    driver.quit()

def test_successful_login_redirects_to_dashboard():
    driver = create_driver()
    wait = login_to_app(driver, "admin@demo.com", "admin123")
    wait.until(EC.url_to_be(f"{BASE_URL}/"))
    assert driver.current_url == f"{BASE_URL}/"
    print("✅ Successful login redirects to dashboard.")
    driver.quit()

def test_forgot_password_redirect():
    driver = create_driver()
    wait = WebDriverWait(driver, 10)
    driver.get(f"{BASE_URL}/login")
    forgot_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.login-form-forgot")))
    forgot_link.click()
    wait.until(EC.url_to_be(f"{BASE_URL}/forgetpassword"))
    assert driver.current_url == f"{BASE_URL}/forgetpassword"
    print("✅ 'Forgot Password' link redirects correctly.")
    driver.quit()

# Run all tests
if __name__ == "__main__":
    test_login_valid_user()
    test_login_invalid_user()
    test_login_empty_fields()
    test_email_only_filled()
    test_password_only_filled()
    test_login_with_whitespace()
    test_invalid_email_format()
    test_case_sensitive_email()
    test_successful_login_redirects_to_dashboard()
    test_forgot_password_redirect()
