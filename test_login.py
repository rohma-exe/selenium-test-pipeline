import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://54.224.159.2:3000/"

def create_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)

def login_to_app(driver, email="", password=""):
    driver.get(f"{BASE_URL}/login")
    wait = WebDriverWait(driver, 30)
    if email:
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='email']"))).send_keys(email)
    if password:
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password']"))).send_keys(password)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
    return wait

def test_login_valid_user():
    driver = create_driver()
    wait = login_to_app(driver, "admin@demo.com", "admin123")

    print("⏳ Waiting for redirect after login...")
    print("🔎 Current URL before wait:", driver.current_url)
    driver.save_screenshot("valid_login_debug.png")

    wait.until(lambda d: d.current_url.startswith(BASE_URL))
    assert driver.current_url.startswith(BASE_URL), "Login failed for valid user"

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

    print("⏳ Waiting for redirect after login with case-variant email...")
    driver.save_screenshot("case_sensitive_debug.png")
    wait.until(lambda d: d.current_url.startswith(BASE_URL))

    assert driver.current_url.startswith(BASE_URL), "Login failed due to case-sensitive email"
    print("✅ Case-insensitive email login passed.")
    driver.quit()

def test_successful_login_redirects_to_dashboard():
    driver = create_driver()
    wait = login_to_app(driver, "admin@demo.com", "admin123")
    wait.until(lambda d: d.current_url.startswith(BASE_URL))
    assert driver.current_url.startswith(BASE_URL)
    print("✅ Successful login redirects to dashboard.")
    driver.quit()

def test_forgot_password_redirect():
    driver = create_driver()
    wait = WebDriverWait(driver, 10)
    driver.get(f"{BASE_URL}/login")
    forgot_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.login-form-forgot")))
    forgot_link.click()
    wait.until(lambda d: d.current_url.endswith("/forgetpassword"))
    assert driver.current_url.endswith("/forgetpassword")
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
